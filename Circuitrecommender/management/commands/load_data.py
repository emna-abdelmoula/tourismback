import csv
import pandas as pd
from django.core.management import BaseCommand
from Circuitrecommender.models import Tourism
class Command(BaseCommand):
    help = 'Load a tourism CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        # Remove any existing data
        print("Clean old tourism data")
        Tourism.objects.all().delete()
        path = kwargs['path']
        # Read the tourism CSV file as a dataframe
        Tourism_df = pd.read_csv(path)
        # Iterate each row in the dataframe
        for index, row in Tourism_df.iterrows():
            category_name = row["category_name"]
            subcategory_name = row["subcategory_name"]
            subsubcategory = row["subsubcategory"]
            rating = row["rating"]
            url = row["url"]
            name = row["name"]
            address = row["address"]
            latitude = row["latitude"]
            longitude = row["longitude"]
            cuisine = row["cuisine"]
            Dietaryrestrictions= row["Dietaryrestrictions"]
            price= row["price"]
            GoodFor=row["GoodFor"]
            Duration=row["Duration"]
            Country=row["Country"]
            destinations_features=row["destinations_features"]

            # Populate Tourism object for each row
            tourism = Tourism(
                category_name=category_name,
                subcategory_name=subcategory_name,
                subsubcategory=subsubcategory,
                rating=rating,
                url=url,
                name=name,
                address=address,
                latitude=latitude,
                longitude=longitude,
                cuisine=cuisine,
                Dietaryrestrictions=Dietaryrestrictions,
                price=price,
                GoodFor=GoodFor,
                Duration=Duration,
                Country=Country,
                destinations_features=destinations_features,
            )
            # Save tourism object
            tourism.save()
            print(f"Tourism: {name}, {address} saved...")

# Commande pour exécuter : python manage.py load_tourisms --path tourisms.csv