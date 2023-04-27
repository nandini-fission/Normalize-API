from django.urls import path, include
from rest_framework import routers

from .views import CompanySearchAPIView, CompanySearchView, NormalizeDataCreationViewSet

router = routers.DefaultRouter()
router.register(
    r"normalize-data", NormalizeDataCreationViewSet, basename="normalize-data"
)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "search/", CompanySearchAPIView.as_view({"get": "list"}), name="company-search"
    ),
    path("search-data/", CompanySearchView.as_view(), name="company-data-search"),
]
