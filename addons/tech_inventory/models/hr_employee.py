from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    equipment_ids = fields.One2many(
        'tech.equipment',
        'employee_id',
        string='Equipos Asignados'
    )
    
    equipment_count = fields.Integer(
        string='Total de Equipos',
        compute='_compute_equipment_count'
    )

    @api.depends('equipment_ids')
    def _compute_equipment_count(self):
        for employee in self:
            employee.equipment_count = len(employee.equipment_ids)