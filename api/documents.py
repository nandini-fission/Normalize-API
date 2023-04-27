from elasticsearch_dsl import Document, Text, Integer, Keyword

from django_elasticsearch_dsl import Document as DjangoDocument
from django_elasticsearch_dsl.registries import registry

from .models import CompaniesData


@registry.register_document
class CompanyDocument(DjangoDocument, Document):
    name = Text(fields={"raw": Keyword()})
    industry = Text(fields={"raw": Keyword()})
    revenue = Integer()
    employees = Integer()
    country = Text(fields={"raw": Keyword()})

    class Index:
        name = "companies"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    def save(self, **kwargs):
        return super().save(**kwargs)

    def delete(self, **kwargs):
        return super().delete(**kwargs)

    @staticmethod
    def search(query=None):
        s = CompanyDocument.search()
        print(query, "query")
        if query:
            s = s.query(
                "multi_match", query=query, fields=["name", "industry", "country"]
            )
        else:
            s = s.query("match_all")

        return s

    class Django:
        model = CompaniesData
