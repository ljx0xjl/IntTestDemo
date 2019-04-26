from django.conf.urls import url
from super_table import views
from django.urls import path


urlpatterns = [
    # super_table interface:
    path('add/', views.add, name='add'),
    path('search_by_name/', views.search_by_name, name='search_by_name'),
]
