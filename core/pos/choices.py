payment_condition = (
    ('contado', 'Contado'),
    ('credito', 'Credito'),
)

payment_method = (
    ('efectivo', 'Efectivo'),
    ('tarjeta_debito_credito', 'Tarjeta de Debito / Credito'),
    ('efectivo_tarjeta', 'Efectivo y Tarjeta'),
)

voucher = (
    ('ticket', 'Ticket'),
    ('factura', 'Factura'),
)
state_request = (
    ('Enviado', 'Enviado'),
    ('Anulado', 'Anulado'),
)
vouchersol = (
    ('cotizacion', 'Cotización'),
)

state_sale = (
    ('cotizacion','Cotización'),
    ('pedido', 'Pedido'),   
)