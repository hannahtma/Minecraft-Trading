from __future__ import annotations
from avl import AVLTree

from cave import Cave
from material import Material
from trader import Trader
from food import Food
from random_gen import RandomGen
from node import TreeNode
from hash_table import LinearProbeTable

# List taken from https://minecraft.fandom.com/wiki/Mob
PLAYER_NAMES = [
    "Steve",
    "Alex",
    "ɘᴎiɿdoɿɘH",
    "Allay",
    "Axolotl",
    "Bat",
    "Cat",
    "Chicken",
    "Cod",
    "Cow",
    "Donkey",
    "Fox",
    "Frog",
    "Glow Squid",
    "Horse",
    "Mooshroom",
    "Mule",
    "Ocelot",
    "Parrot",
    "Pig",
    "Pufferfish",
    "Rabbit",
    "Salmon",
    "Sheep",
    "Skeleton Horse",
    "Snow Golem",
    "Squid",
    "Strider",
    "Tadpole",
    "Tropical Fish",
    "Turtle",
    "Villager",
    "Wandering Trader",
    "Bee",
    "Cave Spider",
    "Dolphin",
    "Enderman",
    "Goat",
    "Iron Golem",
    "Llama",
    "Panda",
    "Piglin",
    "Polar Bear",
    "Spider",
    "Trader Llama",
    "Wolf",
    "Zombified Piglin",
    "Blaze",
    "Chicken Jockey",
    "Creeper",
    "Drowned",
    "Elder Guardian",
    "Endermite",
    "Evoker",
    "Ghast",
    "Guardian",
    "Hoglin",
    "Husk",
    "Magma Cube",
    "Phantom",
    "Piglin Brute",
    "Pillager",
    "Ravager",
    "Shulker",
    "Silverfish",
    "Skeleton",
    "Skeleton Horseman",
    "Slime",
    "Spider Jockey",
    "Stray",
    "Vex",
    "Vindicator",
    "Warden",
    "Witch",
    "Wither Skeleton",
    "Zoglin",
    "Zombie",
    "Zombie Villager",
    "H̴͉͙̠̥̹͕͌̋͐e̸̢̧̟͈͍̝̮̹̰͒̀͌̈̆r̶̪̜͙̗̠̱̲̔̊̎͊̑̑̚o̷̧̮̙̗̖̦̠̺̞̾̓͆͛̅̉̽͘͜͝b̸̨̛̟̪̮̹̿́̒́̀͋̂̎̕͜r̸͖͈͚̞͙̯̲̬̗̅̇̑͒͑ͅi̶̜̓̍̀̑n̴͍̻̘͖̥̩͊̅͒̏̾̄͘͝͝ę̶̥̺̙̰̻̹̓̊̂̈́̆́̕͘͝͝"
]

class Player():

    DEFAULT_EMERALDS = 50

    MIN_EMERALDS = 14
    MAX_EMERALDS = 40

    def __init__(self, name, emeralds=None) -> None:
        self.name = name
        self.balance = self.DEFAULT_EMERALDS if emeralds is None else emeralds
        self.foods = AVLTree()

    def get_balance(self):
        return self.balance

    def get_materials_sold(self):
        return self.materials_sold
    
    def get_foods(self):
        return self.foods

    def set_traders(self, traders_list: list[Trader]) -> None:
        self.traders_list = AVLTree()
        self.traders_key_list = []
        number = 0
        while number < len(traders_list):
            if traders_list[number] not in self.traders_key_list:
                self.traders_list.__setitem__(traders_list[number].get_buy_price(), traders_list[number])
                self.traders_key_list.append(traders_list[number].get_buy_price())
                number += 1
            else:
                traders_list[number].generate_deal()

    def set_foods(self, foods_list: list[Food]) -> None:
        self.foods_list = AVLTree()
        self.foods_key_list = []
        number = 0
        while number < len(foods_list):
            if foods_list[number] not in self.foods_key_list:
                self.foods_list.__setitem__(foods_list[number].get_buy_price(), foods_list[number])
                self.foods_key_list.append(foods_list[number].get_buy_price())
                number += 1
            else:
                foods_list[number].generate_deal()

    @classmethod
    def random_player(self) -> Player:
        name = RandomGen.random_choice(PLAYER_NAMES)
        balance = RandomGen.randint(Player.MIN_EMERALDS, Player.MAX_EMERALDS)

        return Player(name, balance)

    def set_materials(self, materials_list: list[Material]) -> None:
        self.materials_list = materials_list
        
    def set_caves(self, caves_list: list[Cave]) -> None:
        self.caves_list = caves_list
        self.caves_hashed = LinearProbeTable()
        for cave in caves_list:
            self.caves_hashed.__setitem__(cave.get_name(),cave)

    def select_food_and_caves(self) -> tuple[Food | None, float, list[tuple[Cave, float]]]:
        self.foods_key_list.sort(reverse=True)
        food_selected = None
        index = 0
        while food_selected == None:
            food_choice = self.foods.__getitem__(index)
            if self.balance < food_choice.get_buy_price():
                index += 1
            else:
                self.balance -= food_choice.get_buy_price()
                self.hunger_level = food_choice.get_hunger_bars()
                food_selected = food_choice

        self.traders_key_list.sort(reverse=True)
        index = 0

        while self.hunger_level > 0:
            material_to_mine = (self.traders_list.__getitem__(index)).get_material()
            for cave in range(len(self.caves_list)):
                if material_to_mine == self.caves_list[cave].get_material():
                    



        
        return (food_selected, self.balance, self.caves)

    def __str__(self) -> str:
        return f"{self.name} {self.balance}💰"
