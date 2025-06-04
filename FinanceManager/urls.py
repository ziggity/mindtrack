from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('categories/<str:transaction_type>/', views.get_categories, name='get_categories'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    
]