# 📡 TechFlow IT - Documentación de la API REST

Esta API REST permite a sistemas externos (aplicaciones móviles, dashboards en React, microservicios o herramientas como Postman) consultar y gestionar los activos tecnológicos y las órdenes de reparación de **TechFlow Odoo 18**.

* **Base URL:** `http://localhost:8069`
* **Formato:** `JSON` (Content-Type: application/json)
* **Autenticación:** Pública / Sesión web (`auth='public'`)

---

## 📌 Resumen de Endpoints Disponibles

| Método | Endpoint | Descripción |
| :---: | :--- | :--- |
| **`GET`** | `/api/employees/equipments` | Consulta la lista de empleados y los equipos que tienen asignados. |
| **`GET`** | `/api/repairs` | Consulta todas las órdenes de reparación y mantenimiento registradas. |
| **`POST`** | `/api/equipments/assign` | Asigna un equipo a un empleado o lo libera para dejarlo disponible. |
| **`POST`** | `/api/repairs/update_status` | Actualiza el flujo de una reparación (`start`, `done`, `cancel`). |

---

## 1. Consultar Empleados y sus Equipos Asignados

Devuelve la lista completa de empleados registrados en Recursos Humanos (`hr.employee`), junto con la cantidad y el detalle de los equipos que tienen bajo su custodia.

* **URL:** `GET /api/employees/equipments`
* **Método:** `GET`
* **Parámetros:** Ninguno

### Ejemplo con cURL:
```bash
curl -X GET http://localhost:8069/api/employees/equipments
```

### Respuesta Exitosa (`200 OK`):
```json
{
  "status": "success",
  "data": [
    {
      "employee_id": 2,
      "name": "Argenis Torrealba",
      "job_title": "Desarrollador",
      "work_email": "argenistorrealba28112001@gmail.com",
      "equipment_count": 3,
      "assigned_equipments": [
        {
          "id": 8,
          "name": "Dell Latitude E5470",
          "serial": "PGL-3450",
          "category": "Laptops",
          "state": "assigned",
          "cost": 100.0
        },
        {
          "id": 9,
          "name": "Dell OptiPlex 7090",
          "serial": "OPT-2024-11223344",
          "category": "Desktop",
          "state": "assigned",
          "cost": 850.0
        },
        {
          "id": 11,
          "name": "Cisco Catalyst 9200",
          "serial": "CSCO-2024-99001122",
          "category": "Redes y Telecomunicaciones",
          "state": "assigned",
          "cost": 2100.0
        }
      ]
    }
  ]
}
```

---

## 2. Consultar Órdenes de Reparación

Devuelve todas las órdenes de reparación y servicio técnico registradas en el módulo `tech_repair`.

* **URL:** `GET /api/repairs`
* **Método:** `GET`
* **Parámetros:** Ninguno

### Ejemplo con cURL:
```bash
curl -X GET http://localhost:8069/api/repairs
```

### Respuesta Exitosa (`200 OK`):
```json
{
  "status": "success",
  "data": [
    {
      "repair_id": 1,
      "code": "Reparación de Laptop",
      "equipment_id": 8,
      "equipment_name": "Dell Latitude E5470",
      "serial": "PGL-3450",
      "category": "Laptops",
      "technician": "Administrator",
      "description": "La laptop se apaga sola después de un rato de uso y sufre sobrecalentamiento.",
      "cost": 50.0,
      "date_request": "2026-11-01",
      "date_close": "2026-11-01",
      "state": "in_progress"
    }
  ]
}
```

---

## 3. Asignar o Desasignar Equipos

Permite modificar la asignación de un activo tecnológico a un empleado. Si se envía `employee_id: null`, el equipo se desasigna automáticamente y vuelve a estado `Disponible`.

* **URL:** `POST /api/equipments/assign`
* **Método:** `POST`
* **Headers:** `Content-Type: application/json`

### Cuerpo de la Petición (Request Body):
```json
{
  "equipment_id": 10,
  "employee_id": 2
}
```
*(Para desasignar: enviar `"employee_id": null`)*

### Ejemplo con cURL:
```bash
curl -X POST http://localhost:8069/api/equipments/assign \
  -H "Content-Type: application/json" \
  -d '{"equipment_id": 10, "employee_id": 2}'
```

### Respuesta Exitosa (`200 OK`):
```json
{
  "status": "success",
  "message": "Equipo 'Monitor LG UltraWide 29\"' asignado exitosamente a 'Argenis Torrealba'",
  "equipment": {
    "id": 10,
    "name": "Monitor LG UltraWide 29\"",
    "state": "assigned",
    "employee_id": 2
  }
}
```

---

## 4. Modificar el Flujo de una Reparación

Permite cambiar el estado de una orden de reparación de forma segura ejecutando los métodos de negocio del modelo Odoo.

* **URL:** `POST /api/repairs/update_status`
* **Método:** `POST`
* **Headers:** `Content-Type: application/json`

### Acciones Disponibles (`action`):
* `"start"`: Inicia la reparación (Estado: `in_progress`) y sincroniza el equipo a `repair`.
* `"done"`: Finaliza la reparación (Estado: `done`), asigna fecha de cierre y devuelve el equipo a `available`.
* `"cancel"`: Cancela la orden (Estado: `cancelled`).

### Cuerpo de la Petición (Request Body):
```json
{
  "repair_id": 1,
  "action": "done"
}
```

### Ejemplo con cURL:
```bash
curl -X POST http://localhost:8069/api/repairs/update_status \
  -H "Content-Type: application/json" \
  -d '{"repair_id": 1, "action": "done"}'
```

### Respuesta Exitosa (`200 OK`):
```json
{
  "status": "success",
  "message": "Orden 'Reparación de Laptop' actualizada a estado 'done'",
  "repair": {
    "id": 1,
    "code": "Reparación de Laptop",
    "state": "done",
    "equipment_state": "available"
  }
}
```

