from django.urls import path
from core.erp.views.category.views import *
from core.erp.views.timelimit.views import *
from core.erp.views.sucursal.views import *
from core.erp.views.client.views import *
from core.erp.views.provider.views import *
from core.erp.views.dashboard.views import *
from core.erp.views.product.views import *
from core.erp.views.sale.views import *
from core.erp.views.purchase.views import *
from core.erp.views.tests.views import TestView
from core.erp.views.transfer.views import *
from core.erp.views.operation.views import *

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
    # product
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
    # purchase
    path('purchase/list/', PurchaseListView.as_view(), name='purchase_list'),
    path('purchase/add/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('purchase/delete/<int:pk>/', PurchaseDeleteView.as_view(), name='purchase_delete'),
    path('purchase/update/<int:pk>/', PurchaseUpdateView.as_view(), name='purchase_update'),
    path('purchase/invoice/pdf/<int:pk>/', PurchaseInvoicePdfView.as_view(), name='purchase_invoice_pdf'),
    #path('purchase/update/state/<int:pk>/', PurchaseDeleteView.as_view(), name='purchase_update_state'),

]
