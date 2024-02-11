import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI( #gets api key from epi file
    api_key=os.environ.get('OPENAI_API_KEY'),
)


def get_meal_plan(bmi, maintenance_calories, ideal_BMI, food_preferences):#function passing information to the api function
    """
    Generate a meal plan using GPT-3.5 based on user input.
    """
    
    messages = [ #messages that the api will be prompted to provide better personalization
        {
            "role": "system",
            "content": "Generate a 7-day meal plan based on the following information."
        },
        {
            "role": "user",
            "content": f"BMI: {bmi}, Maintenance Calories: {maintenance_calories} calories per day, Weight Loss Goal: {ideal_BMI} pounds, Food Preferences/Dietary Restrictions: {food_preferences}. please say the estimated calories per meal and calories per day.Make sure to let the user know that they cam ask for changes to the plan if needed"
        }#gives the data to the model for better personalization
    ]

    response = client.chat.completions.create( 
      model="gpt-3.5-turbo",  # model being used 
      messages=messages,
      temperature=0.7,
      max_tokens=1000,
      top_p=1.0,
      frequency_penalty=0.5,
      presence_penalty=0.0
    )

    return response.choices[0].message.content #returns the output of the api call to the meal_plan function





def main():#will delete just temporary
    print("Welcome to the HealthGPT Meal Planner!")
    bmi = input("Enter your BMI: ")
    maintenance_calories = input("Enter your daily maintenance calories: ")
    ideal_BMI = input("What is your ideal BMI: ")
    food_preferences = input("List any food preferences or dietary restrictions: ")
    
    meal_plan = get_meal_plan(bmi, maintenance_calories, ideal_BMI, food_preferences)
    print("\nHere's your personalized meal plan:\n")
    print(meal_plan)

if __name__ == "__main__":
    main()

