# Proyecto: Sistema de Turnos Médicos Inteligente

## Descripción

Este proyecto tiene como objetivo desarrollar una aplicación backend para la gestión de turnos médicos en hospitales o clínicas, enfocada en reducir el tiempo de espera en las salas y mejorar la atención a pacientes, especialmente personas mayores. El sistema permite que los doctores informen a los pacientes sobre adelantos, retrasos o emergencias relacionadas con sus turnos, notificándolos en tiempo real. Esto busca evitar que los pacientes esperen innecesariamente y mejorar la organización de los consultorios.

## Características principales

- Registro de pacientes y doctores.
- Asignación y consulta de turnos médicos.
- Cambio de estado de los turnos (adelantado, retrasado, en atención, cancelado).
- Notificaciones automáticas al paciente ante cualquier cambio relevante.
- Backend preparado para integrar un frontend o app móvil en el futuro.

## Tecnologías utilizadas

- **Lenguaje:** Python 3
- **Framework:** Flask
- **ORM:** SQLAlchemy
- **Base de datos:** PostgreSQL
- **Contenedores:** Docker y Docker Compose
- **Estructura modular:** Separación en capas (modelos, servicios, rutas, esquemas, notificaciones)

## Estructura del proyecto

El proyecto sigue una estructura organizada para facilitar su mantenimiento y escalabilidad. La carpeta `app/` contiene todo el código de la aplicación, incluyendo modelos, rutas, servicios y lógica de notificaciones. El entorno se gestiona con Docker para simplificar la instalación y ejecución del sistema.

## Integrantes del equipo

-Bayinay Federico
-Barros Nazareno
-Quinteros Guillermo

## Información adicional

Este proyecto está orientado principalmente a la aplicación de conceptos avanzados de modelado y diseño de bases de datos relacionales, por lo que el foco está puesto en la arquitectura de datos, relaciones entre entidades y su interacción con el ORM. El desarrollo de la interfaz gráfica no está contemplado en esta etapa, pero el backend queda preparado para futuras integraciones.
