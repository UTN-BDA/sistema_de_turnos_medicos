
# Proyecto: Sistema de Turnos Médicos Inteligente
# Medical Center API

Este proyecto es una API REST para la gestión de turnos médicos, desarrollada con Flask y PostgreSQL. Utiliza contenedores Docker para facilitar su despliegue y está preparada para pruebas mediante herramientas como Insomnia o Postman.

## Contenido

- [Requisitos](#requisitos)
- [Clonación del proyecto](#clonación-del-proyecto)
- [Configuración del entorno](#configuración-del-entorno)
- [Inicialización del proyecto](#inicialización-del-proyecto)
- [Población de la base de datos](#población-de-la-base-de-datos)
- [Uso de la API](#uso-de-la-api)
- [Visualización de notificaciones](#visualización-de-notificaciones)

---

## Requisitos

- Docker y Docker Compose instalados.
- Herramienta para pruebas de APIs (Insomnia o Postman).

---

## Clonación del proyecto

Podés clonar este repositorio de dos formas:

```bash
https://github.com/UTN-BDA/sistema_de_turnos_medicos.git
# o
gh repo clone UTN-BDA/sistema_de_turnos_medicos
```

---

## Configuración del entorno

1. En la raíz del proyecto, vas a encontrar el archivo `example.env`, que contiene las variables de entorno necesarias, pero con valores genéricos.

2. Creá un archivo `.env` en la raíz del proyecto. Podés pegar el contenido de `example.env`. O hacerlo desde la terminal con:

```bash
cp example.env .env
```

3. Editá `.env` con tus credenciales y configuraciones reales:

  **Por ejemplo:**

```env
FLASK_ENV=development
DATABASE_URL=postgresql://usuario:contraseña@db:5432/sistema_de_turnos_dev
```

---

## Inicialización del proyecto

Para levantar la aplicación, ejecutá en la raíz del proyecto (recordar abrir Docker Desktop):

```bash
docker compose up --build -d
```

Esto iniciará los contenedores de la aplicación y la base de datos.

---

## Población de la base de datos

Una vez que los contenedores estén corriendo, tenés dos opciones:

### Opción 1: Usar el backup

1. Pedir el backup a algún desarrolador mediante discord:
    **fbayinay_**
    **guillermo09213**
    **nazaaab**
2. Copia la carpeta suministrada a la raíz del proyecto.
3. Abrí una nueva terminal.
4. Copiá el archivo de backup al contenedor de la base de datos:

```bash
docker cp db/backup.sql sistema_de_turnos_medicos-db-1:/backup.sql
```

5. Restaurá el contenido de la base de datos:

```bash
docker exec -it sistema_de_turnos_medicos-db-1 psql -U <usuario> -d <nombre_bd> -f /backup.sql
```

### Opción 2: Usar `seed_data.py`

1. Consultá el nombre del contenedor de la app con:

```bash
docker ps
```

2. Ejecutá los siguientes comandos:

```bash
docker exec -it sistema_de_turnos_medicos-web-1 flask db upgrade
docker exec -it sistema_de_turnos_medicos-web-1 python -m scripts.seed_data
```

3. Deberías ver un mensaje indicando que la población inicial fue exitosa.

---
## Importante la opción que se elija se tiene que hacer con los volumenes vacíos

Si ya probó con una opción y quiere probar la otra, debe hacer:

1. Parar los contenedores:

```bash
docker compose down
```

2. Eliminar volúmenes:

```bash
docker volume rm sistema_de_turnos_medicos_postgres_data
```

3. Levantar de nuevo los contenedores:

```bash
docker compose up --build -d
```
**Ya puede probar la otra opción**   

## Uso de la API

La aplicación expone dos funciones coordinadoras para la gestión de turnos:

### 📌 Crear un turno con notificación

- Método: `POST`
- Ruta: `http://localhost:5000/coordinadoras/crear-con-notificacion`
- Body (JSON):

📍 **Ejemplo:**

```json
{
  "paciente_id": 1,
  "medico_id": 105,
  "administrativo_id": 121,
  "fecha_hora": "2025-06-14T11:10:00"
}
```

### 📌 Modificar un turno con notificación

- Método: `PUT`
- Ruta: `http://localhost:5000/coordinadoras/modificar-con-notificacion`
- Body (JSON):

📍 **Ejemplo:**

```json
{
  "turno_id": 2,
  "nueva_fecha_str": "2025-06-14T10:30:00",
  "nuevo_estado": "reprogramado",
  "origen": "administrativo"
}
```

👉 Para turnos cancelados, atendidos o perdidos, revisar la función `modificar_turno_con_notificacion` en `coordinadoras_controller.py`.

---

## Visualización de notificaciones

1. Con los contenedores ejecutándose, accedé a:

```
http://localhost:5000/web/paciente/<id>
```

2. Reemplazá `<id>` con el ID de un paciente registrado en la base de datos.

3. Al crear o modificar un turno desde Insomnia o Postman, se generará una notificación que se mostrará automáticamente en la web del paciente si tiene una sesión activa.

4. Las notificaciones se crean como `no_leídas` y cambian a `leídas` al ser 'abiertas'. Esto también puede verificarse en la base de datos.

5. Cada paciente puede recibir hasta **3 notificaciones visualizadas a la vez**. Las más antiguas serán reemplazadas por nuevas.

   > 📌 Desde la administración del centro médico se pueden gestionar múltiples turnos para un mismo paciente (sin límite), y pueden generarse muchas notificaciones asociadas a esos turnos.  
   > Sin embargo, en el "dispositivo" del paciente solo se mostrarán **las 3 notificaciones más recientes**, reemplazando las anteriores.

> 💡 Las sesiones por WebSockets se cierran al recargar o cerrar la web, lo que elimina la visualización de notificaciones.
