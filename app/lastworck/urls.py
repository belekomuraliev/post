from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from post import views

schema_view = get_schema_view(
    openapi.Info(
        title="Tips API",
        default_version='v0.1',
        description="API шпоргалка для интервью",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="boke74@mail.ru"),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/auth/token/', obtain_auth_token),
    path('api/register/', views.AuthorView.as_view()),
    path('api/post/', views.PostViewSet.as_view()),
    path('api/post/<int:post_id>/', views.PostUpdateRetrieveDestroyView.as_view()),
    path('api/post/<int:post_id>/score', views.MeanScoreCreateAPIView.as_view()),
    path('api/post/<int:post_id>/score/<int:pk>/', views.MeanScoreDetailRetUpDestroy.as_view()),
    path('api/post/<int:post_id>/comment/', views.CommentViewSet.as_view()),
    path('api/post/<int:post_id>/comment/<int:comment_id>/', views.CommentRetrieveDestroyUpdateView.as_view()),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_ui'),

]
