"""magic_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the 'include()' function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from ads import views
from rest_framework import routers
from ads.views import LocationsViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.SimpleRouter()
router.register('location', LocationsViewSet)

urlpatterns = [
    # ads
    path("ad/", views.AdListView.as_view(), name="ads"),
    path("ad/<int:pk>/", views.ad_detail_view, name="ad"),
    path("ad/create/", views.AdCreateView.as_view(), name="new_ad"),
    path("ad/<int:pk>/update/", views.AdUpdateView.as_view(), name="update_ad"),
    path("ad/<int:pk>/delete/", views.AdDeleteView.as_view(), name="delete_ad"),
    path("ad/<int:pk>/upload_image/", views.AdImageView.as_view(), name="add_img"),

    # categories
    path("cat/", views.CategoryListView.as_view(), name="cats"),
    path("cat/<int:pk>/", views.CategoryDetailView.as_view(), name="cat"),
    path("cat/create/", views.CategoryCreateView.as_view(), name="new_cat"),
    path("cat/<int:pk>/update/", views.CategoryUpdateView.as_view(), name="update_cat"),
    path("cat/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="delete_cat"),

    # users
    path("user/", views.UserListView.as_view(), name="users"),
    path("user/<int:pk>/", views.UserDetailView.as_view(), name="user"),
    path("user/create/", views.UserCreateView.as_view(), name="new_user"),
    path("user/<int:pk>/update/", views.UserUpdateView.as_view(), name="update_user"),
    path("user/<int:pk>/delete/", views.UserDeleteView.as_view(), name="delete_user"),
    path('user/token/', TokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),

    # selections
    path("selection/", views.SelectionListView.as_view(), name="sets"),
    path("selection/<int:pk>/", views.SelectionDetailView.as_view(), name="set"),
    path("selection/create/", views.SelectionCreateView.as_view(), name="new_set"),
    path("selection/<int:pk>/update/", views.SelectionUpdateView.as_view(), name="update_set"),
    path("selection/<int:pk>/delete/", views.SelectionDeleteView.as_view(), name="delete_set"),
]

urlpatterns += router.urls
