""" Food

Defines food with getters for food attributes
"""

from __future__ import annotations
from random import Random

from material import Material
from random_gen import RandomGen

# List of food names from https://github.com/vectorwing/FarmersDelight/tree/1.18.2/src/main/resources/assets/farmersdelight/textures/item
FOOD_NAMES = [
    "Apple Cider",
    "Apple Pie",
    "Apple Pie Slice",
    "Bacon",
    "Bacon And Eggs",
    "Bacon Sandwich",
    "Baked Cod Stew",
    "Barbecue Stick",
    "Beef Patty",
    "Beef Stew",
    "Cabbage",
    "Cabbage Leaf",
    "Cabbage Rolls",
    "Cabbage Seeds",
    "Cake Slice",
    "Chicken Cuts",
    "Chicken Sandwich",
    "Chicken Soup",
    "Chocolate Pie",
    "Chocolate Pie Slice",
    "Cod Slice",
    "Cooked Bacon",
    "Cooked Chicken Cuts",
    "Cooked Cod Slice",
    "Cooked Mutton Chops",
    "Cooked Rice",
    "Cooked Salmon Slice",
    "Dog Food",
    "Dumplings",
    "Egg Sandwich",
    "Fish Stew",
    "Fried Egg",
    "Fried Rice",
    "Fruit Salad",
    "Grilled Salmon",
    "Ham",
    "Hamburger",
    "Honey Cookie",
    "Honey Glazed Ham",
    "Honey Glazed Ham Block",
    "Horse Feed",
    "Hot Cocoa",
    "Melon Juice",
    "Melon Popsicle",
    "Milk Bottle",
    "Minced Beef",
    "Mixed Salad",
    "Mutton Chops",
    "Mutton Wrap",
    "Nether Salad",
    "Noodle Soup",
    "Onion",
    "Pasta With Meatballs",
    "Pasta With Mutton Chop",
    "Pie Crust",
    "Pumpkin Pie Slice",
    "Pumpkin Slice",
    "Pumpkin Soup",
    "Ratatouille",
    "Raw Pasta",
    "Rice",
    "Rice Panicle",
    "Roast Chicken",
    "Roast Chicken Block",
    "Roasted Mutton Chops",
    "Rotten Tomato",
    "Salmon Slice",
    "Shepherds Pie",
    "Shepherds Pie Block",
    "Smoked Ham",
    "Squid Ink Pasta",
    "Steak And Potatoes",
    "Stuffed Potato",
    "Stuffed Pumpkin",
    "Stuffed Pumpkin Block",
    "Sweet Berry Cheesecake",
    "Sweet Berry Cheesecake Slice",
    "Sweet Berry Cookie",
    "Tomato",
    "Tomato Sauce",
    "Tomato Seeds",
    "Vegetable Noodles",
    "Vegetable Soup",
]

class Food:
    """
    Sets food in a certain format
    """
    
    def __init__(self, name: str, hunger_bars: int, price: int) -> None:
        """
        Initializing Food class instance variables

        Parameters:
            name - Name of the food
            hunger_bars - Amount of hunger bars the food replenishes
            price - Cost of food

        Complexity: O(1) 
        """
        self.name = name
        self.hunger_bars = hunger_bars
        self.price = price
    
    def get_hunger_bars(self):
        """
        Returns hunger bars a food replenishes

        Complexity: O(1)
        """
        return self.hunger_bars
    
    def get_price(self):
        """
        Returns price of food

        Complexity: O(1)
        """
        return self.price
    
    def __str__(self) -> str:
        """
        String method. Returns string with format
        
        Complexity: O(1)
        """
        return f"{self.name}"

    @classmethod
    def random_food(cls) -> Food:
        """
        Randomizes a food name, hunger bars and price

        Complexity: O(1)
        """
        hunger_bars = RandomGen.randint(1, 500) # gets a hunger bar level
        price = round(RandomGen.random_float(), 2) # gets a price
        return Food(RandomGen.random_choice(FOOD_NAMES), hunger_bars, price)

if __name__ == "__main__":
    print(Food.random_food())

    print(Food.random_food())

