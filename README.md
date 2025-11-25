# Sistema de Historias Clínicas (Medical Records System)

## Descripción

Sistema completo de gestión de historias clínicas médicas desarrollado con Django REST Framework. Este sistema permite la gestión integral de pacientes, procedimientos médicos, historias clínicas y instalaciones médicas.

## Módulos del Sistema

### 1. **Medical Services (Servicios Médicos)**
- **Especialidades Médicas (Specialty)**: Gestión de especialidades como Cardiología, Pediatría, etc.
- **Procedimientos Médicos (MedicalProcedure)**: Catálogo de procedimientos y servicios médicos con códigos, costos y duración.

### 2. **Medical Records (Historias Clínicas)**
- **MedicalRecord**: Historias clínicas de pacientes con información completa del paciente, diagnóstico, síntomas y observaciones.
- **MedicalRecordDetail**: Detalles de procedimientos realizados en cada historia clínica.

Estados de Historia Clínica:
- `DRAFT`: Borrador
- `IN_PROGRESS`: En Progreso
- `COMPLETED`: Completada
- `ARCHIVED`: Archivada

### 3. **Facilities (Instalaciones Médicas)**
- **MedicalFacility**: Gestión de clínicas, hospitales, laboratorios y centros de urgencias.

Tipos de Instalación:
- `CLINIC`: Clínica
- `HOSPITAL`: Hospital
- `LABORATORY`: Laboratorio
- `EMERGENCY`: Urgencias

### 4. **Users (Usuarios y Perfiles)**
- **DoctorProfile**: Perfiles extendidos para usuarios del sistema (médicos, enfermeros, administrativos).

Roles disponibles:
- `DOCTOR`: Médico
- `NURSE`: Enfermero/a
- `ADMIN`: Administrativo
- `RECEPTIONIST`: Recepcionista

## Endpoints Principales

### Autenticación
- `POST /api/auth/register/` - Registro de usuarios
- `POST /api/auth/login/` - Login (JWT)
- `POST /api/auth/refresh/` - Refresh token

### Catálogo Médico
- `GET/POST /api/specialties/` - Listar/crear especialidades
- `GET/PUT/DELETE /api/specialties/{id}/` - Detalle/actualizar/eliminar especialidad
- `GET/POST /api/procedures/` - Listar/crear procedimientos
- `GET/PUT/DELETE /api/procedures/{id}/` - Detalle/actualizar/eliminar procedimiento

### Historias Clínicas
- `GET/POST /api/medical-records/` - Listar/crear historias clínicas
- `GET/PUT/DELETE /api/medical-records/{id}/` - Detalle/actualizar/eliminar
- `POST /api/medical-records/{id}/add_procedure/` - Agregar procedimiento
- `POST /api/medical-records/{id}/complete/` - Completar historia clínica
- `POST /api/medical-records/{id}/archive/` - Archivar historia clínica

### Instalaciones Médicas
- `GET /api/facilities/list` - Listar instalaciones
- `POST /api/facilities` - Crear instalación
- `GET /api/facilities/{id}/` - Detalle de instalación
- `PUT /api/facilities/{id}/update` - Actualizar instalación
- `DELETE /api/facilities/{id}/delete` - Eliminar instalación

### Perfiles de Doctores
- `GET/POST /api/profiles/` - Listar/crear perfiles
- `GET /api/profiles/me/` - Obtener perfil del usuario actual
- `GET/PUT/DELETE /api/profiles/{id}/` - Detalle/actualizar/eliminar perfil

## Instalación y Configuración

### Requisitos
- Python 3.12+
- PostgreSQL
- virtualenv

### Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd billing_api
```

2. **Crear y activar entorno virtual**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias**
```bash
pip install django djangorestframework djangorestframework-simplejwt django-filter psycopg2-binary python-dotenv
```

4. **Configurar variables de entorno**
El archivo `.env` ya está configurado con:
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT

5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Ejecutar el servidor**
```bash
python manage.py runserver
```

El sistema estará disponible en `http://localhost:8000`

## Estructura del Proyecto

```
billing_api/
├── billing_api/          # Configuración principal
│   ├── settings.py       # Configuración de Django
│   ├── urls.py          # URLs principales
│   └── wsgi.py          # WSGI config
├── medical_services/    # Módulo de servicios médicos
│   ├── models/          # Specialty, MedicalProcedure
│   ├── serializers/     # Serializadores
│   └── views/           # ViewSets
├── medical_records/     # Módulo de historias clínicas
│   ├── models/          # MedicalRecord, MedicalRecordDetail
│   ├── serializers/     # Serializadores
│   ├── views/           # ViewSets
│   └── services/        # Lógica de negocio
├── facilities/          # Módulo de instalaciones médicas
│   ├── models/          # MedicalFacility
│   ├── serializers/     # Serializadores
│   └── views/           # Vistas
├── users/               # Módulo de usuarios
│   ├── models.py        # DoctorProfile
│   ├── serializers/     # Serializadores
│   └── views/           # ViewSets
└── manage.py
```

## Características Principales

### Seguridad
- Autenticación JWT
- Permisos basados en roles
- Validación de acceso a historias clínicas por doctor

### Funcionalidades Médicas
- Gestión completa de historias clínicas
- Registro de procedimientos realizados
- Catálogo de especialidades y procedimientos
- Gestión de instalaciones médicas
- Perfiles médicos con especialización

### API REST
- Filtrado y búsqueda avanzada
- Paginación
- Ordenamiento
- Validaciones completas

## Flujo de Trabajo

1. **Registro de Usuario**: Un usuario se registra en el sistema
2. **Creación de Perfil**: Se crea un perfil de doctor con rol y especialización
3. **Catálogo**: Se configuran especialidades y procedimientos médicos
4. **Historia Clínica**: Se crea una nueva historia clínica para un paciente
5. **Procedimientos**: Se agregan procedimientos realizados a la historia
6. **Completar**: Se completa la historia clínica asignando número de registro
7. **Archivo**: Se archiva la historia cuando ya no está activa

## Tecnologías Utilizadas

- **Django 5.2.7**: Framework web
- **Django REST Framework 3.16**: API REST
- **PostgreSQL**: Base de datos
- **JWT**: Autenticación
- **django-filter**: Filtrado avanzado

## Autor

Sistema desarrollado para la gestión integral de historias clínicas médicas.

## Licencia

Este proyecto es privado y confidencial.
