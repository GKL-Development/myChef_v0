import json
import streamlit as st

# Activates when user need to generate a meal planning. 
# It will prompt Gemini AI using the API and return a JSON structured output that will be sent to Neon Database to be stored

def api_call():
    '''Start a AI prompt for meal plan - TBD'''
    return

# Store the API result in a variable for decomposition - later this will be directly sent to json.loads(api_call())
json_data = """
    {
  "recipes": [
    {
      "Allergen Safety Note": "Always double-check ingredient labels to ensure they are free from your allergens, especially nuts, dairy, shellfish, and soy, and to prevent cross-contamination.",
      "Cook time": "12 minutes",
      "Equipment": "Large skillet with lid, cutting board, knife",
      "Ingredients List": [
        {
          "Ingredient Name": "Chicken thighs (boneless, skinless)",
          "Quantity": 2,
          "Unit": "lbs"
        },
        {
          "Ingredient Name": "Asparagus",
          "Quantity": 1,
          "Unit": "bunch"
        },
        {
          "Ingredient Name": "New potatoes",
          "Quantity": 1,
          "Unit": "lb"
        },
        {
          "Ingredient Name": "Olive oil",
          "Quantity": 2,
          "Unit": "tablespoons"
        },
        {
          "Ingredient Name": "Lemon",
          "Quantity": 1,
          "Unit": ""
        },
        {
          "Ingredient Name": "Fresh thyme",
          "Quantity": 2,
          "Unit": "sprigs"
        },
        {
          "Ingredient Name": "Salt and pepper",
          "Quantity": 1,
          "Unit": "to taste"
        }
      ],
      "Instructions": [
        "Preheat skillet over medium-high heat. Season chicken with salt and pepper.",
        "Add olive oil to the skillet. Sear chicken for 3 minutes per side until browned.",
        "Add new potatoes and asparagus to the skillet around the chicken.",
        "Squeeze lemon juice over the chicken and vegetables. Add thyme sprigs.",
        "Cover the skillet and cook for 10 minutes, or until chicken is cooked through and vegetables are tender.",
        "Serve immediately."
      ],
      "Is Meat Or Fish": true,
      "MyChef Note": "This one-pan chicken with spring vegetables is a quick and easy dinner, perfect for a busy weeknight. The lemon and thyme add a bright, fresh flavor.",
      "MyChef Tips": [
        {
          "Kid-Friendly Adaptation": "Cut the chicken and vegetables into smaller, bite-sized pieces for easier eating. Serve with a dollop of plain yogurt or applesauce.",
          "Serving Suggestion": "Serve with a side of crusty bread to soak up the pan juices.",
          "Variations": "Try adding other spring vegetables like peas or fava beans. You can also substitute chicken breasts for the thighs, but reduce the cooking time accordingly."
        }
      ],
      "Prep time": "8 minutes",
      "Recipe Title": "One-Pan Lemon-Thyme Chicken with Spring Vegetables",
      "Total time": "23 minutes",
      "Yield": [
        "2 adults",
        "1 child"
      ]
    },
    {
      "Allergen Safety Note": "Always double-check ingredient labels to ensure they are free from your allergens, especially nuts, dairy, shellfish, and soy, and to prevent cross-contamination.",
      "Cook time": "15 minutes",
      "Equipment": "Steamer basket, pot with lid, cutting board, knife",
      "Ingredients List": [
        {
          "Ingredient Name": "Salmon fillets",
          "Quantity": 2,
          "Unit": ""
        },
        {
          "Ingredient Name": "Green beans",
          "Quantity": 1,
          "Unit": "lb"
        },
        {
          "Ingredient Name": "Radishes",
          "Quantity": 6,
          "Unit": ""
        },
        {
          "Ingredient Name": "Dill",
          "Quantity": 2,
          "Unit": "tablespoons"
        },
        {
          "Ingredient Name": "Lemon",
          "Quantity": 1,
          "Unit": ""
        },
        {
          "Ingredient Name": "Olive oil",
          "Quantity": 1,
          "Unit": "tablespoon"
        },
        {
          "Ingredient Name": "Salt and pepper",
          "Quantity": 1,
          "Unit": "to taste"
        }
      ],
      "Instructions": [
        "Fill a pot with water and bring to a boil. Place green beans and sliced radishes in a steamer basket. Steam for 8 minutes.",
        "Place salmon fillets on top of the vegetables in the steamer basket. Steam for another 7 minutes, or until salmon is cooked through.",
        "In a small bowl, whisk together olive oil, lemon juice, dill, salt, and pepper.",
        "Serve salmon and vegetables drizzled with the dill dressing."
      ],
      "Is Meat Or Fish": true,
      "MyChef Note": "Steaming is a gentle and healthy way to cook salmon and vegetables, preserving their nutrients and delicate flavors. The dill dressing adds a bright, herbaceous touch.",
      "MyChef Tips": [
        {
          "Kid-Friendly Adaptation": "Make sure all bones are removed from the salmon. Serve with a side of mashed sweet potato or rice.",
          "Serving Suggestion": "Serve with a side of quinoa or couscous.",
          "Variations": "Try using other herbs like parsley or chives. You can also add a sprinkle of red pepper flakes for a little heat."
        }
      ],
      "Prep time": "7 minutes",
      "Recipe Title": "Steamed Salmon with Spring Vegetables and Dill Dressing",
      "Total time": "25 minutes",
      "Yield": [
        "2 adults",
        "1 child"
      ]
    },
    {
      "Allergen Safety Note": "Always double-check ingredient labels to ensure they are free from your allergens, especially nuts, dairy, shellfish, and soy, and to prevent cross-contamination.",
      "Cook time": "18 minutes",
      "Equipment": "Large pot, colander, cutting board, knife",
      "Ingredients List": [
        {
          "Ingredient Name": "Fava beans (fresh or frozen)",
          "Quantity": 2,
          "Unit": "cups"
        },
        {
          "Ingredient Name": "Peas (fresh or frozen)",
          "Quantity": 1,
          "Unit": "cup"
        },
        {
          "Ingredient Name": "Leeks",
          "Quantity": 1,
          "Unit": ""
        },
        {
          "Ingredient Name": "Vegetable broth",
          "Quantity": 4,
          "Unit": "cups"
        },
        {
          "Ingredient Name": "Fresh mint",
          "Quantity": 2,
          "Unit": "tablespoons"
        },
        {
          "Ingredient Name": "Olive oil",
          "Quantity": 1,
          "Unit": "tablespoon"
        },
        {
          "Ingredient Name": "Salt and pepper",
          "Quantity": 1,
          "Unit": "to taste"
        }
      ],
      "Instructions": [
        "Shell the fava beans (if using fresh). Blanch in boiling water for 1 minute, then transfer to an ice bath. Remove the outer skin of the fava beans.",
        "Thinly slice the leek (white and light green parts only).",
        "Heat olive oil in a large pot over medium heat. Add leek and cook until softened, about 5 minutes.",
        "Add vegetable broth, fava beans, and peas to the pot. Bring to a simmer and cook for 10 minutes.",
        "Stir in fresh mint, salt, and pepper. Serve hot."
      ],
      "Is Meat Or Fish": false,
      "MyChef Note": "This simple spring soup is packed with fresh, vibrant flavors. Fava beans can be a bit of work to prepare, but their creamy texture is worth the effort.",
      "MyChef Tips": [
        {
          "Kid-Friendly Adaptation": "Puree a portion of the soup for a smoother texture. Serve with a side of grilled cheese or crackers.",
          "Serving Suggestion": "Serve with a dollop of crème fraîche or a swirl of pesto.",
          "Variations": "Add other spring vegetables like asparagus or artichoke hearts. You can also add a splash of white wine to the soup while cooking."
        }
      ],
      "Prep time": "10 minutes",
      "Recipe Title": "Spring Vegetable Soup with Fava Beans and Mint",
      "Total time": "32 minutes",
      "Yield": [
        "2 adults",
        "1 child"
      ]
    },
    {
      "Allergen Safety Note": "Always double-check ingredient labels to ensure they are free from your allergens, especially nuts, dairy, shellfish, and soy, and to prevent cross-contamination.",
      "Cook time": "10 minutes",
      "Equipment": "Large skillet, cutting board, knife",
      "Ingredients List": [
        {
          "Ingredient Name": "Halloumi cheese",
          "Quantity": 8,
          "Unit": "oz"
        },
        {
          "Ingredient Name": "Spinach",
          "Quantity": 5,
          "Unit": "oz"
        },
        {
          "Ingredient Name": "Strawberries",
          "Quantity": 1,
          "Unit": "cup"
        },
        {
          "Ingredient Name": "Balsamic glaze",
          "Quantity": 2,
          "Unit": "tablespoons"
        },
        {
          "Ingredient Name": "Olive oil",
          "Quantity": 1,
          "Unit": "tablespoon"
        },
        {
          "Ingredient Name": "Salt and pepper",
          "Quantity": 1,
          "Unit": "to taste"
        }
      ],
      "Instructions": [
        "Cut the halloumi cheese into slices.",
        "Heat olive oil in a large skillet over medium heat. Add halloumi and cook for 3 minutes per side, or until golden brown.",
        "Add spinach to the skillet and cook until wilted, about 2 minutes.",
        "Add strawberries to the skillet and cook for 1 minute.",
        "Drizzle with balsamic glaze. Serve immediately."
      ],
      "Is Meat Or Fish": false,
      "MyChef Note": "Halloumi is a firm, salty cheese that grills beautifully and adds a delicious savory element to this salad. The sweetness of the strawberries and the tang of the balsamic glaze complement the cheese perfectly.",
      "MyChef Tips": [
        {
          "Kid-Friendly Adaptation": "Cut the halloumi into smaller pieces. Serve with a side of bread or pita.",
          "Serving Suggestion": "Serve as a light meal or a side dish.",
          "Variations": "Add other spring fruits like raspberries or blueberries. You can also add a sprinkle of chopped nuts (if no allergies) for added crunch."
        }
      ],
      "Prep time": "6 minutes",
      "Recipe Title": "Pan-Fried Halloumi with Spinach and Strawberries",
      "Total time": "18 minutes",
      "Yield": [
        "2 adults",
        "1 child"
      ]
    },
    {
      "Allergen Safety Note": "Always double-check ingredient labels to ensure they are free from your allergens, especially nuts, dairy, shellfish, and soy, and to prevent cross-contamination.",
      "Cook time": "16 minutes",
      "Equipment": "Baking sheet, parchment paper, cutting board, knife",
      "Ingredients List": [
        {
          "Ingredient Name": "Spring lamb chops",
          "Quantity": 6,
          "Unit": ""
        },
        {
          "Ingredient Name": "Carrots",
          "Quantity": 1,
          "Unit": "lb"
        },
        {
          "Ingredient Name": "Garlic",
          "Quantity": 3,
          "Unit": "cloves"
        },
        {
          "Ingredient Name": "Rosemary",
          "Quantity": 2,
          "Unit": "sprigs"
        },
        {
          "Ingredient Name": "Olive oil",
          "Quantity": 2,
          "Unit": "tablespoons"
        },
        {
          "Ingredient Name": "Salt and pepper",
          "Quantity": 1,
          "Unit": "to taste"
        }
      ],
      "Instructions": [
        "Preheat oven to 400°F (200°C). Line a baking sheet with parchment paper.",
        "Peel and chop carrots. Mince garlic.",
        "In a bowl, combine carrots, garlic, rosemary, olive oil, salt, and pepper.",
        "Place lamb chops on the baking sheet. Spread the carrot mixture around the lamb chops.",
        "Bake for 16 minutes, or until lamb is cooked to your liking.",
        "Serve immediately."
      ],
      "Is Meat Or Fish": true,
      "MyChef Note": "Spring lamb is tender and flavorful, and roasting it with carrots and rosemary creates a delicious and aromatic dish. Adjust cooking time to your preference.",
      "MyChef Tips": [
        {
          "Kid-Friendly Adaptation": "Cut the lamb into smaller pieces and remove any bones. Serve with a side of mashed potatoes or sweet potato fries.",
          "Serving Suggestion": "Serve with a side of roasted asparagus or green beans.",
          "Variations": "Add other root vegetables like parsnips or turnips. You can also use different herbs like thyme or oregano."
        }
      ],
      "Prep time": "9 minutes",
      "Recipe Title": "Roasted Spring Lamb Chops with Carrots and Rosemary",
      "Total time": "29 minutes",
      "Yield": [
        "2 adults",
        "1 child"
      ]
    },
    {
      "Allergen Safety Note": "Always double-check ingredient labels to ensure they are free from your allergens, especially nuts, dairy, shellfish, and soy, and to prevent cross-contamination.",
      "Cook time": "14 minutes",
      "Equipment": "Large pot, colander, cutting board, knife",
      "Ingredients List": [
        {
          "Ingredient Name": "White asparagus",
          "Quantity": 1,
          "Unit": "lb"
        },
        {
          "Ingredient Name": "Eggs",
          "Quantity": 3,
          "Unit": ""
        },
        {
          "Ingredient Name": "Butter",
          "Quantity": 2,
          "Unit": "tablespoons"
        },
        {
          "Ingredient Name": "Lemon juice",
          "Quantity": 1,
          "Unit": "tablespoon"
        },
        {
          "Ingredient Name": "Parsley",
          "Quantity": 2,
          "Unit": "tablespoons"
        },
        {
          "Ingredient Name": "Salt and pepper",
          "Quantity": 1,
          "Unit": "to taste"
        }
      ],
      "Instructions": [
        "Peel the white asparagus. Snap off the tough ends.",
        "Boil water in a large pot. Cook asparagus until tender, about 8 minutes.",
        "While asparagus is cooking, poach the eggs.",
        "Melt butter in a small saucepan. Whisk in lemon juice, parsley, salt, and pepper.",
        "Drain asparagus and arrange on plates. Top with poached eggs and drizzle with lemon-butter sauce. Serve immediately."
      ],
      "Is Meat Or Fish": false,
      "MyChef Note": "White asparagus is a delicacy in Europe during the spring. Its mild, slightly sweet flavor pairs perfectly with poached eggs and a tangy lemon-butter sauce.",
      "MyChef Tips": [
        {
          "Kid-Friendly Adaptation": "Serve the asparagus with scrambled eggs instead of poached eggs. Cut the asparagus into smaller pieces.",
          "Serving Suggestion": "Serve with a side of crusty bread or toast.",
          "Variations": "Add a sprinkle of Parmesan cheese (if no dairy allergy). You can also add a pinch of red pepper flakes for a little heat."
        }
      ],
      "Prep time": "8 minutes",
      "Recipe Title": "White Asparagus with Poached Eggs and Lemon-Butter Sauce",
      "Total time": "24 minutes",
      "Yield": [
        "2 adults",
        "1 child"
      ]
    },
    {
      "Allergen Safety Note": "Always double-check ingredient labels to ensure they are free from your allergens, especially nuts, dairy, shellfish, and soy, and to prevent cross-contamination.",
      "Cook time": "19 minutes",
      "Equipment": "Large skillet, cutting board, knife",
      "Ingredients List": [
        {
          "Ingredient Name": "Ramps (wild garlic)",
          "Quantity": 1,
          "Unit": "bunch"
        },
        {
          "Ingredient Name": "Potatoes",
          "Quantity": 1,
          "Unit": "lb"
        },
        {
          "Ingredient Name": "Eggs",
          "Quantity": 4,
          "Unit": ""
        },
        {
          "Ingredient Name": "Olive oil",
          "Quantity": 2,
          "Unit": "tablespoons"
        },
        {
          "Ingredient Name": "Salt and pepper",
          "Quantity": 1,
          "Unit": "to taste"
        }
      ],
      "Instructions": [
        "Wash ramps thoroughly. Chop the leaves and bulbs separately.",
        "Boil potatoes until tender.",
        "Heat olive oil in a large skillet over medium heat. Add ramp bulbs and cook until softened, about 5 minutes.",
        "Add cooked potatoes and ramp leaves to the skillet. Cook until heated through, about 3 minutes.",
        "Crack eggs into the skillet. Cook until eggs are set to your liking.",
        "Season with salt and pepper. Serve immediately."
      ],
      "Is Meat Or Fish": false,
      "MyChef Note": "Ramps, also known as wild garlic, are a spring delicacy with a garlicky, oniony flavor. This simple frittata is a great way to showcase their unique taste. If you cannot find ramps, use scallions and a clove of minced garlic.",
      "MyChef Tips": [
        {
          "Kid-Friendly Adaptation": "Cut the frittata into wedges. Serve with a side of fruit or yogurt.",
          "Serving Suggestion": "Serve with a side of salad or crusty bread.",
          "Variations": "Add other spring vegetables like asparagus or peas. You can also add cheese (if no dairy allergy) for a richer flavor."
        }
      ],
      "Prep time": "10 minutes",
      "Recipe Title": "Ramp and Potato Frittata",
      "Total time": "32 minutes",
      "Yield": [
        "2 adults",
        "1 child"
      ]
    }
  ]
}
"""

data = json.loads(json_data)

recipes = data['recipes']

# Insert SQL scripts
insert_sql = """
INSERT INTO meals (
    meal_id,
    recipeTitle,
    yield,
    prepTime,
    cookTime,
    ingredientsList,
    myChefNotes,
    equipment,
    instructions,
    myChefTips,
    allergens,
    allergensSafetyNote,
    isMeatOrFish
) VALUES (
    :meal_id,
    :recipeTitle,
    :yield,
    :prepTime,
    :cookTime,
    :ingredientsList,
    :myChefNotes,
    :equipment,
    :instructions,
    :myChefTips,
    :allergens,
    :allergensSafetyNote,
    :isMeatOrFish
);
"""

def databaseStorage(sqlInsert, recipesData):
    conn = st.connection('neon', type='sql')
    with conn.session as s:
        try:
            for i, recipe in enumerate(recipesData):
                meal_data = {
                    "meal_id": 1, # TBD replace with actual user ID
                    "recipeTitle": recipe.get("Recipe Title"),
                    "yield": json.dumps(recipe.get("Yield")), # Convert list to JSON string for TEXT column
                    "prepTime": recipe.get("Prep time"),
                    "cookTime": recipe.get("Cook time"),
                    "ingredientsList": json.dumps(recipe.get("Ingredients List")),
                    "myChefNotes": recipe.get("MyChef Note"),
                    "equipment": recipe.get("Equipment"),
                    "instructions": json.dumps(recipe.get("Instructions")),
                    "myChefTips": json.dumps(recipe.get("MyChef Tips")),
                    "allergens": json.dumps(recipe.get("Allergens", [])), # Provide empty list if key not found
                    "allergensSafetyNote": recipe.get("Allergen Safety Note"),
                    "isMeatOrFish": recipe.get("Is Meat Or Fish")
                }
                s.execute(sqlInsert, meal_data)
            s.commit()
            st.success(f"Successfully inserted {len(recipesData)} recipes for User ID: {1}")
        except Exception as e:
            st.error(f"The following error occured during insertion to database: {e}")
            s.rollback()