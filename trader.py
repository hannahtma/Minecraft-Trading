from __future__ import annotations

from abc import abstractmethod, ABC
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
    
    def __init__(self, name: str) -> None:
        if name not in TRADER_NAMES:
            self.name = Trader.random_trader()
        else:
            self.name = name
        self.key_list = []

    @classmethod
    def random_trader(cls):
        return RandomGen.random_choice(TRADER_NAMES)
    
    def set_all_materials(self, mats: list[Material]) -> None:
        for material in mats:
            self.materials.insert_aux(None,material.get_mining_rate(),material)
            self.key_list.append(material.get_mining_rate())
    
    def add_material(self, mat: Material) -> None:
        self.materials.insert_aux(None,mat.get_mining_rate(),mat)
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

    def __init__(self, name):
        self.trader_name = name
        self.material_selected = Material("",0)
        self.buy_price = 0
        self.materials = AVLTree()
    
    def generate_deal(self) -> None:
        self.material_selected = self.materials.__getitem__(RandomGen.random_choice(self.key_list))
        self.buy_price = round(2 + 8 * RandomGen.random_float(), 2)

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
        return f"<RandomTrader: {self.trader_name} buying [{self.material_selected.get_name()}: {self.material_selected.get_mining_rate}🍗/💎] for {self.buy_price}💰>"

class RangeTrader(Trader):

    def __init__(self, name):
        self.trader_name = name
        self.material_selected = Material("",0)
        self.buy_price = 0
        self.materials = AVLTree()

    def generate_deal(self) -> None:
        i = RandomGen.randint(1,self.materials.__len__())
        j = RandomGen.randint(i,self.materials.__len__())
        self.material_selected = RandomGen.random_choice(self.materials_between(i,j))
        self.buy_price = round(2 + 8 * RandomGen.random_float(), 2)
    
    def materials_between(self, i: int, j: int) -> list[Material]:
        self.key_list.sort()
        return self.materials.range_between(self.key_list[i-1],self.key_list[j-1])

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
        return f"<RangeTrader: {self.trader_name} buying [{self.material_selected.get_name()}: {self.material_selected.get_mining_rate}🍗/💎] for {self.buy_price}💰>"

class HardTrader(Trader):

    def __init__(self, name):
        self.trader_name = name
        self.material_selected = Material("",0)
        self.buy_price = 0
        self.materials = AVLTree()
    
    def generate_deal(self) -> None:
        self.material_selected = self.materials.get_maximal(self.materials.get_root())
        self.materials.__delitem__(self.material_selected.key)
        self.buy_price = round(2 + 8 * RandomGen.random_float(), 2)

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
        return f"<HardTrader: {self.trader_name} buying [{self.material_selected.get_name()}: {self.material_selected.get_mining_rate}🍗/💎] for {self.buy_price}💰>"

if __name__ == "__main__":
    trader = RangeTrader("Jackson")
    print(trader)
    trader.set_materials([
        Material("Coal", 4.5),
        Material("Diamonds", 3),
        Material("Redstone", 20),
    ])
    trader.generate_deal()
    print(trader)
    trader.stop_deal()
    print(trader)

