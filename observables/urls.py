from django.urls import path, include
from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'observables', views.ObservableViewSet)
router.register(r'observable-value', views.ObservableValueViewSet, base_name='observable-value')


app_name="observables"
urlpatterns = [
    path(r'', views.ObservableListView.as_view(), name='observable_list'),
    path(r'add', views.CreateObservableView.as_view(), name='observable_add'),
    path(r'<pk>/<uuid>', views.ObservableDetailView.as_view(), name='observable_detail'),
    path(r'<pk>/<uuid>/edit', views.ObservableEditView.as_view(), name='observable_edit'),
    path(r'<pk>/<uuid>/delete', views.DeleteObservableView.as_view(), name='delete_observable'),
    path(r'search', include('haystack.urls')),
    path(r'observables_data', views.ObservableListViewJson.as_view(), name="observables_list_json"),

    path(r'api/', include(router.urls )),
] 
