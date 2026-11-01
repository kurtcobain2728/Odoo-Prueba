{
    'name': 'TechFlow - Reparaciones y Mantenimiento',
    'version': '1.0.0',
    'category': 'Inventory/Repair',
    'summary': 'Gestión de órdenes de reparación para equipos tecnológicos',
    'description': """
        Módulo para registrar y controlar las reparaciones y mantenimientos
        de los equipos tecnológicos gestionados en TechFlow Inventory.
    """,
    'author': 'Argenis Torrealba',
    'website': 'https://techflow.com',
    'depends': ['base', 'mail', 'tech_inventory'],
    'data': [
        'security/ir.model.access.csv',
        'views/tech_repair_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}