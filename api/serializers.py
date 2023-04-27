from rest_framework import serializers

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents import CompanyDocument
from .models import CompaniesData, Normalize, CompanyNormalize


class CompanyDocumentSerializer(DocumentSerializer):
    class Meta(object):
        """Meta options."""

        model = CompaniesData
        document = CompanyDocument


class CompanyDataSerializer(serializers.ModelSerializer):
    """
    Serializer for CompaniesData objects.

    This serializer maps CompaniesData objects to a JSON representation, and can be
    used to serialize and deserialize data for use with the DRF views.

    """

    class Meta:
        model = CompaniesData
        fields = "__all__"


# class NormalizeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Normalize
#         fields = "__all__"


# class CompanyNormalizeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CompanyNormalize
#         fields = "__all__"
