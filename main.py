from taipy import Gui
from taipy.gui import Markdown, State, notify
import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd


load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

#chatbot
context = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today? "
conversation = {
    "Conversation": ["Hi! I am NutriBot. How can I help you today?"]
}
current_user_message = ""

#chatbot request message
def request(state: State, prompt: str) -> str:
    """
    Send a prompt to the GPT-3 API and return the response.

    Args:
        - state: The current state.
        - prompt: The prompt to send to the API.

    Returns:
        The response from the API.
    """
    response = state.client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
        model="gpt-3.5-turbo",
    )
    return response.choices[0].message.content

# send message to chatbot
def send_message(state: State) -> None:
    """
    Send the user's message to the API and update the conversation.

    Args:
        - state: The current state.
    """
    # Add the user's message to the context
    state.context += f"Human: \n {state.current_user_message}\n\n AI:"
    # Send the user's message to the API and get the response
    answer = request(state, state.context).replace("\n", "")
    # Add the response to the context for future messages
    state.context += answer
    # Update the conversation
    conv = state.conversation._dict.copy()
    conv["Conversation"] += [state.current_user_message, answer]
    state.conversation = conv
    # Clear the input field
    state.current_user_message = ""




bmi_data = pd.DataFrame(
    {
    "Categories": ["Underweight","Healthy", "Overweight", "Obesity"],
    "Ranges": [(0), (18.5), (29.9), (40)]
    }
)

def bmi_calculation(feet, inches, weight):
        # calculates BMI
        bmi = (weight / 2.205) / ((((feet * 12) + inches) * .0254)**2)
        return round(bmi, 1)

def bmr_calculation(feet, inches, weight, age, sex):
    #calculates bmr based on sex to later be passed onto the users activity level
    height = (feet * 30.48) + (inches * 2.54) #converts from inches to cm
    if sex == 'Male':
        bmr = (10 * (weight/2.205)) + (6.25 * height) - (5 * age) + 5
        return bmr
    else: 
        bmr = (10 * (weight/2.205)) + (6.25 * height) - (5 * age) + 161
        return bmr

def calorie_calculation(feet, inches, weight, age, sex, activity):
    # Calculates the calories for maintaining weight based on activity level
    if activity == "Little or no exercise":
        return round(bmr_calculation(feet, inches, weight, age, sex) * 1.2)
    elif activity == "Exercise 1-3 times/week":
        return round(bmr_calculation(feet, inches, weight, age, sex) * 1.375)
    elif activity == "Exercise 3-5 times/week":
        return round(bmr_calculation(feet, inches, weight, age, sex) * 1.55)
    elif activity == "Exercise 6-7 times/week":
        return round(bmr_calculation(feet, inches, weight, age, sex) * 1.725)
    elif activity == "Very intense exercise or 2x training":
        return round(bmr_calculation(feet, inches, weight, age, sex) * 1.9)
    
      

#presets to allow program to run
activity = 'Little or no exercise'
sex ='Male'
cal = 0
weight = 160
feet = 5
inches = 9
age = 18

#calls functions locally so that it updates
bmi = bmi_calculation(feet, inches, weight)
bmr = bmr_calculation(feet, inches, weight, age, sex)
cal = calorie_calculation(feet, inches, weight, age, sex, activity)
#half_pound_loss = cal - 250
#pound_loss = calorie_calculation(feet, inches, weight, age, sex, activity) - 500   
#two_pound_loss = calorie_calculation(feet, inches, weight, age, sex, activity) - 1000

# initializes navbar and title
# Add a navbar to switch from one page to the other
main = Markdown("""
#HealthGPT
<|navbar|>
""")

# page to input user data
home_page = Markdown("""## Achieve your fitness goals.
###Input your data :)
<|layout|columns=200px 1fr 50px|
<|{sex}|toggle|lov=Male;Female|>
<|{age}|number|label=Age|>
|>
<|layout|columns=200px auto 50px|
<|{feet}|number|label=Feet|>
<|{inches}|number|label=Inches|>
|>
<|layout|columns=200px 1fr 50px
<|{weight}|number|label=Weight (lbs)|>
<|{activity}|selector|label=Activity level|lov=Little or no exercise;Exercise 1-3 times/week;Exercise 3-5 times/week;Exercise 6-7 times/week;Very intense exercise or 2x training|dropdown|>
|>
""")

#markdown allows function call; function call allows updates based on user input
bmi_page = Markdown("""
<|{bmi_calculation(feet, inches, weight)}|number|active=False|>
<|{bmi_data}|chart|type=line|values=Ranges|labels=Categories|>
""")

calorie_page = Markdown("""
####Maintenance: 
<|{calorie_calculation(feet, inches, weight, age, sex, activity)}|> cal/day
                        
####Mild weight loss (0.5 lbs/week):
<|{calorie_calculation(feet, inches, weight, age, sex, activity)-250}|> cal/day

####Weight loss (1 lb/week):
<|{calorie_calculation(feet, inches, weight, age, sex, activity)-500}|> cal/day
                        
####Extreme weight loss (2 lbs/week): 
<|{calorie_calculation(feet, inches, weight, age, sex, activity)-1000}|> cal/day
""")

meal_plan_page = """
#meals
"""

chatbot_page = """
<|{conversation}|table|show_all|width=100%|>
<|{current_user_message}|input|label=Write your message here...|on_action=send_message|class_name=fullwidth|>
"""

# pages to navigate through navbar
pages = {
    "/": main,
    "Home": home_page,
    "BMI": bmi_page,
    "Calorie": calorie_page,
    "MealPlan": meal_plan_page,
    "ChatBot": chatbot_page
}

#Gui is the graphical user interface that is interactive, runs on local port
Gui(pages=pages).run(use_reloader=True, port=5001)