# Generated by Django 5.0.4 on 2024-10-11 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_remove_individualcare_index_year_month_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="individualcarecategory",
            name="unique_individual_care_category",
        ),
    ]
