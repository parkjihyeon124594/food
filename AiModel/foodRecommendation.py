from openai import OpenAI
import re


client = OpenAI(api_key= 'sk-vW-Pte2WN_hlhm__LbfjyXCVAfmsWzgzHkxia5FT47T3BlbkFJyl9ythf6RhiIawVER8gb3AHQMDDC8ob_n6R4KFIMEA')

def recommend_food(food=''):
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    #system : instruction
    #user : input
    #assistant : designate output
    messages=[
      {"role": "system", "content": "You are a helpful assistant designed to output."},
      {"role": "user", "content": f"Recommend a food similar to the {food} considering the food information(taste, cost, etc). If it's Indonesian, recommend Korean food and recommend Indonesian vice versa."},
      {"role": "assistant",
       "content": '{"food_name":"~~", "reason":"~~"}'}
    ],

  )
  return response.choices[0].message.content

from openai import OpenAI
client = OpenAI(api_key= 'sk-vW-Pte2WN_hlhm__LbfjyXCVAfmsWzgzHkxia5FT47T3BlbkFJyl9ythf6RhiIawVER8gb3AHQMDDC8ob_n6R4KFIMEA')
def generate_image(food):
  response = client.images.generate(
    model="dall-e-3",
    prompt=food,
    size="1024x1024",
    quality="standard",
    n=1,
  )
  return response



def nutrition(food=''): #calories: kcal, the rest: g
  response = client.chat.completions.create(
    model="gpt-4o",
    response_format={ "type": "json_object" },
    #system : instruction
    #user : input
    #assistant : designate output
    messages=[
      {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
      {"role": "user", "content": f"Give nutritional information about {food}"},
      {"role": "assistant",
       "content": '{"food_name":"Bulgogi", "calories":"100kcal", "carbohydrates":"24g", "protein":"22g", "fat": "20g"}'}
    ],
    temperature=0

  )
  return response.choices[0].message.content