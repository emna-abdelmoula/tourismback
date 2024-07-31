# import base64
# from io import BytesIO
# import folium


# def generate_map_image(recommendations):
#     if not recommendations:
#         return None

#     # Create a base map
#     map_center = [recommendations[0]['latitude'], recommendations[0]['longitude']]
#     map_ = folium.Map(location=map_center, zoom_start=13)

#     # Add markers to the map
#     for index, rec in enumerate(recommendations):
#         folium.Marker(
#             location=[rec['latitude'], rec['longitude']],
#             popup=f"Day {index + 1}: {rec['name']}"
#         ).add_to(map_)

#     # Save map to a bytes buffer
#     img_data = BytesIO()
#     map_.save(img_data, close_file=False)

#     # Encode as base64
#     img_data.seek(0)
#     encoded_img_data = base64.b64encode(img_data.read()).decode('utf-8')

#     return encoded_img_data

import folium
import io
import os
from django.http import HttpResponse
from html2image import Html2Image
import pandas as pd

def create_map_image(recommendations):
    # Convertir la liste de recommandations en DataFrame
    place_df = pd.DataFrame(recommendations)

    # Créer une carte Folium
    m = folium.Map(location=[place_df['latitude'].mean(), place_df['longitude'].mean()], zoom_start=13)
    
    for index, row in place_df.iterrows():
        # Ajouter un marqueur pour chaque destination
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"<strong>{row['name']}</strong><br>{row['address']}",
            icon=folium.Icon(color='red' if row['category_name'] == 'Hotels' else ('green' if row['category_name'] == 'Restaurants' else 'blue'))
        ).add_to(m)

        # Ajouter une annotation pour le jour
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 12pt; color: black;"><b>Day {index + 1}</b></div>'
            ),
        ).add_to(m)
        
        # Ajouter une ligne reliant les destinations
        next_index = (index + 1) % len(place_df)
        current_coords = [row['latitude'], row['longitude']]
        next_coords = [place_df.loc[next_index, 'latitude'], place_df.loc[next_index, 'longitude']]
        folium.PolyLine(locations=[current_coords, next_coords]).add_to(m)

    # Sauvegarder la carte en tant que fichier HTML temporaire
    map_html = 'map.html'
    m.save(map_html)

    # Convertir le fichier HTML en image
    hti = Html2Image()
    image_path = 'map_image.png'
    hti.screenshot(html_file=map_html, save_as=image_path)

    # Lire l'image et la convertir en réponse HTTP
    with open(image_path, 'rb') as image_file:
        response = HttpResponse(image_file.read(), content_type='image/png')
    
    # Supprimer les fichiers temporaires
    os.remove(map_html)
    os.remove(image_path)

    return response