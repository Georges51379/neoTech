from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from my_app.views import ClientTransactionsView, welcome_view

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('api/clients/<str:client_id>/transactions/', ClientTransactionsView.as_view(), name='client-transactions'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
