import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Circuitrecommender.models import Tourism

def recommend_destinations(user_preferences, num_recommendations):
    # Charger les données de la base de données dans un DataFrame
    queryset = Tourism.objects.all().values()
    df = pd.DataFrame(queryset)
    
    test=True
    split_preferences = user_preferences.split(" ",1)
    subcategory_name_from_split = split_preferences[0]
    price_from_split = split_preferences[1]
    nb1=len(df[df["price"]==price_from_split])
    nb2=len(df[df["subcategory_name"]==subcategory_name_from_split])
    num_recommendation=min(nb1,nb2)
    if num_recommendations >= num_recommendation:
        num_recommendations = num_recommendation
        test=False
        
    recommendation_message = (
         f"Based on your preferences ({user_preferences}), here are {num_recommendations}possibles recommendations"
    )
    

    
    # Créer la colonne destinations_features
    df["destinations_features"] = df["subcategory_name"] + ' ' + df["price"]
    
    # Initialiser CountVectorizer
    vectorizer = CountVectorizer()
    
    # Créer la matrice de caractéristiques pour les destinations
    destinations_features = vectorizer.fit_transform(df["destinations_features"])
    
    # Créer le vecteur utilisateur
    user_vector = vectorizer.transform([user_preferences])
    
    # Calculer la similarité cosinus
    cosine_sim = cosine_similarity(user_vector, destinations_features)
    
    # Trier les scores de similarité
    scores = [(idx, sim) for idx, sim in enumerate(cosine_sim[0])]
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # # Recommander les destinations
    # if num_recommendation > len(scores):
    #     recommendations = [
    #         {
    #             "recommended_destinations_ids": str(df.iloc[index]["id"]),
    #             "category_name": df.iloc[index]["category_name"],
    #             "subcategory_name": df.iloc[index]["subcategory_name"],
    #             "subsubcategory_name": df.iloc[index]["subsubcategory"],
    #             "Photo": df.iloc[index]["url"],
    #             "name": df.iloc[index]["name"],
    #             "Price": df.iloc[index]["price"],
    #             "address" : df.iloc[index]['address'],
    #         }
    #         for index in scores[: len(scores)]
    #     ]
    # else:
    #     recommendations = [
           
    #         {
    #             "recommended_destinations_ids": str(df.iloc[index]["id"]),
    #             "category_name": df.iloc[index]["category_name"],
    #             "subcategory_name": df.iloc[index]["subcategory_name"],
    #             "subsubcategory_name": df.iloc[index]["subsubcategory"],
    #             "Photo": df.iloc[index]["url"],
    #             "name": df.iloc[index]['name'],
    #             "Price": df.iloc[index]["price"],
    #             "address" : df.iloc[index]['address'],
    #         }
    #         for index in scores[:num_recommendation]
      #  ]
   

    # return recommendations
    recommendations = []
    for i in scores[:num_recommendations]:
        index = i[0]
        destinations_details = {
            "number":num_recommendations,
            "recommended_destinations_ids": str(df.iloc[index]['id']),
            "category_name": df.iloc[index]['category_name'],
            "subcategory_name": df.iloc[index]['subcategory_name'],
            "subsubcategory_name": df.iloc[index]['subsubcategory'],
            "Photo": df.iloc[index]['url'],
            "name": df.iloc[index]['name'],
            "Price": df.iloc[index]['price'],
            "address" : df.iloc[index]['address'],
            "longitude": df.iloc[index]['longitude'],
            "latitude": df.iloc[index]['latitude'],
            # "cuisine": df.iloc[index]['cuisine'],
            # "Dietaryrestrictions": df.iloc[index]['Dietaryrestrictions'],
            # "GoodFor": df.iloc[index]['GoodFor'],
            "Country": df.iloc[index]['Country'],
        }
        recommendations.append(destinations_details)
    return recommendations

    
    