import csv
import pandas as pd
from django.core.management import BaseCommand
from Circuitrecommender.models import Hotel

class Command(BaseCommand):
    help = 'Load a hotels CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        # Remove any existing data
        print("Clean old hotels data")
        Hotel.objects.all().delete()
        path = kwargs['path']
        # Read the hotels CSV file as a dataframe
        hotels_df = pd.read_csv(path)
        # Iterate each row in the dataframe
        for index, row in hotels_df.iterrows():
            address = row["address"]
            category = row["category"]
            description = row["description"]
            email = row["email"]
            hotelClass = row["hotelClass"]
            image = row["image"]
            latitude = row["latitude"]
            longitude = row["longitude"]
            name = row["name"]
            phone = row["phone"]
            priceLevel = row["priceLevel"]
            rating = row["rating"]
            subcategories = row.get("subcategories", [])
            website = row["website"]
            amenities = row["amenities"]

            # Populate Hotel object for each row
            hotel = Hotel(
                address=address,
                category=category,
                description=description,
                email=email,
                hotelClass=hotelClass,
                image=image,
                latitude=latitude,
                longitude=longitude,
                name=name,
                phone=phone,
                priceLevel=priceLevel,
                rating=rating,
                subcategories=subcategories,  # Assuming it's a list or convert to list if needed
                website=website,
                amenities=amenities,
            )
            # Save hotel object
            hotel.save()
            print(f"Hotel: {name}, {address} saved...")

