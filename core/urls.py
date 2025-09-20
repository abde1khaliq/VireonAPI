from django.urls import path
from .views import *

urlpatterns = [
    path('', interface_view, name='interface-page'),
    path('vireon-docs/', documentation_view, name='docs-page'),
    path('dashboard/', dashboard_view, name='dashboard-page'),
    
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('create-api-key/', create_api_key_modal, name='create_api_key_modal'),
]