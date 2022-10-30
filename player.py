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

    DEFAULT_EMERALDS = 50

    MIN_EMERALDS = 14
    MAX_EMERALDS = 40

    def __init__(self, name, emeralds=None) -> None:
        """
            Instantiates a Player object

            Parameters:
                name: player's name
                emeralds: number of emeralds a player has
        """
        self.name = name
        self.balance = self.DEFAULT_EMERALDS if emeralds is None else emeralds
        self.hunger_bars = 0

    def get_name(self):
        return self.name

    def get_balance(self):
        return self.balance

    def get_materials_sold(self):
        return self.materials_sold
    
    def get_hunger_bars(self):
        return self.hunger_bars
    
    def get_foods(self):
        return self.foods

    def set_traders(self, traders_list: list[Trader]) -> None:
        """
            Sets specific trader lists for players into an AVL
            
            :complexity: O(N) where N is the length of the traders_list
        """
        self.traders_list = AVLTree()
        self.traders_key_list = []
        number = 0
        while number < len(traders_list):
            if traders_list[number].get_buy_price() not in self.traders_key_list:
                self.traders_list.__setitem__(traders_list[number].get_buy_price(),traders_list[number]) 
                self.traders_key_list.append(traders_list[number].get_buy_price())
                number += 1
            else:
                traders_list[number].generate_deal()

    def set_foods(self, foods_list: list[Food]) -> None:
        """
            Sets specific food list for players into an AVL

            :complexity: O(N) where N is the length of the foods_list
        """
        self.foods = AVLTree()
        self.foods_key_list = []
        number = 0
        while number < len(foods_list):
            if foods_list[number].get_hunger_bars() not in self.foods_key_list:
                self.foods.__setitem__(foods_list[number].get_hunger_bars(),foods_list[number])
                self.foods_key_list.append(foods_list[number].get_hunger_bars())
                number += 1
            else:
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
        self.caves_list = LinearProbeTable(len(caves_list))
        for cave in caves_list:
            self.caves_list.__setitem__(cave.get_name(), cave)

    def select_food_and_caves(self) -> tuple[Food | None, float, list[tuple[Cave, float]]]:
        """
            1. Choose the food that gives the most hunger bars and deduct the hunger bars
            off the player's hunger bars.
            2. Find which trader has the highest bidding price and get the material name.
            3. Go into the cave which contains the material the player wishes to mine.
            4. Then, mine all possible material quantity if the player has enough hunger bars.
            5. Steps 2-4 is repeated until the player runs out of hunger bars.

            :complexity: O(N)
        """      
        self.caves = []
        food_choice = self.foods.get_maximal(self.foods.root)
        print("food choice", food_choice)

        self.hunger_bars = food_choice.item.get_hunger_bars()
        # self.hunger_bars -= food_choice
        self.balance -= food_choice.item.get_price()
        print("hunger bars", self.hunger_bars)
        print("balance: ", self.balance)

        self.materials_sold = []
        print(self.traders_list.is_empty())
        while self.hunger_bars > 0 and self.traders_list.is_empty() == False and len(self.materials_sold) <= len(self.caves):
            print("current self.hunger_bars:", self.hunger_bars)
            print("current self.balance:", self.balance)

            best_price = self.traders_list.get_maximal(self.traders_list.root)
            # self.traders_list.__delitem__(best_price.key)
            # for x in self.traders_list:
            #     print("trader",x)
            print("best price: ", best_price)

            item_to_buy = best_price.item.get_selected_material()
            print("item to buy: ", item_to_buy)

            # print("this is self.caves_list: ")
            # print("here",type(self.caves_list))
            cave_values = self.caves_list.values()
            print(cave_values)
            # for cave in self.caves_list:

            # ignore this
            


            profit_heap = MaxHeap(len(cave_values))
            cost_heap = MaxHeap(len(cave_values))
            for cave in cave_values:
                the_profit = best_price.item.get_buy_price() * cave.get_quantity()
                at_what_cost = cave.get_material().get_mining_rate() * cave.get_quantity()
                profit_heap.add(the_profit)
                cost_heap.add(at_what_cost)
                self.materials_sold.append((cave, cave.get_quantity()))
                # self.caves.append(cave)

            max_profit = profit_heap.get_max()
            print("current max profit",max_profit)
            hunger_cost = cost_heap.get_max()
            print("current hunger cost",hunger_cost)
            while self.hunger_bars - hunger_cost > 0:
                self.hunger_bars -= hunger_cost
                print("after buying: ", self.hunger_bars)
                self.balance += max_profit
                print("after selling",self.balance)
                max_profit = profit_heap.get_max()
                print("current max profit",max_profit)
                hunger_cost = cost_heap.get_max()
                print("current hunger cost",hunger_cost)
            print("how many hunger bars left?",self.hunger_bars)
            #     print("the cave",cave)
            #     if cave.get_material() == item_to_buy:
            #         cave_index = cave_values.index(cave)
            #         self.caves.append((cave_values[cave_index], cave_values[cave_index].get_quantity()))
            #         quantity_bought = 0
            #         while self.hunger_bars - item_to_buy.get_mining_rate() > 0:
            #             self.hunger_bars -= item_to_buy.get_mining_rate()
            #             print("after purchase: ", self.hunger_bars)
            #             self.balance += best_price.item.get_buy_price()
            #             quantity_bought += 1
            #             break
            #         self.materials_sold.append((cave, quantity_bought))
            #         quantity_bought = 0
            # break

        return (food_choice, self.balance, self.caves)

    def __str__(self) -> str:
        """
            Returns a string representation of what a player object should look like.
            Includes the player's name and the player's balance.
        """
        return f"{self.name} {self.balance}💰"
