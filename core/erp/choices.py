gender_choices = (
    ('male','Masculino'),
    ('female','Femenino'),
)

state_sale = (
    ('Cotización','Cotización'),
    ('Pedido', 'Pedido'),
    ('A Facturar', 'A Facturar'),
    ('Facturación Completa', 'Facturación Completa'),
    ('Cancelada','Cancelada'),
)

tipo_pago = (
    ('Al Contado','Al Contado'),
    ('Crédito','Crédito'),
)

tipo_doc = (
    ('Ruc','Ruc'),
    ('Cédula','Cédula'),
    #('Pasaporte','Pasaporte'),
)


state_purchase = (
    ('Anulado','Anulado'),
    ('Por Aprobar','Por Aprobar'),
    ('aprobada', 'Aprobado'),
    ('asignar Series','Asignar Series'),
    ('Caducado','Caducado'),
    ('Cerrado','Cerrado'),
    ('Enviado','Enviado'),
    ('Rechazado','Rechazado'),
    ('Registrado','Registrado'),
    ('Recibido','Recibido')
)

ret_iva = (
    ('1','Ninguno'),
    ('2','721 10 % Retención Iva'),
    ('3','723 20 % Retención Iva'),
    ('4','725 30 % Retención Iva'),
    ('5','727 50 % Retención Iva'),
    ('6','729 70 % Retención Iva'),
    ('7','731 100 % Retención Iva'),
    ('8','7 0 % Retención Iva en cero'),
    ('9','8 0 % No procede Retención'),


)

Ciudades = (

    ('Balao', 'Balao'),
    ('Balzar','Balzar'),
    ('Colimes', 'Colimes'),
    ('Daule', 'Daule'),
    ('Duran', 'Duran'),
    ('El Empalme', 'El Empalme'),
    ('El Triunfo', 'El triunfo'),
    ('Guayaquil', 'Guayaquil'),
    ('Milagro', 'Milagro'),
    ('Naranjal', 'Naranjal'),
    ('Naranjito', 'Naranjito'),
    ('Quevedo', 'Quevedo'),
    ('Palestina', 'Palestina'),
    ('Pedro Carbo','Pedro Carbo'),
    ('Playas','Playas'),
    ('Samborondon','Samborondon'),
    ('Yaguachi','Yaguachi'),
    ('Santa Lucia','Santa Lucia'),
    ('Santa Elena', 'Santa Elena'),

)
#-----------------------------------------------------------------------------------
Rutas =(
     ('Todas las Rutas','Todas las rutas'),
     ('General','General')
 )

#---------------------------------------------------------------------------------------------------
Zonas=(
     ('Todas las Zonas','Todas las Zonas'),
     ('Zona General','Zona General')

 )

#----------------------------------------------------------------------------------------------------
EstadoGastos=(
('Activo','Activo'),
('Inactivo','Inactivo'), 
('Bien','Bien'),
('Servicio', 'Servicio'), 
 )
#----------------------------------------------------------------------------------------------------
Documentos=(
 ('Factura','Factura'),
 )

Tributo =(
 ('00 Casos Especiales Cuyo Sustento No Aplica en las Opciones Anteriores','00 Casos Especiales Cuyo Sustento No Aplica en las Opciones Anteriores' ),
 ('01 Credito Tributario Para Declaraciones De IVA(Servicios y Bienes distintos de Inventarios y Activos Fijos )', '01 Credito Tributario Para Declaraciones De IVA(Servicios y Bienes distintos de Inventarios y Activos Fijos ' ),
 ('02 Costo o Gastos Para Declaracion de Ir(Servicios y Bienes Distintos de Inventario y Activos Fijos)', '02 Costo o Gastos Para Declaracion de Ir(Servicios y Bienes Distintos de Inventario y Activos Fijos)'),
 ('03 Activo Fijo-Credito Tributario para Declaraciones de IVA','03 Activo Fijo-Credito Tributario para Declaraciones de IVA' ),
 ('04 Activo Fijo-Costo o Gasto para Declaraciones de Ir', '04 Activo Fijo-Costo o Gasto para Declaraciones de Ir'),
 ('05 Liquidación Gastos De Viaje, Hospedaje Y Alimentación Gastos Ir (A Nombre De Empleados Y No De La Empresa)', '05 Liquidación Gastos De Viaje, Hospedaje Y Alimentación Gastos Ir (A Nombre De Empleados Y No De La Empresa)'),
 ('06 Inventario - Crédito Tributario Para Declaraciones De IVA', '06 Inventario - Crédito Tributario Para Declaraciones De IVA'),
 ('07 Inventario - Costos O Gastos Para Declaración De Ir','07 Inventario - Costos O Gastos Para Declaración De Ir'),
 ('08 Valor Pagado Para Solicitar Reembolso De Gasto (Intermediario)', '08 Valor Pagado Para Solicitar Reembolso De Gasto (Intermediario)'),
 ('09 Reembolso Por Siniestros','09 Reembolso Por Siniestros'),
 ('10 Distribución De Dividendos, Beneficios, Utilidades', '10 Distribución De Dividendos, Beneficios, Utilidades'),
 ('11 Convenio De Débito O Recaudación Para Ifis', '11 Convenio De Débito O Recaudación Para Ifis'),
 ('12 Impuestos Y Retenciones Presuntivos', '12 Impuestos Y Retenciones Presuntivos'),
 ('13 Valores Reconocidos Por Entidades Del Sector Público A Favor De Sujetos Pasivos', '13 Valores Reconocidos Por Entidades Del Sector Público A Favor De Sujetos Pasivos'),
 ('14 Valores Facturados Por Socios A Operadoras De Transporte (Que No Constituyen Gastos De Dicha Operadora)', '14 Valores Facturados Por Socios A Operadoras De Transporte (Que No Constituyen Gastos De Dicha Operadora)'),
 )



Movimiento=(
 ('Protesto Cheque','Protesto Cheque'),
 ('Saldo Inicial Pagos','Saldo Inicial Pagos')
 )

CentroCostos=(
   ('C001 Centro Costo Matriz','C001 Centro Costo Matriz') ,
   ('C002 Centro Costo Prosperina','C002 Centro Costo Prosperina'),
   ('C003 Centro Costo Paraiso','C003 Centro Costo Paraiso'),
   ('C004 Centro Costo Santa Lucia','C004 Centro Costo Santa Lucia'),
   ('C005 Centro Costo San Francisco','C005 Centro Costo San Francisco'),
   ('C006 Centro Costo Santa Elena','C006 Centro Costo Santa Elena')
)

