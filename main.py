# ===== PARTE 1: conexión y modelo de la tabla =====
import os

from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import Column, Date, Integer, String, create_engine, func, select
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base

load_dotenv()  # lee las credenciales del archivo .env

TOTAL = 100_000   # registros a insertar
LOTE = 10_000     # tamaño de cada inserción por lotes

Base = declarative_base()


class Persona(Base):
    __tablename__ = "personas_juan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(60))
    apellido = Column(String(60))
    correo = Column(String(120))
    fecha_nacimiento = Column(Date)
    ciudad = Column(String(80))
    direccion = Column(String(150))
    telefono = Column(String(50))
    profesion = Column(String(150))


def crear_engine():
    url = URL.create(
        "mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME"),
    )
    return create_engine(url)


# ===== PARTE 2: generación de datos con Faker =====
def generar_personas(n):
    fake = Faker("es_CO")
    personas = []
    for _ in range(n):
        personas.append({
            "nombre": fake.first_name(),
            "apellido": fake.last_name(),
            "correo": fake.email(),
            "fecha_nacimiento": fake.date_of_birth(minimum_age=18, maximum_age=80),
            "ciudad": fake.city(),
            "direccion": fake.street_address(),
            "telefono": fake.phone_number(),
            "profesion": fake.job(),
        })
    return personas


# ===== PARTE 3: inserción por lotes y main =====
def insertar(engine, datos):
    with engine.begin() as conn:
        for i in range(0, len(datos), LOTE):
            conn.execute(Persona.__table__.insert(), datos[i:i + LOTE])
            print(f"Insertados {min(i + LOTE, len(datos))} de {len(datos)}")


def main():
    engine = crear_engine()
    Base.metadata.create_all(engine)  # crea la tabla solo si no existe

    with engine.connect() as conn:
        existentes = conn.execute(select(func.count()).select_from(Persona)).scalar()
    if existentes >= TOTAL:
        print(f"La tabla ya tiene {existentes} registros. No se inserta nada.")
        return

    print("Generando datos con Faker...")
    datos = generar_personas(TOTAL)
    insertar(engine, datos)
    print("Listo: 100000 registros insertados en personas_juan")


if __name__ == "__main__":
    main()
