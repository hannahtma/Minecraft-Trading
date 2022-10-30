""" Trader

Trader ADT and the 3 subclasses (RandomTrader, RangeTrader, HardTrader)
"""
from __future__ import annotations

from abc import abstractmethod, ABC
from random import Random
from unicodedata import name
from material import Material
from random_gen import RandomGen
from avl import AVLTree

# Generated with https://www.namegenerator.co/real-names/english-name-generator
TRADER_NAMES = [
    "Pierce Hodge",
    "Loren Calhoun",
    "Janie Meyers",
    "Ivey Hudson",
    "Rae Vincent",
    "Bertie Combs",
    "Brooks Mclaughlin",
    "Lea Carpenter",
    "Charlie Kidd",
    "Emil Huffman",
    "Letitia Roach",
    "Roger Mathis",
    "Allie Graham",
    "Stanton Harrell",
    "Bert Shepherd",
    "Orson Hoover",
    "Lyle Randall",
    "Jo Gillespie",
    "Audie Burnett",
    "Curtis Dougherty",
    "Bernard Frost",
    "Jeffie Hensley",
    "Rene Shea",
    "Milo Chaney",
    "Buck Pierce",
    "Drew Flynn",
    "Ruby Cameron",
    "Collie Flowers",
    "Waldo Morgan",
    "Winston York",
    "Dollie Dickson",
    "Etha Morse",
    "Dana Rowland",
    "Eda Ryan",
    "Audrey Cobb",
    "Madison Fitzpatrick",
    "Gardner Pearson",
    "Effie Sheppard",
    "Katherine Mercer",
    "Dorsey Hansen",
    "Taylor Blackburn",
    "Mable Hodge",
    "Winnie French",
    "Troy Bartlett",
    "Maye Cummings",
    "Charley Hayes",
    "Berta White",
    "Ivey Mclean",
    "Joanna Ford",
    "Florence Cooley",
    "Vivian Stephens",
    "Callie Barron",
    "Tina Middleton",
    "Linda Glenn",
    "Loren Mcdaniel",
    "Ruby Goodman",
    "Ray Dodson",
    "Jo Bass",
    "Cora Kramer",
    "Taylor Schultz",
]

class Trader(ABC):
    """
    Trader ADT class that has 3 different sub-classes
    """
    
    def __init__(self, name: str = None) -> None:
        """
        Initialises variables

        Parameters:
            name - Name of the trader

        Complexity: O(1)
        """
        if name == None: 
        # When a trader name is not given, a name is chosen from the original list
            self.name = RandomGen.random_choice(TRADER_NAMES)
        else:
            self.name = name

    @classmethod
    def random_trader(cls):
        """
        Randomizes the type of trader

        Complexity: O(1)
        """
        return RandomGen.random_choice([RandomTrader(),RangeTrader(),HardTrader()])
    
    def set_all_materials(self, mats: list[Material]) -> None:
        """
        Resets all the materials a trader has

        Parameters:
            mats - A list of materials to set under the trader

        Complexity: O(n), where n is the length of mats
        """
        self.materials = AVLTree() # creates a new materials AVL Tree
        self.key_list = [] # empties the key list
        for material in mats:
            # sets the mining rate as the key of the node and the material class as the item of the node
            self.materials.__setitem__(material.get_mining_rate(),material) 
            # the key list to keep track of the keys
            self.key_list.append(material.get_mining_rate())
    
    def add_material(self, mat: Material) -> None:
        """
        Adds a material to the AVL Tree

        Parameters:
            mat - A material to be added to the materials list

        Complexity: O(1)
        """
        # sets the mining rate as the key of the node and the material class as the item of the node
        self.materials.__setitem__(mat.get_mining_rate(),mat)
        # the key list to keep track of the keys
        self.key_list.append(mat.get_mining_rate())
    
    @abstractmethod
    def is_currently_selling(self) -> bool:
        pass

    @abstractmethod
    def current_deal(self) -> tuple[Material, float]:
        pass
    
    @abstractmethod
    def generate_deal(self) -> None:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_buy_price(self) -> float:
        pass

    @abstractmethod
    def get_material_selected(self) -> Material:
        pass

    def stop_deal(self) -> None:
        """
        Ends the trader's current deal

        Complexity: O(1)
        """
        self.deal = None
    
    @abstractmethod
    def __str__(self) -> str:
        pass

class RandomTrader(Trader):
    """
    Trader that randomly selects the material to sell
    """

    def __init__(self, name=None):
        """
        Initialises variables

        Parameters:
            name - Name of the trader
        """
        if name == None:
            self.name = RandomGen.random_choice(TRADER_NAMES)
        else:
            self.name = name

        self.material_selected = Material("",0)
        self.buy_price = 0
        self.materials = AVLTree()
        self.key_list = []
        self.deal = None
    
    def generate_deal(self) -> None:
        """
        Generates a deal by randomly selecting a material and generating a buy price

        Complexity: O(1)
        """
        # Randomly choose a key and gets the material from the tree node
        self.material_selected = self.materials.__getitem__(RandomGen.random_choice(self.key_list))
        # Generates the buy price
        self.buy_price = round(2 + 8 * RandomGen.random_float(), 2)
        # Calls current deal to set the deal
        self.current_deal()

    def current_deal(self) -> tuple[Material, float]:
        """
        Sets the deal into a tuple form after generating

        Complexity: O(1)
        """
        # If deal has not been generated, raises error
        if self.material_selected == Material("",0) or self.buy_price == 0:
            raise ValueError("The deal has not been generated")
        # Sets the deal into a tuple
        self.deal = tuple((self.material_selected, self.buy_price))
        return self.deal

    def is_currently_selling(self) -> bool:
        """
        Checks if the deal is still ongoing

        Complexity: O(1)
        """
        # if there is a deal, return true. Else false
        if self.deal != None:
            return True
        else:
            return False

    def get_name(self) -> str:
        """
        Returns the trader name

        Complexity: O(1)
        """
        return self.name

    def get_buy_price(self) -> float:
        """
        Return the price they will buy the material for

        Complexity: O(1)
        """
        return self.buy_price

    def get_material_selected(self) -> Material:
        """
        Returns the material they chose to sell

        Complexity: O(1)
        """
        return self.material_selected

    def __str__(self) -> str:
        """
        Returns a string representation of the Random Trader

        Complexity: O(1)
        """
        return f"<RandomTrader: {self.name} buying [{self.material_selected.get_name()}: {self.material_selected.get_mining_rate()}🍗/💎] for {self.buy_price}💰>"

class RangeTrader(Trader):
    """
    Trader that selects the material from a range of mining rates to sell
    """

    def __init__(self, name=None):
        """
        Initialises variables

        Parameters:
            name - Name of the trader
        """
        if name == None:
            self.name = RandomGen.random_choice(TRADER_NAMES)
        else:
            self.name = name
        self.material_selected = Material("",0)
        self.buy_price = 0
        self.materials = AVLTree()
        self.key_list = []
        self.deal = None

    def generate_deal(self) -> None:
        """
        Generates a deal by randomly selecting a material and generating a buy price

        Complexity: O(j-i), due to materials_between being called
        """
        if self.materials.__len__() <= 1: # if the material list is not more than 1
            # sets the material chosen to the only one in the list
            self.material_selected = self.materials.__getitem__(self.key_list[0])
        else:
            # randomly generates the i and j
            i = RandomGen.randint(0,self.materials.__len__()-1)
            j = RandomGen.randint(i,self.materials.__len__()-1)
            # chooses the material from the ranged list
            self.material_selected = RandomGen.random_choice(self.materials_between(i,j))
        # Generates the buy price
        self.buy_price = round(2 + 8 * RandomGen.random_float(), 2)
        # Calls current deal to set the deal
        self.current_deal()
    
    def materials_between(self, i: int, j: int) -> list[Material]:
        """
        Returns a list of materials within the range of ith index and jth index easiest to mine

        Parameters:
            i - the lower bound index
            j - the upper bound index

        Complexity: O(j-i), loops for that amount of times
        """
        # initialises an empty list
        the_list = []
        # sets the limit to j-i+1 because for loop range upper bound is not inclusive
        for index in range(j-i+1):
            # appends the material of that index to the list
            the_list.append(self.materials.__getitem__(self.key_list[i+index]))

        return the_list

    def current_deal(self) -> tuple[Material, float]:
        """
        Sets the deal into a tuple form after generating

        Complexity: O(1)
        """
        # If deal has not been generated, raises error
        if self.material_selected == Material("",0) or self.buy_price == 0:
            raise ValueError("The deal has not been generated")
        # Sets the deal into a tuple
        self.deal = tuple((self.material_selected, self.buy_price))
        return self.deal

    def is_currently_selling(self) -> bool:
        """
        Checks if the deal is still ongoing

        Complexity: O(1)
        """
        # if there is a deal, return true. Else false
        if self.deal != None:
            return True
        else:
            return False

    def get_name(self) -> str:
        """
        Returns the trader name

        Complexity: O(1)
        """
        return self.name

    def get_buy_price(self) -> float:
        """
        Return the price they will buy the material for

        Complexity: O(1)
        """
        return self.buy_price

    def get_material_selected(self) -> Material:
        """
        Returns the material they chose to sell

        Complexity: O(1)
        """
        return self.material_selected

    def __str__(self) -> str:
        """
        Returns a string representation of the Random Trader

        Complexity: O(1)
        """
        return f"<RangeTrader: {self.name} buying [{self.material_selected.get_name()}: {self.material_selected.get_mining_rate()}🍗/💎] for {self.buy_price}💰>"

class HardTrader(Trader):
    """
    Trader that selects the material with highest mining rate to sell
    """

    def __init__(self, name=None):
        """
        Initialises variables

        Parameters:
            name - Name of the trader
        """
        if name == None:
            self.name = RandomGen.random_choice(TRADER_NAMES)
        else:
            self.name = name
        self.material_selected = Material("",0)
        self.buy_price = 0
        self.materials = AVLTree()
        self.key_list = []
        self.deal = None
    
    def generate_deal(self) -> None:
        """
        Generates a deal by randomly selecting a material and generating a buy price

        Complexity: O(1)
        """
        # gets the material that has the highest mining rate
        self.material_selected = (self.materials.get_maximal(self.materials.get_root())).item
        # deletes the material from the tree
        self.materials.__delitem__(self.material_selected.get_mining_rate())
        # Generates the buy price
        self.buy_price = round(2 + 8 * RandomGen.random_float(), 2)
        # Calls current deal to set the deal
        self.current_deal()

    def current_deal(self) -> tuple[Material, float]:
        """
        Sets the deal into a tuple form after generating

        Complexity: O(1)
        """
        # If deal has not been generated, raises error
        if self.material_selected == Material("",0) or self.buy_price == 0:
            raise ValueError("The deal has not been generated")
        # Sets the deal into a tuple
        self.deal = tuple((self.material_selected, self.buy_price))
        return self.deal

    def is_currently_selling(self) -> bool:
        """
        Checks if the deal is still ongoing

        Complexity: O(1)
        """
        # if there is a deal, return true. Else false
        if self.deal != None:
            return True
        else:
            return False

    def get_name(self) -> str:
        """
        Returns the trader name

        Complexity: O(1)
        """
        return self.name

    def get_buy_price(self) -> float:
        """
        Return the price they will buy the material for

        Complexity: O(1)
        """
        return self.buy_price

    def get_material_selected(self) -> Material:
        """
        Returns the material they chose to sell

        Complexity: O(1)
        """
        return self.material_selected

    def __str__(self) -> str:
        """
        Returns a string representation of the Random Trader

        Complexity: O(1)
        """
        return f"<HardTrader: {self.name} buying [{self.material_selected.get_name()}: {self.material_selected.get_mining_rate()}🍗/💎] for {self.buy_price}💰>"

if __name__ == "__main__":
    RandomGen.set_seed(16)
    rando = RangeTrader("Mr Barnes")
    rando.add_material(Material("Amethyst", 1))
    rando.add_material(Material("Emerald", 2))
    rando.add_material(Material("Ruby", 3))
    rando.add_material(Material("Diamond", 4))
    rando.add_material(Material("Arrow", 5))
    rando.add_material(Material("Clock", 6))
    rando.add_material(Material("Pickaxe", 7))
    rando.add_material(Material("Gunpowder", 8))

    rando.generate_deal()
    print(rando)


