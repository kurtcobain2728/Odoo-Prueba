from odoo import models, fields, api, _
from odoo.exceptions import UserError

class TechRepair(models.Model):
    _name = 'tech.repair'
    _description = 'Orden de Reparación y Mantenimiento'
    _order = 'id desc'

    name = fields.Char(
        string='Código de Reparación',
        required=True,
        copy=False,
        default='Nueva Reparación'
    )
    
    equipment_id = fields.Many2one(
        'tech.equipment',
        string='Equipo Tecnológico',
        required=True,
        ondelete='restrict'
    )

    category_id = fields.Many2one(
        related='equipment_id.category_id',
        string='Categoría',
        readonly=True,
        store=True
    )
    serial = fields.Char(
        related='equipment_id.serial',
        string='Número de Serie',
        readonly=True
    )

    technician_id = fields.Many2one(
        'res.users',
        string='Técnico Responsable',
        default=lambda self: self.env.user,
        required=True
    )
    
    description = fields.Text(
        string='Diagnóstico / Falla Reportada',
        required=True
    )
    solution = fields.Text(
        string='Solución Técnica Aplicada'
    )

    cost = fields.Monetary(
        string='Costo de Reparación',
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id
    )
    date_request = fields.Date(
        string='Fecha de Entrada',
        default=fields.Date.today,
        required=True
    )
    date_close = fields.Date(
        string='Fecha de Finalización',
        readonly=True
    )

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('in_progress', 'En Reparación'),
        ('done', 'Reparado'),
        ('cancelled', 'Cancelado')
    ], string='Estado', default='draft', required=True)

    def action_start_repair(self):
        """Inicia la reparación y cambia el equipo automáticamente a 'En Reparación'"""
        for record in self:
            record.state = 'in_progress'
            if record.equipment_id:
                record.equipment_id.action_set_repair()

    def action_set_done(self):
        """Finaliza la reparación y devuelve el equipo a 'Disponible'"""
        for record in self:
            record.write({
                'state': 'done',
                'date_close': fields.Date.today()
            })
            if record.equipment_id:
                record.equipment_id.action_set_available()

    def action_cancel(self):
        """Cancela la orden de reparación"""
        for record in self:
            record.state = 'cancelled'
            