# modulos-libnamic-practica
Módulo backend para Licium que permite gestionar checklists internas y sus ítems, con CRUD automático, acciones de cierre/reapertura, marcado de tareas, vistas admin y control de permisos mediante grupos y ACL. Ideal para aprender paso a paso la creación de módulos.

## Descripción
Este proyecto está enfocado en trabajar con:

- Importación y exportación de módulos
- Separación de lógica en distintos archivos
- Uso de funciones reutilizables
- Organización básica de un proyecto en Node.js

## Estructura

```
modules
├─ asset_lending
│  ├─ data
│  │  ├─ acl_rules.yml
│  │  ├─ groups.yml
│  │  └─ ui_modules.yml
│  ├─ models
│  │  ├─ asset.py
│  │  ├─ loan.py
│  │  ├─ location.py
│  │  └─ __init__.py
│  ├─ services
│  │  ├─ lending.py
│  │  └─ __init__.py
│  ├─ views
│  │  ├─ menu.yml
│  │  └─ views.yml
│  ├─ __init__.py
│  └─ __manifest__.yaml
├─ community_events
│  ├─ data
│  │  ├─ acl_rules.yml
│  │  ├─ groups.yml
│  │  ├─ settings.yml
│  │  └─ ui_modules.yml
│  ├─ models
│  │  ├─ event.py
│  │  ├─ registration.py
│  │  ├─ session.py
│  │  └─ __init__.py
│  ├─ services
│  │  ├─ event.py
│  │  ├─ registration.py
│  │  ├─ session.py
│  │  └─ __init__.py
│  ├─ tests
│  │  └─ test_registration_service.py
│  ├─ views
│  │  ├─ menu.yml
│  │  └─ views.yml
│  ├─ __init__.py
│  └─ __manifest__.yaml
├─ feedback_moderation
│  ├─ data
│  │  ├─ acl_rules.yml
│  │  ├─ groups.yml
│  │  └─ ui_modules.yml
│  ├─ models
│  │  ├─ comment.py
│  │  ├─ suggestion.py
│  │  ├─ tag.py
│  │  └─ __init__.py
│  ├─ services
│  │  ├─ comment.py
│  │  ├─ suggestion.py
│  │  ├─ tag.py
│  │  ├─ tag_api.py
│  │  └─ __init__.py
│  ├─ tests
│  │  ├─ test_suggestion_states.py
│  │  └─ __init__.py
│  ├─ views
│  │  ├─ menu.yml
│  │  └─ views.yml
│  ├─ __init__.py
│  └─ __manifest__.yaml
└─ practice_checklist
   ├─ data
   │  ├─ acl_rules.yml
   │  ├─ groups.yml
   │  └─ ui_modules.yml
   ├─ i18n
   │  ├─ en.yml
   │  └─ es.yml
   ├─ models
   │  ├─ checklist.py
   │  ├─ __init__.py
   │  └─ __pycache__
   │     ├─ checklist.cpython-314.pyc
   │     └─ __init__.cpython-314.pyc
   ├─ services
   │  ├─ checklist.py
   │  ├─ checklist_override.py
   │  └─ __init__.py
   ├─ settings.yml
   ├─ test
   │  ├─ conftest.py
   │  ├─ test_service.py
   │  ├─ test_services.py
   │  └─ __init__.py
   ├─ views
   │  ├─ menu.yml
   │  └─ views.yml
   ├─ __init__.py
   ├─ __manifest__.yaml
   └─ __pycache__
      └─ __init__.cpython-314.pyc

```

## Funcionamiento de los módulos
Este proyecto se organiza en distintos niveles, donde cada uno introduce un módulo más complejo y completo dentro del sistema.

### - Nivel 1: Checklist
Módulo básico para introducir la estructura modular.

Funcionalidad principal:
- Crear y gestionar tareas simples
- Operaciones CRUD (crear, leer, actualizar, eliminar)
- Visualización en el panel de administración

Cómo funciona:
- Se definen modelos simples (tareas)
- Se crean vistas automáticas en el admin
- Se aplican permisos básicos (ACL)
- Se organiza el módulo con estructura estándar

### - Nivel 2: Asset_lending
Gestiona el préstamo de recursos internos.

Funcionalidad principal:
- Registro de recursos (portátiles, cámaras, etc.)
- Control de disponibilidad (available, loaned, maintenance)
- Gestión de préstamos con fechas de salida y devolución

Cómo funciona:
- Un recurso solo puede prestarse si está disponible
- Al hacer un préstamo (checkout), el recurso pasa a estado loaned
- Al devolverlo (return), vuelve a available
- También se puede marcar como en mantenimiento

