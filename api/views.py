from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status

from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from .models import CompaniesData, Normalize, CompanyNormalize
from .documents import CompanyDocument
from .serializers import (
    CompanyDocumentSerializer,
    CompanyDataSerializer,
)


class CompanySearchAPIView(DocumentViewSet):
    document = CompanyDocument
    serializer_class = CompanyDocumentSerializer
    lookup_field = "id"

    filter_backends = [
        CompoundSearchFilterBackend,
        FilteringFilterBackend,
        OrderingFilterBackend,
    ]
    search_fields = (
        "name",
        "industry",
        "country",
    )
    filter_fields = {
        "name": "name.raw",
        "industry": "industry.raw",
        "revenue": "revenue",
        "employees": "employees",
        "country": "country.raw",
    }
    ordering_fields = {"name": "name.raw", "industry": "industry.raw"}


class CompanySearchView(generics.ListAPIView):
    """
    Search for MyModel objects based on a query string.

    This view expects a query string parameter 'q', which is used to filter
    MyModel objects by the 'name' field. The search is case-insensitive.

    Example usage:
        /search-data/?q=query

    """

    serializer_class = CompanyDataSerializer

    def get_queryset(self):
        """
        Return a queryset of MyModel objects that match the search query.

        This method filters MyModel objects by the 'name' field, using a
        case-insensitive search. The search term is specified in the 'q'
        query string parameter.

        Returns:
            A queryset of MyModel objects that match the search query.
        """
        query = self.request.query_params.get("q")
        return CompaniesData.objects.filter(name__icontains=query)


class NormalizeDataCreationViewSet(viewsets.ViewSet):
    def create(self, request):
        normalized_name = request.data.get("name", None)
        company_data = request.data.get("ids", [])

        print(company_data)

        if not normalized_name:
            return Response({"error": "Normalized name is required."}, status=400)

        if not company_data:
            return Response(
                {
                    "error": "Please select the data that needs to be mapped with a normalized name."
                },
                status=400,
            )

        normalized_obj, _ = Normalize.objects.get_or_create(name=normalized_name)

        for company in company_data:
            try:
                company_obj = CompaniesData.objects.get(id=company)
            except:
                return Response({"error": "Invalid Data!"}, status=404)

            normalized_comapany_data_obj, _ = CompanyNormalize.objects.get_or_create(
                normalized_name=normalized_obj, company=company_obj
            )

        return Response({"Message": "Data has been successfully created."}, status=200)
