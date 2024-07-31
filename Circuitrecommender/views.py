# views.py

from django.http import HttpResponse, JsonResponse
import pandas as pd

from Circuitrecommender.models import Hotel, Tourism
from Circuitrecommender.services.distance import haversine_distance
from Circuitrecommender.services.map import create_map_image
from .services.recommendations import recommend_destinations

def recommend_destinations_view(request):
    subcategory_name = request.GET.get('subcategory_name')
    price = request.GET.get('price')
    duration = int(request.GET.get('duration', 1))
    
    # Créer les préférences de l'utilisateur basées sur les filtres
    user_preferences = f"{subcategory_name} {price}"
    
    # Obtenir les recommandations
    recommendations = recommend_destinations(user_preferences, duration)
    
    # Retourner les recommandations sous forme de JSON
    return JsonResponse(recommendations, safe=False)

def get_categories_view(request):
    # Obtenez toutes les catégories uniques depuis la base de données
    categories = Tourism.objects.values_list('category_name', flat=True).distinct()
    return JsonResponse({'categories': list(categories)})
def get_countries_view(request):
    # Obtenez toutes les catégories uniques depuis la base de données
    countries = Tourism.objects.values_list('Country', flat=True).distinct()
    return JsonResponse({'countries': list(countries)})
def get_subcategories_view(request):
    category_name = request.GET.get('category_name')
    if not category_name:
        return JsonResponse({'error': 'Category name is required'}, status=400)
    
    # Obtenez toutes les sous-catégories uniques pour la catégorie donnée
    subcategories = Tourism.objects.filter(category_name=category_name).values_list('subcategory_name', flat=True).distinct()
    return JsonResponse({'subcategories': list(subcategories)})

def get_prices_view(request):
    subcategory_name = request.GET.get('subcategory_name')
    if not subcategory_name:
        return JsonResponse({'error': 'Subcategory name is required'}, status=400)
    
    # Obtenez toutes les options de prix uniques pour la sous-catégorie donnée
    prices = Tourism.objects.filter(subcategory_name=subcategory_name).values_list('price', flat=True).distinct()
    return JsonResponse({'prices': list(prices)})



# from django.http import JsonResponse
# import pandas as pd
# import numpy as np
# from heapq import heappop, heappush
# from Circuitrecommender.models import Hotel
# from Circuitrecommender.services.distance import haversine_distance
# from .services.recommendations import recommend_destinations
# from django.http import JsonResponse
# from Circuitrecommender.models import Hotel
# import pandas as pd
# import numpy as np
# from .services.distance import haversine_distance

# from django.http import JsonResponse
# import pandas as pd
# import numpy as np
# from Circuitrecommender.models import Hotel
# from Circuitrecommender.services.distance import haversine_distance


# def find_nearest_hotels(target_lon, target_lat, df_hotels):
#     distances = {index: np.inf for index in df_hotels.index}
#     distances_heap = [(0, None, target_lon, target_lat)]  # (distance, previous index, lon, lat)
#     visited = set()
#     nearest_hotels = []

#     while distances_heap:
#         current_dist, prev_index, lon, lat = heappop(distances_heap)

#         if prev_index is not None and prev_index in visited:
#             continue

#         visited.add(prev_index)

#         for index, row in df_hotels.iterrows():
#             if index in visited:
#                 continue

#             if pd.notna(row['longitude']) and pd.notna(row['latitude']):
#                 dist = haversine_distance(lon, lat, row['longitude'], row['latitude'])
#                 new_dist = current_dist + dist

#                 if new_dist < distances[index]:
#                     distances[index] = new_dist
#                     heappush(distances_heap, (new_dist, index, row['longitude'], row['latitude']))

#     sorted_hotels = sorted(distances, key=distances.get)[:3]
#     nearest_hotels = [df_hotels.loc[index] for index in sorted_hotels]
    
#     return nearest_hotels

# def recommend_hotels_near_recommendations(request):
#     subcategory_name = request.GET.get('subcategory_name')
#     price = request.GET.get('price')
#     duration = int(request.GET.get('duration', 1))

#     # Créer les préférences de l'utilisateur basées sur les filtres
#     user_preferences = f"{subcategory_name} {price}"
    
#     # Obtenir les recommandations
#     recommendations = recommend_destinations(user_preferences, duration)

#     if not recommendations:
#         return JsonResponse({'error': 'No recommendations found'}, status=404)

#     # Préparer les données des hôtels
#     hotels = Hotel.objects.all()
#     df_hotels = pd.DataFrame.from_records(hotels.values())

#     if df_hotels.empty:
#         return JsonResponse({'error': 'Hotel data not found'}, status=404)

#     all_hotels = []

#     for recommendation in recommendations:
#         target_lon = recommendation.get('longitude')
#         target_lat = recommendation.get('latitude')

#         if pd.notna(target_lon) and pd.notna(target_lat):
#             nearest_hotels = find_nearest_hotels(target_lon, target_lat, df_hotels)
#             all_hotels.extend(nearest_hotels)

#     if not all_hotels:
#         return JsonResponse({'error': 'No hotels found for the given recommendations'}, status=404)

#     # Préparer les données pour la réponse JSON
#     hotels_details = [
#         {
#             "name": hotel["name"],
#             "address": hotel["address"],
#             "priceLevel": hotel["priceLevel"],
#             "rating": hotel["rating"],
#             "image": hotel["image"]
#         }
#         for hotel in all_hotels
#     ]

#     return JsonResponse(hotels_details, safe=False)


from django.http import JsonResponse
import pandas as pd
import numpy as np
from heapq import heappop, heappush
from Circuitrecommender.models import Hotel, Tourism  # Importer le modèle Tourism
from Circuitrecommender.services.distance import haversine_distance
from Circuitrecommender.services.recommendations import recommend_destinations
from django.http import JsonResponse
import pandas as pd
import numpy as np
from heapq import heappop, heappush
from .models import Hotel, Tourism
from .services.distance import haversine_distance
from .services.recommendations import recommend_destinations

# def find_nearest_places(target_lon, target_lat, df_places):
#     distances = {index: np.inf for index in df_places.index}
#     distances_heap = [(0, None, target_lon, target_lat)]
#     visited = set()
#     nearest_places = []

#     while distances_heap:
#         current_dist, prev_index, lon, lat = heappop(distances_heap)

#         if prev_index is not None and prev_index in visited:
#             continue

#         visited.add(prev_index)

#         for index, row in df_places.iterrows():
#             if index in visited:
#                 continue

#             if pd.notna(row['longitude']) and pd.notna(row['latitude']):
#                 dist = haversine_distance(lon, lat, row['longitude'], row['latitude'])
#                 new_dist = current_dist + dist

#                 if new_dist < distances[index]:
#                     distances[index] = new_dist
#                     heappush(distances_heap, (new_dist, index, row['longitude'], row['latitude']))

#     sorted_places = sorted(distances, key=distances.get)[:3]
#     nearest_places = [df_places.loc[index] for index in sorted_places]
    
#     return nearest_places


# def recommend_hotels_and_restaurants_near_recommendations(request):
#     subcategory_name = request.GET.get('subcategory_name')
#     price = request.GET.get('price')
#     duration = int(request.GET.get('duration', 1))

#     user_preferences = f"{subcategory_name} {price}"
#     recommendations = recommend_destinations(user_preferences, duration)

#     if not recommendations:
#         return JsonResponse({'error': 'No recommendations found'}, status=404)

#     category_of_subcategory = Tourism.objects.filter(subcategory_name=subcategory_name).values('category_name').first()
#     if category_of_subcategory:
#         category_name = category_of_subcategory['category_name']
#     else:
#         return JsonResponse({'error': 'Category not found for the given subcategory'}, status=404)

#     hotels = Hotel.objects.all()
#     df_hotels = pd.DataFrame.from_records(hotels.values())

#     if df_hotels.empty:
#         return JsonResponse({'error': 'Hotel data not found'}, status=404)

#     all_hotels = []
#     for recommendation in recommendations:
#         target_lon = recommendation.get('longitude')
#         target_lat = recommendation.get('latitude')

#         if pd.notna(target_lon) and pd.notna(target_lat):
#             nearest_hotels = find_nearest_places(target_lon, target_lat, df_hotels)
#             all_hotels.extend(nearest_hotels)

#     hotels_details = [
#         {
#             "name": hotel.get("name", "N/A"),
#             "address": hotel.get("address", "N/A"),
#             "priceLevel": hotel.get("priceLevel", "N/A"),
#             "rating": hotel.get("rating", "N/A"),
#             "image": hotel.get("image", "N/A")
#         }
#         for hotel in all_hotels
#     ]

#     if category_name == 'Culinary Tourism':
#         return JsonResponse({'hotels': hotels_details}, safe=False)

#     restaurants_df = Tourism.objects.filter(subcategory_name=subcategory_name)
#     df_restaurants = pd.DataFrame.from_records(restaurants_df.values())

#     if df_restaurants.empty:
#         return JsonResponse({'error': 'Restaurant data not found'}, status=404)

#     all_restaurants = []
#     for recommendation in recommendations:
#         target_lon = recommendation.get('longitude')
#         target_lat = recommendation.get('latitude')

#         if pd.notna(target_lon) and pd.notna(target_lat):
#             nearest_restaurants = find_nearest_places(target_lon, target_lat, df_restaurants)
#             all_restaurants.extend(nearest_restaurants)

#     restaurants_details = [
#         {
#             "name": restaurant.get("name", "N/A"),
#             "address": restaurant.get("address", "N/A"),
#             "priceLevel": restaurant.get("price", "N/A"),
#             "rating": restaurant.get("rating", "N/A"),
#             "image": restaurant.get("url", "N/A")
#         }
#         for restaurant in all_restaurants
#     ]

#     response_data = {
#         'hotels': hotels_details,
#         'restaurants': restaurants_details
#     }

#     return JsonResponse(response_data, safe=False)



# Fonction pour trouver les lieux les plus proches
def find_nearest_places(target_lon, target_lat, df_places, num_places=3):
    distances = {index: np.inf for index in df_places.index}
    distances_heap = [(0, None, target_lon, target_lat)]
    visited = set()
    nearest_places = []

    while distances_heap:
        current_dist, prev_index, lon, lat = heappop(distances_heap)

        if prev_index is not None and prev_index in visited:
            continue

        visited.add(prev_index)

        for index, row in df_places.iterrows():
            if index in visited:
                continue

            if pd.notna(row['longitude']) and pd.notna(row['latitude']):
                dist = haversine_distance(lon, lat, row['longitude'], row['latitude'])
                new_dist = current_dist + dist

                if new_dist < distances[index]:
                    distances[index] = new_dist
                    heappush(distances_heap, (new_dist, index, row['longitude'], row['latitude']))

    sorted_places = sorted(distances, key=distances.get)[:num_places]
    nearest_places = [df_places.loc[index] for index in sorted_places]
    
    return nearest_places

# Fonction pour recommander les hôtels et restaurants
def recommend_hotels_and_restaurants_near_recommendations(request):
    subcategory_name = request.GET.get('subcategory_name')
    price = request.GET.get('price')
    duration = int(request.GET.get('duration', 1))

    user_preferences = f"{subcategory_name} {price}"
    recommendations = recommend_destinations(user_preferences, duration)

    if not recommendations:
        return JsonResponse({'error': 'No recommendations found'}, status=404)

    category_of_subcategory = Tourism.objects.filter(subcategory_name=subcategory_name).values('category_name').first()
    if category_of_subcategory:
        category_name = category_of_subcategory['category_name']
    else:
        return JsonResponse({'error': 'Category not found for the given subcategory'}, status=404)

    hotels = Hotel.objects.all()
    df_hotels = pd.DataFrame.from_records(hotels.values())

    if df_hotels.empty:
        return JsonResponse({'error': 'Hotel data not found'}, status=404)

    all_hotels = []
    for recommendation in recommendations:
        target_lon = recommendation.get('longitude')
        target_lat = recommendation.get('latitude')

        if pd.notna(target_lon) and pd.notna(target_lat):
            nearest_hotels = find_nearest_places(target_lon, target_lat, df_hotels, num_places=duration)
            all_hotels.extend(nearest_hotels)

    # Supprimer les doublons possibles et limiter le nombre total d'hôtels affichés
    all_hotels = list({v['id']: v for v in all_hotels}.values())
    all_hotels = sorted(all_hotels, key=lambda x: x['rating'], reverse=True)[:duration]

    hotels_details = [
        {
            "name": hotel.get("name", "N/A"),
            "address": hotel.get("address", "N/A"),
            "priceLevel": hotel.get("priceLevel", "N/A"),
            "rating": hotel.get("rating", "N/A"),
            "image": hotel.get("image", "N/A")
        }
        for hotel in all_hotels
    ]

    if category_name == 'Culinary Tourism':
        return JsonResponse({'hotels': hotels_details}, safe=False)

    restaurants_df = Tourism.objects.filter(subcategory_name="Restaurants")
    df_restaurants = pd.DataFrame.from_records(restaurants_df.values())

    if df_restaurants.empty:
        return JsonResponse({'error': 'Restaurant data not found'}, status=404)

    all_restaurants = []
    for recommendation in recommendations:
        target_lon = recommendation.get('longitude')
        target_lat = recommendation.get('latitude')

        if pd.notna(target_lon) and pd.notna(target_lat):
            nearest_restaurants = find_nearest_places(target_lon, target_lat, df_restaurants, num_places=duration)
            all_restaurants.extend(nearest_restaurants)

    # Supprimer les doublons possibles et limiter le nombre total de restaurants affichés
    all_restaurants = list({v['id']: v for v in all_restaurants}.values())
    all_restaurants = sorted(all_restaurants, key=lambda x: x['rating'], reverse=True)[:duration]

    restaurants_details = [
        {
            "name": restaurant.get("name", "N/A"),
            "address": restaurant.get("address", "N/A"),
            "priceLevel": restaurant.get("price", "N/A"),
            "rating": restaurant.get("rating", "N/A"),
            "image": restaurant.get("url", "N/A")
        }
        for restaurant in all_restaurants
    ]

    response_data = {
        'hotels': hotels_details,
        'restaurants': restaurants_details
    }

    return JsonResponse(response_data, safe=False)


from django.http import JsonResponse
from django.views.decorators.http import require_GET
import folium
import base64
from io import BytesIO
from Circuitrecommender.services.recommendations import recommend_destinations
from django.http import JsonResponse
from django.views.decorators.http import require_GET
# Assurez-vous d'avoir cette fonction dans votre code

# @require_GET
# def map_image_view(request):
#     subcategory_name = request.GET.get('subcategory_name')
#     price = request.GET.get('price')
#     duration = int(request.GET.get('duration', 1))
    
#     # Créer les préférences de l'utilisateur basées sur les filtres
#     user_preferences = f"{subcategory_name} {price}"
    
#     # Obtenir les recommandations
#     recommendations = recommend_destinations(user_preferences, duration)
    
#     map_image = generate_map_image(recommendations)

#     if map_image:
#         return JsonResponse({'map_image': map_image})
#     else:
#         return JsonResponse({'error': 'No recommendations available'}, status=400)


@require_GET
def map_image_view(request):
    subcategory_name = request.GET.get('subcategory_name')
    price = request.GET.get('price')
    duration = int(request.GET.get('duration', 1))
    
    # Créer les préférences de l'utilisateur basées sur les filtres
    user_preferences = f"{subcategory_name} {price}"
    
    # Obtenir les recommandations
    recommendations = recommend_destinations(user_preferences, duration)
    
    if recommendations and isinstance(recommendations, list) and len(recommendations) > 0:
        map_image = create_map_image(recommendations)
        
        # Créer une réponse HttpResponse avec le type de contenu approprié
        response = HttpResponse(map_image, content_type='image/png')
        response['Content-Disposition'] = 'inline; filename="map.png"'
        return response
    else:
        return JsonResponse({'error': 'No recommendations available'}, status=400)