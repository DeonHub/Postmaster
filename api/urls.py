from django.urls import include, path, re_path
# from api import context_processors
from rest_framework import routers
from rest_framework import permissions
from . import views
# from . import context_processors

router = routers.DefaultRouter()

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Postmaster API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
   # path('', include(router.urls)),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

   # path('mail/message_id=<str:message_id>&contact=/', views.webpage, name='webpage'),

   path('websms/<str:message_id>/t=<str:contact>', views.viewWebmail, name="viewWebmail"),

   path('send-posts/', views.SendPosts.as_view(), name="sendPosts"),

   path('posts/client_id=<str:client_id>&branch=<str:branch>', views.GetPosts.as_view(), name="getPosts"),

   path('top-up/', views.TopUpCredit.as_view(), name="TopUpCredit"),
   path('add-credit/', views.AddCredit.as_view(), name="AddCredit"),

   path('contact-groups/', views.ContactGroup.as_view(), name="ContactGroup"),

   path('set-email-details/', views.SetEmailDetails.as_view(), name="SetEmailDetails"),

   path('balances/client_id=<str:client_id>&branch=<str:branch>', views.GetCredits.as_view(), name="GetCredits"),

   path('purchase-history/client_id=<str:client_id>&branch=<str:branch>', views.PurchaseHistory.as_view(), name="PurchaseHistory"),

   path('view-service-types/', views.ViewServiceTypes.as_view(), name="view_service_types"),


    # path('add-extra-report/', views.AddExtraWorkReport.as_view(), name="add_extra_report"),
    # path('extra-reports/', views.ExtraWorkReport.as_view(), name="extra_report"),

    # path('assigned-duties/', views.ViewAssignedTasks.as_view(), name="ViewAssignedTasks"),
    # path('member-duties/', views.MemberAssignedDuties.as_view(), name="MemberAssignedDuties"),

    # path('subjects/', views.GetSubjects.as_view(), name="subjects"), 


    re_path('swagger/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # path('list/<int:pk>', views.HeroDetails.as_view(), name="heros"),
    # path('members/', views.members, name="members"),
]