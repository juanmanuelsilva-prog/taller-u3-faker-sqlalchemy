# Taller U3 – Automatización de BD con Python, Faker y Git

Script en Python que se conecta a una base de datos MySQL local con SQLAlchemy,
crea la tabla `personas_juan` (si no existe) e inserta 100.000 registros falsos
generados con Faker (nombre, apellido, correo, fecha de nacimiento, ciudad,
dirección, teléfono y profesión).

## Requisitos
- Python 3.10+
- MySQL local en ejecución y una base de datos creada (por ejemplo `taller_u3`)

## Instalación
```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

## Configuración
Copia `.env.example` a `.env` y pon tus datos reales (el `.env` no se sube a Git):
```
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=taller_u3
```

## Ejecución
```bash
python main.py
```

## Verificación
En DBeaver:
```sql
SELECT COUNT(*) FROM personas_juan;
```
Debe devolver 100000.
