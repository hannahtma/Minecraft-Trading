""" Player class

Instantiates a player that will select caves and foods based on the caves, materials and traders
generated in the game.

"""

from __future__ import annotations
from avl import AVLTree

from cave import Cave
from hash_table import LinearProbeTable
from heap import MaxHeap
from material import Material
from trader import Trader
from food import Food
from random_gen import RandomGen
from node import TreeNode

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
    """
    Player class that stores functions used by a player
    """

    DEFAULT_EMERALDS = 50

    MIN_EMERALDS = 14
    MAX_EMERALDS = 40

    def __init__(self, name, emeralds=None) -> None:
        """
            Instantiates a Player object

            Parameters:
                name: player's name
                emeralds: number of emeralds a player has at the start of a game
        """
        self.name = name
        # if the emeralds is not given, uses default emerald value as balance
        self.balance = self.DEFAULT_EMERALDS if emeralds is None else emeralds
        self.hunger_bars = 0

    def get_name(self):
        """
        Returns name of player

        Complexity: O(1)
        """
        return self.name

    def get_balance(self):
        """
        Returns number of emeralds the player has

        Complexity: O(1)
        """
        return self.balance

    def get_materials_mined(self):
        """
        Returns the list of materials that the player mined

        Complexity: O(1)
        """
        return self.materials_mined
    
    def get_hunger_bars(self):
        """
        Returns the number of hunger bars the player has

        Complexity: O(1)
        """
        return self.hunger_bars
    
    def get_original_hunger_bars(self):
        """
        Returns the original number of hunger bars the player has

        Complexity: O(1)
        """
        return self.original_hunger_bars
    
    def get_foods(self):
        """
        Returns the list of foods

        Complexity: O(1)
        """
        return self.foods
    
    def set_hunger_bars(self, bars) -> None:
        self.hunger_bars -= bars

    def set_traders(self, traders_list: list[Trader]) -> None:
        """
            Sets specific trader lists for players into an AVL
            
            :complexity: O(N) where N is the length of the traders_list
        """
        # we chose to use an AVLTree for convenience of finding the trader with max buy price
        self.traders_list = AVLTree()
        self.traders_key_list = [] # used for convenience of accessing values in the tree
        self.traders_material = [] # compiles the materials that all traders sell
        number = 0
        while number < len(traders_list):
            if traders_list[number].get_buy_price() not in self.traders_key_list:
                # if the trader's buy price doesn't exist in the key list, add trader into the tree
                # we cannot have duplicate keys for AVL as it will cause an error
                self.traders_list.__setitem__(traders_list[number].get_buy_price(),traders_list[number]) 
                self.traders_key_list.append(traders_list[number].get_buy_price())
                self.traders_material.append(traders_list[number].get_material_selected())
                number += 1
            else:
                # if the trader's buy price exists in the key list, regenerate the deal
                traders_list[number].generate_deal()

    def set_foods(self, foods_list: list[Food]) -> None:
        """
            Sets specific food list for players into an AVL

            :complexity: O(N) where N is the length of the foods_list
        """
        # we chose to use an AVLTree for convenience of finding the food with the highest hunger bars level
        self.foods = AVLTree()
        self.foods_key_list = [] # used for convenience of accessing values in the tree
        number = 0
        while number < len(foods_list):
            if foods_list[number].get_hunger_bars() not in self.foods_key_list:
                # if the food's hunger bars doesn't exist in the key list, add food into the tree
                # we cannot have duplicate keys for AVL as it will cause an error
                self.foods.__setitem__(foods_list[number].get_hunger_bars(),foods_list[number])
                self.foods_key_list.append(foods_list[number].get_hunger_bars())
                number += 1
            else:
                # if the food's hunger bars exists in the key list, randomize the food
                foods_list[number].random_food()

    @classmethod
    def random_player(self) -> Player:
        """
            Randomly generates a Player object with name from the list of PLAYER_NAMES and
            balance from range MIN_EMERALDS to MAX_EMERALDS

            Returns:
                - Player object by passing these values to Player class

            :complexity: O(1)
        """
        # randomizes the player name and balance for variety
        name = RandomGen.random_choice(PLAYER_NAMES)
        balance = RandomGen.randint(Player.MIN_EMERALDS, Player.MAX_EMERALDS)

        return Player(name, balance)

    def set_materials(self, materials_list: list[Material]) -> None:
        """
            Sets specific material list for players into an AVL

            :complexity: O(N) where N is the length of the materials_list
        """
        self.materials_list = materials_list
        
    def set_caves(self, caves_list: list[Cave]) -> None:
        """
            Sets specific food list for players into a hash table

            :complexity: O(N) where N is the length of the caves_list
        """
        # saves the list of caves into a hash table with the cave names as the key
        self.caves_list = LinearProbeTable(len(caves_list))
        cave_names = [] # used for convenience of accessing values in the hash table
        number = 0
        while number < len(caves_list):
            if caves_list[number].get_name() not in cave_names:
                # if the cave name doesn't exist in the name list, add cave into the hash table
                # we cannot have duplicate keys for hash tables as it will cause an error
                self.caves_list.__setitem__(caves_list[number].get_name(), caves_list[number])
                cave_names.append(caves_list[number].get_name())
                number += 1
            else:
                # if the cave name exists in the name list, randomize the cave again
                caves_list[number] = caves_list[number].random_cave(self.materials_list)

    def select_food_and_caves(self) -> tuple[Food | None, float, list[tuple[Cave, float]]]:
        """
            1. Choose the food that gives the most hunger bars and deduct the hunger bars
            off the player's hunger bars.
            2. Find which trader has the highest bidding price and get the material name.
            3. Go into the cave which contains the material of highest mining price.
            4. Then, mine all possible material quantity if the player has enough hunger bars.
            5. Steps 2-4 is repeated until the player runs out of hunger bars or there are no more materials that can be mined and sold.

            :complexity: O(T + C + F * log F)
        """      
        # selecting the food to buy
        # best complexity: O(F)
        # worst complexity: O(F * log F)
        # where F is the number of foods there are
        food_selected = None
        self.original_hunger_bars = self.balance
        while food_selected == None: # loops until the player is able to buy a food
            food_choice = (self.foods.get_maximal(self.foods.root)) # finds the food with the highest value of hunger bars
            if self.balance < food_choice.item.get_price(): # if the food is too expensive
                self.foods.__delitem__(food_choice.key) # deletion of an AVLTreeNode is logN
            else: # if the food is purchasable
                self.balance -= food_choice.item.get_price() # pay the money for the food
                self.hunger_bars = food_choice.item.get_hunger_bars() # eat the food
                food_selected = food_choice # food is eaten
        print(food_selected)
        print(self.balance)
        
        # choosing the highest selling material to mine and entering the cave that houses it to mine
        # complexity: O(T + C)
        # where T is the number of traders and C is the number of caves
        self.caves = []
        self.materials_mined = []
        while self.hunger_bars > 0 and self.traders_list.is_empty() == False: # 
            trader_best_price = self.traders_list.get_maximal(self.traders_list.root) # O(T)
            print(trader_best_price)
            self.traders_list.__delitem__(trader_best_price.key) # O(T)
            item_to_buy = (trader_best_price.item).get_material_selected() # O(1)
            cave_values = self.caves_list.values() # list of cave objects O(1)
            for cave in cave_values: # O(C)
                cave_quantity = cave.get_material().get_mining_rate() * cave.get_quantity() # O(1)
                if cave.get_material() == item_to_buy:
                    self.caves.append((cave, cave.get_quantity())) # O(1)
                    if cave_quantity > self.hunger_bars: 
                        how_many_mined = self.hunger_bars / cave.get_material().get_mining_rate() # O(1)
                        self.materials_mined.append((cave, how_many_mined)) # O(1)
                        self.hunger_bars -= item_to_buy.get_mining_rate() * how_many_mined # O(1)
                        self.balance += trader_best_price.item.get_buy_price() * how_many_mined # O(T)
                    else:
                        self.materials_mined.append((cave, cave.get_quantity())) # O(1)
                        self.hunger_bars -= item_to_buy.get_mining_rate() * cave.get_quantity() # O(1)
                        self.balance += trader_best_price.item.get_buy_price() * cave.get_quantity() # O(T)
            print(self.balance)

        return (food_selected, self.balance, self.caves)

    def __str__(self) -> str:
        """
            Returns a string representation of what a player object should look like.
            Includes the player's name and the player's balance.
        """
        return f"{self.name} {self.balance}💰"
