from django.db import models


class CompaniesData(models.Model):
    """
    Represents data for a company in the database.

    Fields:
    - name: A CharField that stores the name of the company.
    - industry: A CharField that stores the industry of the company.
    - revenue: A DecimalField that stores the revenue of the company.
    - employees: An IntegerField that stores the number of employees in the company.
    - country: A CharField that stores the country of the company.
    """

    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    employees = models.IntegerField()
    country = models.CharField(max_length=255)

    class Meta:
        db_table = "companies_data"

    def __str__(self):
        """
        Returns the name of the company when the object is printed or displayed in the Django admin interface.
        """
        return self.name


class Normalize(models.Model):
    """
    Represents a normalized name in the database.

    Fields:
    - name: A CharField that stores the normalized name.
    """

    name = models.CharField(
        max_length=255, unique=True, help_text="The normalized name."
    )

    class Meta:
        db_table = "normalize"

    def __str__(self):
        """
        Returns the name of the normalized name object when the object is printed or displayed in the Django admin interface.
        """
        return self.name


class CompanyNormalize(models.Model):
    """
    Represents the normalization of a company in the database.

    Fields:
    - normalized_name: A ForeignKey to the NormalizedName model, representing the normalized name being applied.
    - company: A ForeignKey to the CompaniesData model, representing the company being normalized.
    """

    normalized_name = models.ForeignKey(Normalize, on_delete=models.CASCADE)
    company = models.ForeignKey(
        CompaniesData, on_delete=models.CASCADE, related_name="normalizations"
    )

    class Meta:
        unique_together = ("normalized_name", "company")
        db_table = "company_normalize"

    def __str__(self):
        """
        Returns a string representation of the CompanyNormalize object.
        """
        return f"{self.company.name} ({self.normalized_name.name})"
