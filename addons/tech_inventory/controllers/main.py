import json
from odoo import http
from odoo.http import request

class TechFlowApiController(http.Controller):

    # GET Consultar empleados con sus equipos asignados
    @http.route('/api/employees/equipments', type='http', auth='public', methods=['GET'], csrf=False)
    def get_employees_equipments(self, **kwargs):
        """Devuelve la lista de empleados junto con los equipos que tienen asignados."""
        employees = request.env['hr.employee'].sudo().search([])
        result = []

        for emp in employees:
            equipments_data = []
            for eq in emp.equipment_ids:
                equipments_data.append({
                    'id': eq.id,
                    'name': eq.name,
                    'serial': eq.serial,
                    'category': eq.category_id.name if eq.category_id else None,
                    'state': eq.state,
                    'cost': eq.cost,
                })

            result.append({
                'employee_id': emp.id,
                'name': emp.name,
                'job_title': emp.job_title or 'Sin puesto asignado',
                'work_email': emp.work_email or 'Sin correo',
                'equipment_count': emp.equipment_count,
                'assigned_equipments': equipments_data
            })

        return request.make_json_response({'status': 'success', 'data': result})

    # GET Consultar las órdenes de reparación registradas
    @http.route('/api/repairs', type='http', auth='public', methods=['GET'], csrf=False)
    def get_repairs(self, **kwargs):
        """Devuelve la lista de órdenes de reparación del módulo tech_repair."""
        repairs = request.env['tech.repair'].sudo().search([])
        result = []

        for rep in repairs:
            result.append({
                'repair_id': rep.id,
                'code': rep.name,
                'equipment_id': rep.equipment_id.id,
                'equipment_name': rep.equipment_id.name,
                'serial': rep.serial,
                'category': rep.category_id.name if rep.category_id else None,
                'technician': rep.technician_id.name if rep.technician_id else None,
                'description': rep.description,
                'cost': rep.cost,
                'date_request': str(rep.date_request) if rep.date_request else None,
                'date_close': str(rep.date_close) if rep.date_close else None,
                'state': rep.state,
            })

        return request.make_json_response({'status': 'success', 'data': result})

    # POST Asignar o desasignar un equipo a un empleado
    @http.route('/api/equipments/assign', type='http', auth='public', methods=['POST'], csrf=False)
    def assign_equipment(self, **kwargs):
        """Modifica la asignación de un equipo tecnológico."""
        try:
            data = json.loads(request.httprequest.data or '{}')
            equipment_id = data.get('equipment_id')
            employee_id = data.get('employee_id')

            if not equipment_id:
                return request.make_json_response({'status': 'error', 'message': 'equipment_id es obligatorio'}, status=400)

            equipment = request.env['tech.equipment'].sudo().browse(equipment_id)
            if not equipment.exists():
                return request.make_json_response({'status': 'error', 'message': 'Equipo no encontrado'}, status=404)

            # Si envían employee_id, asignamos; si envían null, desasignamos
            if employee_id:
                employee = request.env['hr.employee'].sudo().browse(employee_id)
                if not employee.exists():
                    return request.make_json_response({'status': 'error', 'message': 'Empleado no encontrado'}, status=404)
                equipment.write({'employee_id': employee.id, 'state': 'assigned'})
                msg = f"Equipo '{equipment.name}' asignado exitosamente a '{employee.name}'"
            else:
                equipment.action_set_available()
                msg = f"Equipo '{equipment.name}' liberado y marcado como disponible"

            return request.make_json_response({
                'status': 'success',
                'message': msg,
                'equipment': {
                    'id': equipment.id,
                    'name': equipment.name,
                    'state': equipment.state,
                    'employee_id': equipment.employee_id.id if equipment.employee_id else None
                }
            })
        except Exception as e:
            return request.make_json_response({'status': 'error', 'message': str(e)}, status=500)

    # POST Modificar el estado de una reparación
    @http.route('/api/repairs/update_status', type='http', auth='public', methods=['POST'], csrf=False)
    def update_repair_status(self, **kwargs):
        """Modifica el flujo de una orden de reparación llamando a sus métodos de negocio."""
        try:
            data = json.loads(request.httprequest.data or '{}')
            repair_id = data.get('repair_id')
            action = data.get('action')  # 'start', 'done', 'cancel'

            if not repair_id or not action:
                return request.make_json_response({'status': 'error', 'message': 'repair_id y action son obligatorios'}, status=400)

            repair = request.env['tech.repair'].sudo().browse(repair_id)
            if not repair.exists():
                return request.make_json_response({'status': 'error', 'message': 'Orden de reparación no encontrada'}, status=404)

            if action == 'start':
                repair.action_start_repair()
            elif action == 'done':
                repair.action_set_done()
            elif action == 'cancel':
                repair.action_cancel()
            else:
                return request.make_json_response({'status': 'error', 'message': "Acción inválida. Use: 'start', 'done' o 'cancel'"}, status=400)

            return request.make_json_response({
                'status': 'success',
                'message': f"Orden '{repair.name}' actualizada a estado '{repair.state}'",
                'repair': {
                    'id': repair.id,
                    'code': repair.name,
                    'state': repair.state,
                    'equipment_state': repair.equipment_id.state
                }
            })
        except Exception as e:
            return request.make_json_response({'status': 'error', 'message': str(e)}, status=500)