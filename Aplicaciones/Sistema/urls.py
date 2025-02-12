from django.urls import path
from . import views

app_name = 'Sistema'

urlpatterns = [
    # URLs para páginas principales
    path('', views.inicio, name='inicio'),
    
    # URLs para Recetas
    path('recetas/', views.lista_recetas, name='recetas'),
    path('receta/nueva/', views.crear_receta, name='crear_receta'),
    path('receta/<int:pk>/', views.detalle_receta, name='detalle_receta'),
    path('receta/<int:pk>/editar/', views.editar_receta, name='editar_receta'),
    path('receta/<int:pk>/eliminar/', views.eliminar_receta, name='eliminar_receta'),

    
    # URLs para Ingredientes
    path('ingredientes/', views.lista_ingredientes, name='ingredientes'),
    path('ingrediente/nuevo/', views.crear_ingrediente, name='crear_ingrediente'),
    path('ingrediente/<int:pk>/editar/', views.editar_ingrediente, name='editar_ingrediente'),
    path('ingrediente/<int:pk>/eliminar/', views.eliminar_ingrediente, name='eliminar_ingrediente'),

    
    # URLs para Lugares de Origen
    path('lugares/', views.lista_lugares, name='lugares'),
    path('lugar/nuevo/', views.crear_lugar, name='crear_lugar'),
    path('lugar/<int:pk>/editar/', views.editar_lugar, name='editar_lugar'),
    path('lugar/<int:pk>/eliminar/', views.eliminar_lugar, name='eliminar_lugar'),
    
    # URLs para filtros y búsquedas
    path('recetas/dificultad/<str:dificultad>/', views.recetas_por_dificultad, name='recetas_por_dificultad'),

    path('recetas/origen/<int:origen_id>/', views.recetas_por_origen, name='recetas_por_origen'),
    
]