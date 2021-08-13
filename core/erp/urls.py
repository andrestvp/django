from django.urls import path
from core.erp.views.category.views import *
from core.erp.views.timelimit.views import *
from core.erp.views.sucursal.views import *
from core.erp.views.client.views import *
from core.erp.views.provider.views import *
from core.erp.views.dashboard.views import *
from core.erp.views.product.views import *
from core.erp.views.sale.views import *
#from core.erp.views.purchase.views import *
from core.erp.views.purchaseOrder.views import *
from core.erp.views.tests.views import TestView
from core.erp.views.transfer.views import *
from core.erp.views.operation.views import *
from core.erp.views.payment.views import *
from core.erp.views.tax.views import *
from core.erp.views.grouprov.views import *
from core.erp.views.scrap.views import *
from core.erp.views.pricelist.views import *
from core.erp.views.serie.views import *
from core.erp.views.vendor.views import *
from core.erp.views.invoicing.views import *
from core.erp.views.prices.views import *
from core.erp.views.secuences.views import *
from core.erp.views.measures.views import *
from core.erp.views.creditcard.views import *
from core.erp.views.accounts.views import *
from core.erp.views.reception.views import *
from core.erp.views.expenses.views import *
from core.erp.views.financial.views import *
from core.erp.views.quotation.views import *
from core.erp.views.toinvoice.views import *
#from core.erp.views.solicitudCompra import *




from django.conf.urls import url


app_name = 'erp'

urlpatterns = [
    # category
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # timelimit
    path('timelimit/list/', TimelimitListView.as_view(), name='timelimit_list'),
    path('timelimit/add/', TimelimitCreateView.as_view(), name='timelimit_create'),
    path('timelimit/update/<int:pk>/', TimelimitUpdateView.as_view(), name='timelimit_update'),
    path('timelimit/delete/<int:pk>/', TimelimitDeleteView.as_view(), name='timelimit_delete'),
    #sucursal
    path('sucursal/list/', SucursalListView.as_view(), name='sucursal_list'),
    path('sucursal/add/', SucursalCreateView.as_view(), name='sucursal_create'),
    path('sucursal/update/<int:pk>/', SucursalUpdateView.as_view(), name='sucursal_update'),
    path('sucursal/delete/<int:pk>/', SucursalDeleteView.as_view(), name='sucursal_delete'),
    # client
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # provider
    path('provider/list/', ProviderListView.as_view(), name='provider_list'),
    path('provider/add/', ProviderCreateView.as_view(), name='provider_create'),
    path('provider/update/<int:pk>/', ProviderUpdateView.as_view(), name='provider_update'),
    path('provider/delete/<int:pk>/', ProviderDeleteView.as_view(), name='provider_delete'),
    # product mod
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
     # Transfers
    path('transfer/list/', TransferListView.as_view(), name='transfer_list'),
    path('transfer/add/', TransferCreateView.as_view(), name='transfer_create'),
    path('transfer/update/<int:pk>/', TransferUpdateView.as_view(), name='transfer_update'),
    path('transfer/delete/<int:pk>/', TransferDeleteView.as_view(), name='transfer_delete'),
     #Operations
    path('operation/list/', OperacionesListView.as_view(), name='operation_list'),
    path('operation/add/', OperacionesCreateView.as_view(), name='operation_create'),
    path('operation/update/<int:pk>/', OperacionesUpdateView.as_view(), name='operation_update'),
    path('operation/delete/<int:pk>/', OperacionesDeleteView.as_view(), name='operation_delete'),
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # test
    path('test/', TestView.as_view(), name='test'),
    # sale
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    #path('sale/invoice/pdf/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),

    # quotation
    path('quotation/list/', QuotationSaleListView.as_view(), name='quotation_list'),
    path('quotation/add/', QuotationSaleCreateView.as_view(), name='quotation_create'),
    path('quotation/delete/<int:pk>/', QuotationSaleDeleteView.as_view(), name='quotation_delete'),
    path('quotation/update/<int:pk>/', QuotationSaleUpdateView.as_view(), name='quotation_update'),
    path('quotation/invoice/pdf/<int:pk>/', QuotationSaleInvoicePdfView.as_view(), name='quotation_invoice_pdf'),

    # toinvoice
    path('toinvoice/list/', ToInvoiceSaleListView.as_view(), name='toinvoice_list'),
    path('toinvoice/add/', ToInvoiceSaleCreateView.as_view(), name='toinvoice_create'),
    path('toinvoice/delete/<int:pk>/', ToInvoiceSaleDeleteView.as_view(), name='toinvoice_delete'),
    path('toinvoice/update/<int:pk>/', ToInvoiceSaleUpdateView.as_view(), name='toinvoice_update'),
    path('toinvoice/invoice/pdf/<int:pk>/', ToInvoiceSaleInvoicePdfView.as_view(), name='toinvoice_invoice_pdf'),

    # purchase
    #path('purchase/list/', PurchaseListView.as_view(), name='purchase_list'),
    #path('purchase/add/', PurchaseCreateView.as_view(), name='purchase_create'),
    #path('purchase/delete/<int:pk>/', PurchaseDeleteView.as_view(), name='purchase_delete'),
    #path('purchase/update/<int:pk>/', PurchaseUpdateView.as_view(), name='purchase_update'),
    #path('purchase/invoice/pdf/<int:pk>/', PurchaseInvoicePdfView.as_view(), name='purchase_invoice_pdf'),

   #path('solicitudCompra/list/', PedidosCompraListView.as_view(), name = 'solicitudCompra_list'),
   #path('solicitudCompra/add/', PedidosCompraCreateView.as_view(), name = 'solicitudCompra_create'), 
   #path('solicitudCompra/solicitud/pdf/<int:pk>/', PedidoCompraInvoicePdfView.as_view(), name='solicitudCompra_invoice_pdf'),


   #path('solicitudCompra/list/', PedidosCompraListView.as_view(), name = 'solicitudCompra_list'),
   #path('solicitudCompra/add/', PedidosCompraCreateView.as_view(), name = 'solicitudCompra_create'), 
   #path('solicitudCompra/solicitud/pdf/<int:pk>/', PedidoCompraInvoicePdfView.as_view(), name='solicitudCompra_invoice_pdf'),


    # payment
    path('payment/list/', PaymentListView.as_view(), name='payment_list'),
    path('payment/add/', PaymentCreateView.as_view(), name='payment_create'),
    path('payment/update/<int:pk>/', PaymentUpdateView.as_view(), name='payment_update'),
    path('payment/delete/<int:pk>/', PaymentDeleteView.as_view(), name='payment_delete'),
    # tax
    path('tax/list/', TaxListView.as_view(), name='tax_list'),
    path('tax/add/', TaxCreateView.as_view(), name='tax_create'),
    path('tax/update/<int:pk>/', TaxUpdateView.as_view(), name='tax_update'),
    path('tax/delete/<int:pk>/', TaxDeleteView.as_view(), name='tax_delete'),
     # grupo proveedores
    path('grouprov/list/', GrouprovListView.as_view(), name='grouprov_list'),
    path('grouprov/add/', GrouprovCreateView.as_view(), name='grouprov_create'),
    path('grouprov/update/<int:pk>/', GrouprovUpdateView.as_view(), name='grouprov_update'),
    path('grouprov/delete/<int:pk>/', GrouprovDeleteView.as_view(), name='grouprov_delete'),

   # pricelist
    path('priceList/list/', PriceListListView.as_view(), name='pricelist_list'),
    path('priceList/add/', PriceListCreateView.as_view(), name='pricelist_create'),
    path('priceList/update/<int:pk>/', PriceListUpdateView.as_view(), name='pricelist_update'),
    path('priceList/delete/<int:pk>/', PriceListDeleteView.as_view(), name='pricelist_delete'),
     #  scrap
    path('scrap/list/', ScrapListView.as_view(), name='scrap_list'),
    path('scrap/add/', ScrapCreateView.as_view(), name='scrap_create'),
    path('scrap/update/<int:pk>/', ScrapUpdateView.as_view(), name='scrap_update'),
    path('scrap/delete/<int:pk>/', ScrapDeleteView.as_view(), name='scrap_delete'),

     #  serie
    path('serie/list/', SerieListView.as_view(), name='serie_list'),
    path('serie/add/', SerieCreateView.as_view(), name='serie_create'),
    path('serie/update/<int:pk>/', SerieUpdateView.as_view(), name='serie_update'),
    path('serie/delete/<int:pk>/', SerieDeleteView.as_view(), name='serie_delete'),

    # vendor
    path('vendor/list/', VendorListView.as_view(), name='vendor_list'),
    path('vendor/add/', VendorCreateView.as_view(), name='vendor_create'),
    path('vendor/update/<int:pk>/', VendorUpdateView.as_view(), name='vendor_update'),
    path('vendor/delete/<int:pk>/', VendorDeleteView.as_view(), name='vendor_delete'),

    # invoicing
    path('invoicing/list/', InvoicingListView.as_view(), name='invoicing_list'),
    path('invoicing/add/', InvoicingCreateView.as_view(), name='invoicing_create'),
    path('invoicing/update/<int:pk>/', InvoicingUpdateView.as_view(), name='invoicing_update'),
    path('invoicing/delete/<int:pk>/', InvoicingDeleteView.as_view(), name='invoicing_delete'),

    # secuences
    path('secuences/list/', SecuencesListView.as_view(), name='secuences_list'),
    path('secuences/add/', SecuencesCreateView.as_view(), name='secuences_create'),
    path('secuences/update/<int:pk>/', SecuencesUpdateView.as_view(), name='secuences_update'),
    path('secuences/delete/<int:pk>/', SecuencesDeleteView.as_view(), name='secuences_delete'),



   # measures
   path('measures/list/', MeasuresListView.as_view(), name='measures_list'),
   path('measures/add/', MeasuresCreateView.as_view(), name='measures_create'),
   path('measures/update/<int:pk>/', MeasuresUpdateView.as_view(), name='measures_update'),
   path('measures/delete/<int:pk>/', MeasuresDeleteView.as_view(), name='measures_delete'),

 # creditcard
   path('creditcard/list/', CreditCardListView.as_view(), name='creditcard_list'),
   path('creditcard/add/', CreditCardCreateView.as_view(), name='creditcard_create'),
   path('creditcard/update/<int:pk>/', CreditCardUpdateView.as_view(), name='creditcard_update'),
   path('creditcard/delete/<int:pk>/', CreditCardDeleteView.as_view(), name='creditcard_delete'),

# payment
   path('accounts/list/', PlanCuentasListView.as_view(), name='accounts_list'),
   path('accounts/add/', PlanCuentasCreateView.as_view(), name='accounts_create'),
   path('accounts/update/<int:pk>/', PlanCuentasUpdateView.as_view(), name='accounts_update'),
   path('accounts/delete/<int:pk>/', PlanCuentasDeleteView.as_view(), name='accounts_delete'),




# recepcioncompra
   path('reception/list/', RecepcionCompraListView.as_view(), name='reception_list'),
   path('reception/add/', RecepcionCompraCreateView.as_view(), name='reception_create'),
   path('reception/update/<int:pk>/', RecepcionCompraUpdateView.as_view(), name='reception_update'),
   path('reception/delete/<int:pk>/', RecepcionCompraDeleteView.as_view(), name='reception_delete'),

# expenses
   path('expenses/list/', GastosListView.as_view(), name='expenses_list'),
   path('expenses/add/', GastosCreateView.as_view(), name='expenses_create'),
   path('expenses/update/<int:pk>/', GastosUpdateView.as_view(), name='expenses_update'),
   path('expenses/delete/<int:pk>/', GastosDeleteView.as_view(), name='expenses_delete'),

# financial
   path('financial/list/', FinancieroPagosListView.as_view(), name='financial_list'),
   path('financial/add/', FinancieroPagosCreateView.as_view(), name='financial_create'),
   path('financial/update/<int:pk>/', FinancieroPagosUpdateView.as_view(), name='financial_update'),
   path('financial/delete/<int:pk>/', FinancieroPagosDeleteView.as_view(), name='financial_delete'),



# tariff
  #  path('tariff/list/', TariffListView.as_view(), name='tariff_list'),
   # path('tariff/add/', TariffCreateView.as_view(), name='tariff_create'),
   # path('tariff/update/<int:pk>/', TariffUpdateView.as_view(), name='tariff_update'),
   # path('tariff/delete/<int:pk>/', TariffDeleteView.as_view(), name='tariff_delete'),
 
]
