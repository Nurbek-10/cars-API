"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from cars.views import BrandListView, Model_authListView, CarListView, api_root, CarViewSet, CommentCreateView

router = DefaultRouter()
router.register('books', CarViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='Cars shop API',
        default_version='v1',
        description='My online-cars shop\'s API'
    ), public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('account.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/docs/', schema_view.with_ui()),
    path('', api_root),
    path('api/v1/brands/', BrandListView.as_view(), name='brand-list'),
    path('api/v1/models/', Model_authListView.as_view(), name='model_auth-list'),
    path('api/v1/comments/', CommentCreateView.as_view(), name="create-comment"),
    path('api/v1/cars/', CarListView.as_view(), name='car-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)