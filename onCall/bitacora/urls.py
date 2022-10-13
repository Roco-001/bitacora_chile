from django.urls import path
from . import views
from .views import IncidenciaListView, IncidenciaCreate, IncidenciaUpdate, IncidenciaDelete, IncidenciaHijoCreate, IncidenciaHijoDelete, IncidenciahijoUpdate, IncidenciaHijoDetailView, IncidenciaCerradasListView



app_name= 'bitacora'
urlpatterns = [
	path('', views.bitacora, name="home"),
	path('bitacora_list/', IncidenciaListView.as_view(), name="incidencia_list"),
	path('create/', views.create_bitacora, name='incidencia_create'),
	path('update/<int:pk>', IncidenciaUpdate.as_view(), name='incidencia_update'),
	path('delete/<int:pk>', IncidenciaDelete.as_view(), name='incidencia_delete'),
	path('detail/<int:pk>', IncidenciaHijoCreate.as_view(), name='incidencia_detail'),

	path('incidenciaHijo/update/<int:pk>', IncidenciahijoUpdate.as_view(), name='incidenciaHijo_update'),
	path('incidenciaHijo/delete/<int:pk>', IncidenciaHijoDelete.as_view(), name='incidenciaHijo_delete'),

	path('incidenciaHijo/<int:pk>/', IncidenciaHijoDetailView.as_view(), name='incidenciaHijo_detail'),

	path('download_csv/', views.export_csv, name="export_csv"),
	path('download_csv_cerradas/', views.export_csv_cerradas, name="export_csv_cerradas"),

	path('bitacora_list_cerradas/', IncidenciaCerradasListView.as_view(), name="incidencia_list_cerradas"),


]