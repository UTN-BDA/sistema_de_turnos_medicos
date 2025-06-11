from faker import Faker
from app import create_app, db
from sqlalchemy import text
from app.models.usuarios import TipoUsuario
from app.models.pacientes import Paciente
from app.models.medicos import Medico
from app.models.administrativos import Administrativo

fake = Faker(['es_AR'])  # Se puede cambiar a 'es_ES' o dejar por defecto

app = create_app()

def generar_email_unico(nombre, usados):
    base = nombre.lower().replace(" ", ".").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    while True:
        sufijo = fake.random_int(min=10, max=99)  # 2 cifras
        email = f"{base}{sufijo}@ejemplo.com"
        if email not in usados:
            usados.add(email)
            return email

with app.app_context():
    print("Eliminando datos existentes...")
    db.session.execute(text("TRUNCATE TABLE turnos RESTART IDENTITY CASCADE;"))
    db.session.execute(text("TRUNCATE TABLE notificaciones RESTART IDENTITY CASCADE;"))
    db.session.execute(text("TRUNCATE TABLE pacientes RESTART IDENTITY CASCADE;"))
    db.session.execute(text("TRUNCATE TABLE medicos RESTART IDENTITY CASCADE;"))
    db.session.execute(text("TRUNCATE TABLE administrativos RESTART IDENTITY CASCADE;"))
    db.session.execute(text("TRUNCATE TABLE usuarios RESTART IDENTITY CASCADE;"))
    db.session.commit()

    emails_usados = set()

    print("Generando pacientes...")
    pacientes = []
    for _ in range(100):
        nombre = fake.name()
        paciente = Paciente(
            nombre=nombre,
            email=generar_email_unico(nombre, emails_usados),
            tipo=TipoUsuario.PACIENTE,
            nro_historia_clinica=fake.unique.bothify("HC-#####")
        )
        pacientes.append(paciente)
    db.session.add_all(pacientes)

    print("Generando médicos...")
    especialidades = ["Cardiología", "Pediatría", "Neurología", "Clínica Médica", "Traumatología"]
    medicos = []
    for _ in range(20):
        nombre = fake.name()
        medico = Medico(
            nombre=nombre,
            email=generar_email_unico(nombre, emails_usados),
            tipo=TipoUsuario.MEDICO,
            matricula=fake.unique.bothify("MAT-#####"),
            especialidad=fake.random_element(especialidades)
        )
        medicos.append(medico)
    db.session.add_all(medicos)

    print("Generando administrativos...")
    administrativos = []
    for _ in range(5):
        nombre = fake.name()
        admin = Administrativo(
            nombre=nombre,
            email=generar_email_unico(nombre, emails_usados),
            tipo=TipoUsuario.ADMIN,
            nro_legajo=fake.unique.bothify("LEG-####")
        )
        administrativos.append(admin)
    db.session.add_all(administrativos)

    db.session.commit()
    print("✅ Base de datos poblada exitosamente.")
