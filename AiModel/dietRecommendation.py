from openai import OpenAI
client = OpenAI(api_key= 'sk-None-seWbT3E091YJULvkFWSzT3BlbkFJgL9xGC3agN1lmJNFvMI2')


def recommend_diet(country='',meal_time='',member_info={},food_list=''):
  response = client.chat.completions.create(
    model="gpt-4o",
    response_format={ "type": "json_object" },
    #system : instruction
    #user : input
    #assistant : designate output
    messages=[
      {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
      {"role": "user", "content": f"You recommend a diet for {meal_time} based on member information and food preference. I live in {country}, my status is : {member_info}. I recently ate {food_list}."},
      {"role": "assistant", "content": ' "data" : {"food_name":"~~", "food_description":"~~", "reason": "~~"} '}
    ],
    temperature=0.1
  )
  return response.choices[0].message.content


