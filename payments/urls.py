from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import *

urlpatterns = [
    path('', View_Order_Page, name='order'),
    path('confirm_order', View_Create_Order, name = 'create_order'),
    path('payment_status', View_Payment_Status, name = 'payment_status'),
    # path('payments/', include('payments.urls')),
]
