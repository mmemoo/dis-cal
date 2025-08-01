from pydantic import BaseModel,Field
from ollama import chat
import json
import chromadb
import pandas
from sentence_transformers import SentenceTransformer
from time import time
import torch


device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

food_csv = pandas.read_csv("data/usda_data/food.csv")
food_csv = food_csv[[type(desc) == str for desc in food_csv["description"]]]
food_csv["description"] = [i.lower().replace(",","") for i in food_csv["description"].tolist()]

food_nutrient_csv = pandas.read_csv("data/usda_data/food_nutrient.csv")
nutrient_csv = pandas.read_csv("data/usda_data/nutrient.csv")

client = chromadb.PersistentClient(path = "data/chromadb")
collection = client.get_or_create_collection("foods")


def foodName_to_nutrientsAndCal(food_name,food_amount):
    fdc_id = food_csv[food_csv["description"] == food_name]
    fdc_id = fdc_id["fdc_id"].tolist()[0]

    nutrient_ids = food_nutrient_csv[food_nutrient_csv["fdc_id"] == fdc_id]
    
    amounts = nutrient_ids["amount"].tolist()
    nutrient_ids = nutrient_ids["nutrient_id"].tolist()

    nutrients = {}
    total_cals = 0

    for nutrient_id,amount in zip(nutrient_ids,amounts):
        row = nutrient_csv[nutrient_csv["id"] == nutrient_id]
        
        if amount > 0.0:
            if (unit_name := row["unit_name"].tolist()[0]) == "KCAL":
                total_cals += amount / 100 * food_amount
            else:
                nutrients[row["name"].tolist()[0]] = [amount / 100 * food_amount,unit_name]

    return nutrients,total_cals

def match_foodname(query):
    encoded_query = encoder.encode([query])[0].tolist()

    result = collection.query(encoded_query,n_results=1)
    result = result["documents"][0][0]

    return result

def estimate_cals_and_nutrients(food_items):
    total_nutrients = {}
    total_cals = 0
    
    for food_item in food_items:
        food_name = food_item["food_name"].lower() + " " + food_item["cooking_method"].lower()
        food_name = match_foodname(food_name)

        amount = food_item["amount"]
        nutrients,cals = foodName_to_nutrientsAndCal(food_name,amount)

        for nutrient in nutrients:
            amount,unit = nutrients[nutrient]

            if nutrient in total_nutrients:
                total_nutrients[nutrient][0] = total_nutrients[nutrient][0] + amount
            else:
                total_nutrients[nutrient] = [amount,unit]

        total_cals += cals

    return total_nutrients,total_cals