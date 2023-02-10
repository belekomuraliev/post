from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from post import views

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

]
