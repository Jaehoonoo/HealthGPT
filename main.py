from taipy import Gui
from taipy.gui import Markdown

bmi_data = {
  "Range": ["Healthy","Underweight","Overweight", "Obese", "Severe obesity"],
  "BMI": [18.5, 10, 25.0, 30.0, 40]
}


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
activity = ''
sex =''
cal = 0
weight = 160
feet = 5
inches = 9
age = 0

#calls functions locally so that it updates
bmi = bmi_calculation(feet, inches, weight)
bmr = bmr_calculation(feet, inches, weight, age, sex)
cal = calorie_calculation(feet, inches, weight, age, sex, activity)
half_pound_loss = calorie_calculation(feet=0, inches=0, weight=0, age=0, sex='Male', activity='Little or no exercise') - 250
pound_loss = calorie_calculation(feet=0, inches=0, weight=0, age=0, sex='Male', activity='Little or no exercise') - 500   
two_pound_loss = calorie_calculation(feet=0, inches=0, weight=0, age=0, sex='Male', activity='Little or no exercise') - 1000

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
<|{bmi_data}|chart|type=pie|values=BMI|labels=Range|>
""")

calorie_page = Markdown("""
#####Maintenance: <|{calorie_calculation(feet, inches, weight, age, sex, activity)}|> calories/day
#####Mild weight loss (0.5 lbs/week): <|{half_pound_loss}|> calories/day
#####Weight loss (1 lb/week): <|{pound_loss}|> calories/day
#####Extreme weight loss (2 lbs/week): <|{two_pound_loss}|> calories/day
""")

meal_plan_page = """
#meals
"""
# pages to navigate through navbar
pages = {
    "/": main,
    "Home": home_page,
    "BMI": bmi_page,
    "Calorie": calorie_page,
    "MealPlan": meal_plan_page
}
#Gui is the graphical user interface that is interactive, runs on local port
Gui(pages=pages).run(use_reloader=True, port=5001)
