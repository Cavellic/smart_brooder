from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('feeding_time_table', views.timeTable, name='feeding_time_table'),
    path('egg_production', views.eggProduction, name='egg_production'),
    path('chicks_management', views.chicksManagement, name='chicks_management'),
    path('profile', views.userProfile, name='profile'),
    path('batch/<str:pk>', views.batchInfo, name='batch_info'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('add_new_batch/', views.create_chicks_management, name='add_new_batch'),
    path('chicks/<int:pk>/update/', views.update_chicks, name='update_chicks'),
    path('batch/delete/<int:pk>/', views.delete_chicks_management, name='delete_batch'),
]
