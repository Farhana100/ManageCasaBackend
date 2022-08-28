from venv import create
from django.urls import path
from .views import *

urlpatterns = [
    path('getFundInfo/<str:username>', getFundInfo, name = 'getFundInfo'),
    path('updateCharge/<str:username>', updateCharge, name = 'updateCharge'),
    path('getExpenseInfo/<str:username>', getExpenseInfo, name = 'getExpenseInfo'),
    path('addExpense/<str:username>', addExpense, name = 'addExpense'),
    path('stripeCheckoutSession', stripeCheckoutSession, name = 'stripeCheckoutSession'),
    path('getDues/<int:id>', getDues, name = 'getDues'),
    path('duesPayment', duesPayment, name = 'duesPayment'),
    path('getPayments/<int:id>', getPayments, name='getPayments'),
]

