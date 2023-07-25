from django.urls import include, path, re_path
# from api import context_processors
from . import views
# from . import context_processors


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

app_name = "postman"

urlpatterns = [
#    path('message_id=<str:message_id>&contact=<str:contact>/', views.webpage, name='webpage'),

    path('', views.index, name="index"),
    path('client_id=<str:client_id>/', views.dashboard, name="dashboard"),
    path('create-service-type/', views.createServiceType, name="createServiceType"),
    path('view-service-types/', views.viewServiceTypes, name="viewServiceTypes"),
    path('edit-service-type/<int:id>', views.editServiceType, name='editServiceType'),
    path('delete-service-type/<int:id>', views.deleteServiceType, name='deleteServiceType'),

]