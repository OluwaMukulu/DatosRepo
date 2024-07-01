from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path('registerpage/', views.registerpage, name='registerpage'),
    path('logoutpage/', views.logoutpage, name='logoutpage'),
    path('listexpenses/', views.listexpenses, name='listexpenses'),
    path('addexpenses/', views.addexpenses, name='addexpenses'),
    path('updateexpenses/<str:pk>/', views.updateexpenses, name='updateexpenses'),
    path('deleteexpense/<str:pk>/', views.deleteexpense, name='deleteexpense'),
    path('listincome/', views.listincome, name='listincome'),
    path('addincome/', views.addincome, name='addincome'),
    path('updateincome/<str:pk>/', views.updateincome, name='updateincome'),
    path('deleteincome/<str:pk>/', views.deleteincome, name='deleteincome'),
    path('invoice/', views.invoice, name='invoice'),
    path("listIncome/", views.listIncome, name="listIncome"),
    path("listExpense/", views.listExpense, name="listExpense"),
]