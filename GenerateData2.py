import json
import random

def generate_meal_plan_conversation(bmi, calories, IdealBMI, preferences):
    meals_snacks = [ #sample data set we used 
    "Almonds & Raisins",
    "Air-popped Popcorn with Butter and Real Sea Salt",
    "Raw Veggies with Hummus",
    "Apples & Peanut Butter",
    "Homemade Granola Bars",
    "Mini Tuna & Cheese Lettuce Wraps",
    "Chicken Salad Lettuce Wraps",
    "Egg Salad Lettuce Wraps",
    "Steamed Veggies Smothered in Butter & Real Sea Salt",
    "Hard-boiled Eggs",
    "Homemade Beef Jerky",
    "Homemade Fruit Leather",
    "Real Sourdough Bread with Butter and Honey-Sweetened Jam",
    "A Piece of Seasonal Fresh Fruit",
    "Fruit Salad",
    "Nachos and Cheese",
    "Homemade Trail Mix",
    "Kale Chips",
    "Roasted Pumpkin or Squash Seeds",
    "Deviled Eggs",
    "Spinach Dip",
    "Simple Herbed Avocado",
    "Dandelion Fritters",
    "Healthy Peppermint Patties",
    "Homemade Potato Chips",
    "Browned Butter Fudge",
    "Raspberry Poppyseed Muffins",
    "Roasted Asparagus with Parmesan and Salt",
    "Steamed Spinach",
    "Homemade Banana Bread",
    "Quinoa Pudding",
    "Dark Chocolate",
    "Dehydrated Fruit Chips",
    "Roasted Chickpeas",
    "Guacamole",
    "Homemade French Fries",
    "Chocolate-Dipped Strawberries",
    "Cold Leftover Pancakes",
    "Meatballs with Marinara for Dipping",
    "Bacon-Wrapped Asparagus, Water Chestnuts, or Scallops",
    "Cold Fried Chicken",
    "Dried Anchovies",
    "Chickpea and Bean Salad",
    "Vegetable Juice",
    ]
    # Generate a conversation-like structure for the meal plan
    conversation = [
        {"role": "system", "content": "Generate a meal plan based on the following requirements."},
        {"role": "user", "content": f"BMI: {bmi}, Calories: {calories}, Ideal BMI: {IdealBMI}, Preferences: {preferences}."},
        {"role": "assistant", "content": random.choice(meals_snacks)}
    ]
    return conversation

def create_dataset(num_entries):
    dataset = []
    for _ in range(num_entries):#loops for amout of data we want to create
        bmi = round(random.uniform(18.5, 30), 1)
        calories = random.choice([1800, 2000, 2200, 2500])
        IdealBMI = round(random.uniform(18.5, 30), 1)#randomizes to create data
        preferences = random.choice(["Vegetarian", "Vegan", "Low-Carb", "High-Protein", "Gluten-Free"])
        
        conversation = generate_meal_plan_conversation(bmi, calories, IdealBMI, preferences)
                          
        dataset.append({
            "messages": conversation
        })
    
    return dataset

def main():
    num_entries = 50  # The number of entries for the dataset
    dataset = create_dataset(num_entries)
    
    # Save the dataset to a JSONL file
    with open('meal_plan_dataset.json', 'w') as f:
        for entry in dataset:
            json_entry = json.dumps(entry)
            f.write(f"{json_entry}\n")

if __name__ == "__main__":
    main()
