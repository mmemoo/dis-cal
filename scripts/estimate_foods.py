from pydantic import BaseModel,Field
from ollama import chat
import json


class FoodItem(BaseModel):
    food_name : str
    cooking_method : str = Field(description="Specify a cooking method. The cooking methods provided should be accurate and real. Also , dont say stuff like grilled and roasted together, choose one. And you should ONLY provide cooking methods or if its raw, not preperation methods like sliced etc. This is cruical.")
    amount : float
    unit : str = Field(description="Provide gr or ml. This is crucial")

class Schema(BaseModel):
    foods : list[FoodItem]

prompt = """Tell me the type and amount (in gram's for solids and ml's for liquids) of foods present in the image in this format =
food_type : amount

reply only with the food types and amounts in the specified format and nothing else
the type shouldnt be like , theres food in the bowl so the bowl is this grams. no, it should be very specific like apple or green apple etc. also , specify the parts of the foods (like if its the wing of a chicken etc. if the food doesnt have a part dont specify it) etc. too. 
dont add grams , gr , ml etc. after the amount even if you are giving the amount in grams or ml

reply with foundation foods , not the name of them mixed.

you should always come up with a prediction and not say , i cant , im not confident etc.
the prediction doesnt have to be a round number , it can be but you are not forced
reply in json format

and i step on it again,the amount should be in grams for solids and ml for liquids."""


def estimate_food_amounts(img_path):
    path_2_img = img_path

    response = chat(
        model = "qwen2.5vl:7b",
        messages = [
            {
                "role" : "user",
                "content" : prompt,
                "images" : [path_2_img]
            }
        ],
        format = Schema.model_json_schema()
    )

    response = response.message.content
    response = json.loads(response)
    response = response["foods"]

    return response