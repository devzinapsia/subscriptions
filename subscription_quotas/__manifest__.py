{
    'name': 'Control de cuotas de suscripciones',
    'version': '19.0.2.0.0',
    'category': 'Sales/Subscriptions',
    'summary': 'Manejo de cuotas máximas, leyendas en facturación recurrente '
               'y cierre automático al facturar la última cuota',
    'author': 'Zinapsia',
    'website': 'https://www.zinapsia.com',
    'license': 'AGPL-3',
    'depends': ['sale_subscription'],
    'data': [
        'views/sale_subscription_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
