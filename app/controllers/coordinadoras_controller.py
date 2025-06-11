from flask import request, jsonify
from flask_socketio import emit
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.sockets import notificar_paciente
from app.models.turnos import Turno, EstadoTurno
from app.models.medicos import Medico
from app.models.usuarios import Usuario
from app.services.turnos_service import crear_turno, modificar_turno
from app.services.notificaciones_service import crear_notificacion

def crear_turno_con_notificacion():
    data = request.get_json()
    try:
        with db.session.begin():  # Inicia transacción

            # 1. Validaciones
            paciente = db.session.get(Usuario, data.get("paciente_id"))
            administrativo = db.session.get(Usuario, data.get("administrativo_id"))
            # Obtener directamente al médico como Medico (hereda de Usuario)
            medico = db.session.get(Medico, data.get("medico_id"))

            if not paciente or paciente.tipo.name != "PACIENTE":
                return jsonify({"error": "Paciente inválido"}), 400
            if not administrativo or administrativo.tipo.name != "ADMIN":
                return jsonify({"error": "Administrativo inválido"}), 400
            if not medico or not isinstance(medico, Medico):
                return jsonify({"error": "Médico inválido"}), 400            

            # 2. Verificar disponibilidad (con bloqueo)
            try:
                fecha_hora = datetime.fromisoformat(data["fecha_hora"])
            except ValueError:
                return jsonify({"error": "Formato de fecha inválido (se espera ISO 8601)"}), 400
            
            resultado = db.session.execute(
                db.select(Turno)
                .where(
                    Turno.medico_id == medico.id,
                    Turno.fecha_hora == fecha_hora,
                    Turno.estado == EstadoTurno.PROGRAMADO
                )
                .with_for_update()
            ).first()

            if resultado:
                return jsonify({"error": "El médico ya tiene un turno en esa fecha y hora"}), 409

            # 3. Crear turno
            turno_data = {
                "fecha_hora": data["fecha_hora"],   # Se puede pasar como string si el service convierte
                "paciente_id": paciente.id,
                "medico_id": medico.id,
                "administrativo_id": administrativo.id
            }
            turno = crear_turno(turno_data)
            db.session.add(turno)
            db.session.flush()  # Obtener ID

            # 4. Crear notificación
            mensaje = (f"Su turno para {medico.especialidad} es el día {fecha_hora.strftime('%d/%m/%Y')} a las {fecha_hora.strftime('%H:%M')}.\n"
            f"Profesional: Dr. {medico.nombre}")
            noti_data = {
                "tipo": "otorgamiento",
                "mensaje": mensaje,
                "turno_id": turno.id,
                "origen": "sistema"
            }
            notificacion = crear_notificacion(noti_data)
            db.session.add(notificacion)

        # Fin de la transacción: commit automático si no hubo errores

        # 5. Emitir evento por socket fuera de la transacción
        notificar_paciente(paciente.id, {
            "mensaje": mensaje,
            "id": notificacion.id
        })

        return jsonify({"mensaje": "Turno y notificación creados correctamente"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "detalles": str(e)}), 500

def modificar_turno_con_notificacion():
    data = request.get_json()
    try:
        with db.session.begin():
             # Verificar disponibilidad (con bloqueo)
            nueva_fecha_str = data.get("nueva_fecha_str")
            if nueva_fecha_str:
                try:
                    nueva_fecha = datetime.fromisoformat(nueva_fecha_str)
                except ValueError:
                    raise ValueError("Formato de fecha inválido (se espera ISO 8601)")

                # Obtener turno actual para acceder al médico
                turno_actual = db.session.get(Turno, data["turno_id"])
                if not turno_actual:
                    raise ValueError("Turno no encontrado")

                resultado = db.session.execute(
                    db.select(Turno)
                .where(
                    Turno.medico_id == turno_actual.medico_id,
                    Turno.fecha_hora == nueva_fecha,
                    Turno.estado.in_([EstadoTurno.PROGRAMADO, EstadoTurno.REPROGRAMADO]),
                    Turno.id != turno_actual.id
                )
                .with_for_update()
                ).first()

                if resultado:
                    raise ValueError("El médico ya tiene un turno en esa fecha y hora")

            # Modificar el turno
            turno_modificado = modificar_turno(
                turno_id=data["turno_id"],
                nueva_fecha_str=data.get("nueva_fecha_str"),
                nuevo_estado=data.get("nuevo_estado")
            )
            db.session.add(turno_modificado)

            # Determinar tipo de notificación según el nuevo estado
            estado = turno_modificado.estado.value  # "programado", "reprogramado", etc.
            tipo_map = {
                "programado": "otorgamiento",
                "reprogramado": "reprogramacion",
                "cancelado": "cancelacion",
                "atendido": "consulta_realizada",
                "perdido": "perdida_del_turno"
            }
            try:
                tipo_notificacion = tipo_map[estado]
            except KeyError:
                raise ValueError(f"Estado inesperado: {estado}")

            # Asegurarse de que las relaciones están cargadas
            fecha_hora = turno_modificado.fecha_hora
            medico = turno_modificado.medico

            # Generar mensaje dinámico
            if estado == "reprogramado":
                mensaje = (
                    f"Su turno para {medico.especialidad} ha sido reprogramado para el día "
                    f"{fecha_hora.strftime('%d/%m/%Y')} a las {fecha_hora.strftime('%H:%M')}.\n"
                    f"Profesional: Dr. {medico.nombre}"
                )
            elif estado in ["cancelado", "atendido", "perdido"]:
                mensaje = (
                    f"Su turno para {medico.especialidad} del día "
                    f"{fecha_hora.strftime('%d/%m/%Y')} a las {fecha_hora.strftime('%H:%M')}.\n"
                    f"Profesional: Dr. {medico.nombre}\n"
                    f"Ha sido {estado}"
                )
            else:
                mensaje = data.get("mensaje", f"El estado de su turno ha cambiado a {estado}")    

            noti_data = {
                "tipo": tipo_notificacion,
                "mensaje": mensaje,
                "turno_id": turno_modificado.id,
                "origen": data.get("origen", "sistema")
            }

            notificacion = crear_notificacion(noti_data)
            db.session.add(notificacion)
            db.session.flush()  # Para obtener notificacion.id si es necesario


        # Emitir notificación al paciente fuera de la transacción
        notificar_paciente(turno_modificado.paciente_id, {
        "mensaje": notificacion.mensaje,
        "id": notificacion.id
        })

        return jsonify({"mensaje": "Turno modificado y notificación enviada"}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        print(f"[ERROR] {str(e)}")  # o logger.error(...)
        return jsonify({"error": "Error interno al modificar el turno"}), 500


'''def modificar_turno_con_notificacion():
    try:
        data = request.get_json(force=True)
        print(f"[INFO] Datos recibidos: {data}")

        with db.session.begin():
            turno_modificado = modificar_turno(
                turno_id=data["turno_id"],
                nueva_fecha_str=data.get("nueva_fecha_str"),
                nuevo_estado=data.get("nuevo_estado")
            )
            print(f"[INFO] Turno modificado: ID={turno_modificado.id}, Estado={turno_modificado.estado}")

        try:
            estado = turno_modificado.estado.value
            tipo_map = {
                "programado": "otorgamiento",
                "reprogramado": "reprogramacion",
                "cancelado": "cancelacion",
                "atendido": "consulta_realizada",
                "perdido": "perdida_del_turno"
            }
            tipo_notificacion = tipo_map[estado]
            print(f"[INFO] Tipo de notificación determinado: {tipo_notificacion}")
        except KeyError:
            print(f"[ERROR] Estado inesperado: {estado}")
            return jsonify({"error": f"Estado inesperado: {estado}"}), 400

        # Asegurar que se pueda acceder a relaciones
        try:
            fecha_hora = turno_modificado.fecha_hora
            medico = turno_modificado.medico
            print(f"[INFO] Médico: {medico.nombre} - Especialidad: {medico.especialidad}")
        except Exception as e:
            print(f"[ERROR] No se pudo acceder al médico del turno: {e}")
            return jsonify({"error": "Error al acceder a los datos del médico"}), 500

        try:
            if estado == "reprogramado":
                mensaje = (
                    f"Su turno para {medico.especialidad} ha sido reprogramado para el día "
                    f"{fecha_hora.strftime('%d/%m/%Y')} a las {fecha_hora.strftime('%H:%M')}.\n"
                    f"Profesional: Dr. {medico.nombre}"
                )
            elif estado in ["cancelado", "atendido", "perdido"]:
                mensaje = (
                    f"Su turno para {medico.especialidad} del día "
                    f"{fecha_hora.strftime('%d/%m/%Y')} a las {fecha_hora.strftime('%H:%M')}.\n"
                    f"Profesional: Dr. {medico.nombre}\n"
                    f"Ha sido {estado}"
                )
            else:
                mensaje = data.get("mensaje", f"El estado de su turno ha cambiado a {estado}")
        except Exception as e:
            print(f"[ERROR] Error al generar el mensaje: {e}")
            return jsonify({"error": "Error al generar el mensaje de notificación"}), 500

        try:
            noti_data = {
                "tipo": tipo_notificacion,
                "mensaje": mensaje,
                "turno_id": turno_modificado.id,
                "origen": data.get("origen", "sistema")
            }
            print(f"[INFO] Datos de la notificación: {noti_data}")
            notificacion = crear_notificacion(noti_data)
            db.session.add(notificacion)
            db.session.flush()
        except Exception as e:
            print(f"[ERROR] Error al crear o guardar la notificación: {e}")
            return jsonify({"error": "Error al crear la notificación"}), 500

        try:
            notificar_paciente(turno_modificado.paciente_id, {
            "mensaje": notificacion.mensaje,
            "id": notificacion.id
            })
            print(f"[INFO] Notificación emitida al paciente ID={turno_modificado.paciente_id}")
        except Exception as e:
            print(f"[ERROR] Falló el envío de la notificación: {e}")
            return jsonify({"error": "Error al emitir la notificación"}), 500

        return jsonify({"mensaje": "Turno modificado y notificación enviada"}), 200

    except ValueError as e:
        print(f"[ERROR - ValueError]: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"[ERROR - General]: {e}")
        return jsonify({"error": "Error interno al modificar el turno"}), 500
'''
