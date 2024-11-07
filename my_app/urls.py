from django.urls import path
from .views import ClientTransactionsView

urlpatterns = [
    path('clients/<str:client_id>/transactions/', ClientTransactionsView.as_view(), name='client-transactions'),
]
