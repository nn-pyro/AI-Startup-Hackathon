import openai
import os
import json
import re


def extract_json_from_text(text):

    start_index = text.find('[')
    end_index = text.rfind(']') + 1
    
    if start_index == -1 or end_index == -1:
        raise ValueError("No valid JSON found in the text")

    json_str = text[start_index:end_index]
    
    return json_str



def gen_respone(user_content):
    
    system_content = """
        You are an intelligent culinary assistant with a deep understanding of Vietnamese food and beverages. 
        Your primary task is to suggest meals and drinks tailored to the user's preferences, dietary needs, or any other information they provide. 
        If the input seems unrelated or vague, use your knowledge and creativity to offer relevant suggestions that might align with their tastes or needs.
        Only food and drink suggestions that are relevant to the user's content are allowed.
        By default, respond in Vietnamese. However, if the user inputs a request in another language or specifically asks for a response in a different language, adapt accordingly and reply in that language.
        The response must strictly adhere to the following JSON structure and should not include any additional text or explanations:
        Not allowed to reply with anything other than json structure

        [
            {
                "food_name": "<Food Name>",
                "food_decription": "<Describe the food in detail>",
                "food_reason": "<Write a paragraph of about 100 words describing why you should choose this food.>",
                "food_review": "<Write a paragraph of about 100 words reviewing a food.>",
                "food_analysis": 
                                "{
                                    "meta": "<Write a paragraph of about 200 words analyzing in detail the nutritional value of the food.>",
                                    "calories": "<Food calorie>",
                                    "nutrients": "<Food nutrients>"
                                }",
                "food_recipe": 
                                "{
                                    "ingredient": "<Food ingredient>",
                                    "bartending": "<Food preparation steps>"
                                }",
            },

            {
                "drink_name": "<Drink Name>",
                "drink_decription": "<Describe the drink in detail>",
                "drink_reason": "<Write a paragraph of about 100 words describing why you should choose this drink.>",
                "drink_review": "<Write a paragraph of about 100 words reviewing a drink.>",
                "drink_analysis": 
                                "{
                                    "meta": "<Write a paragraph of about 200 words analyzing in detail the nutritional value of the drink.>",
                                    "calories": "<Drink calorie>",
                                    "nutrients": "<Drink nutrients>"
                                }",
                "drink_recipe": 
                                "{
                                    "ingredient": "<Drink ingredient>",
                                    "bartending": "<Drink bartending steps>"
                                }",
            }
        ]
        """
    
    client = openai.OpenAI(
        api_key=os.environ.get("API_KEY"),
        base_url=os.environ.get("API_URL"),
    )

    chat_completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
        temperature=0.7,
        max_tokens=2048,
    )

    response = chat_completion.choices[0].message.content
    
    json_content = extract_json_from_text(response)
    return json_content

if __name__ == "__main__":
    
    test = gen_respone("Hôm nay trời vào thu có vẻ mát mẻ")
    print(test)