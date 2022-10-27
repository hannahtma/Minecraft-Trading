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
    
    def __init__(self, name: str = None) -> None:
        if name == None:
            self.name = RandomGen.random_choice(TRADER_NAMES)
        else:
            self.name = name

    @classmethod
    def random_trader(cls):
        return RandomGen.random_choice([RandomTrader(),RangeTrader(),HardTrader()])
    
    def set_all_materials(self, mats: list[Material]) -> None:
        self.materials = AVLTree()
        self.key_list = []
        for material in mats:
            self.materials.__setitem__(material.get_mining_rate(),material)
            self.key_list.append(material.get_mining_rate())
    
    def add_material(self, mat: Material) -> None:
        self.materials.__setitem__(mat.get_mining_rate(),mat)
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

    def stop_deal(self) -> None:
        self.deal = None
    
    @abstractmethod
    def __str__(self) -> str:
        pass

class RandomTrader(Trader):

    def __init__(self, name=None):
        self.trader_name = name
        self.material_selected = Material("",0)
        self.buy_price = 0
        self.materials = AVLTree()
        self.key_list = []
        self.deal = None
    
    def get_buy_price(self):
        return self.buy_price
    
    def get_selected_material(self):
        return self.material_selected
    
    def generate_deal(self) -> None:
        self.material_selected = self.materials.__getitem__(RandomGen.random_choice(self.key_list))
        self.buy_price = round(2 + 8 * RandomGen.random_float(), 2)
        self.current_deal()

    def current_deal(self) -> tuple[Material, float]:
        if self.material_selected == Material("",0) or self.buy_price == 0:
            raise ValueError("The deal has not been generated")
        self.deal = tuple((self.material_selected, self.buy_price))
        return self.deal

    def is_currently_selling(self) -> bool:
        if self.deal != None:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"<RandomTrader: {self.trader_name} buying [{self.material_selected.get_name()}: {self.material_selected.get_mining_rate()}🍗/💎] for {self.buy_price}💰>"

class RangeTrader(Trader):

    def __init__(self, name=None):
        self.trader_name = name
        self.material_selected = Material("",0)
        self.buy_price = 0
        self.materials = AVLTree()
        self.key_list = []
        self.deal = None

    def get_buy_price(self):
        return self.buy_price
    
    def get_selected_material(self):
        return self.material_selected

    def generate_deal(self) -> None:
        if self.materials.__len__() <= 1:
            self.material_selected = self.materials.__getitem__(self.key_list[0])
        else:
            i = RandomGen.randint(0,self.materials.__len__()-1)
            j = RandomGen.randint(i,self.materials.__len__()-1)
            self.material_selected = RandomGen.random_choice(self.materials_between(i,j))
        self.buy_price = round(2 + 8 * RandomGen.random_float(), 2)
        self.current_deal()
    
    def materials_between(self, i: int, j: int) -> list[Material]:
        the_list = []
        for index in range(j-i+1):
            the_list.append(self.materials.__getitem__(self.key_list[i+index]))
        return the_list

    def current_deal(self) -> tuple[Material, float]:
        if self.material_selected == Material("",0) or self.buy_price == 0:
            raise ValueError("The deal has not been generated")
        self.deal = tuple((self.material_selected, self.buy_price))
        return self.deal

    def is_currently_selling(self) -> bool:
        if self.deal != None:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"<RangeTrader: {self.trader_name} buying [{self.material_selected.get_name()}: {self.material_selected.get_mining_rate()}🍗/💎] for {self.buy_price}💰>"

class HardTrader(Trader):

    def __init__(self, name=None):
        self.trader_name = name
        self.material_selected = Material("",0)
        self.buy_price = 0
        self.materials = AVLTree()
        self.key_list = []
        self.deal = None

    def get_buy_price(self):
        return self.buy_price
    
    def get_selected_material(self):
        return self.material_selected
    
    def generate_deal(self) -> None:
        self.material_selected = (self.materials.get_maximal(self.materials.root)).item
        self.materials.__delitem__(self.material_selected.get_mining_rate())
        self.buy_price = round(2 + 8 * RandomGen.random_float(), 2)
        self.current_deal()

    def current_deal(self) -> tuple[Material, float]:
        if self.material_selected == Material("",0) or self.buy_price == 0:
            raise ValueError("The deal has not been generated")
        self.deal = tuple((self.material_selected, self.buy_price))
        return self.deal

    def is_currently_selling(self) -> bool:
        if self.deal != None:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"<HardTrader: {self.trader_name} buying [{self.material_selected.get_name()}: {self.material_selected.get_mining_rate()}🍗/💎] for {self.buy_price}💰>"

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
