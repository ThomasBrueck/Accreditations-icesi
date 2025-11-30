# Sistema de Gestión de Acreditación Académica

Un sistema web desarrollado en Django para la gestión de procesos de acreditación académica, que permite la administración de reportes, factores, características y comentarios con un sistema de roles y permisos.

## 📋 Características Principales

- **Sistema de Usuarios y Roles**: Gestión de usuarios con roles específicos (acadi, program director, common)
- **Gestión de Reportes**: Creación, edición y administración de reportes de acreditación
- **Factores y Características**: Manejo detallado de factores con sus características asociadas
- **Sistema de Comentarios**: Comentarios con sistema de aprobación y revisión
- **Métricas de Integración**: Sistema automático de recolección y análisis de métricas de pruebas
- **Notificaciones**: Sistema de notificaciones y tareas asignadas
- **Documentos DOFA**: Generación automática de documentos de análisis DOFA
- **Dashboard Administrativo**: Panel de control con estadísticas y métricas

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.1.6, Python 3.12.3
- **Base de Datos**: 
  - PostgreSQL (Neon.tech) para producción
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Testing**: Django TestCase
- **Documentos**: python-docx para generación de documentos Word

## 📦 Instalación

### Prerrequisitos

- Realizar instalacion del requeriments.txt

```
pip install -r requeriments.txt
```

### Paso para ejecutar las pruebas

```
coverage run manage.py test --keepdb
```