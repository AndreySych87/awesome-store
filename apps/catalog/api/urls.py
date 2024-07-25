from django.urls import path, include
from rest_framework.routers import DefaultRouter

from catalog.api import resources


app_name = 'catalog'

router = DefaultRouter()

router.register(
        'products',
        resources.ProductModelViewSet,
        basename='products'
)
router.register(
    'params',
    resources.ParamViewSet,
    basename='params'
)

urlpatterns = (
    path(
        '',
        include(router.urls)
    ),
)
