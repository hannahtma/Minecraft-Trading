from random_gen import RandomGen

# Material names taken from https://minecraft-archive.fandom.com/wiki/Items
RANDOM_MATERIAL_NAMES = [
    "Arrow",
    "Axe",
    "Bow",
    "Bucket",
    "Carrot on a Stick",
    "Clock",
    "Compass",
    "Crossbow",
    "Exploration Map",
    "Fire Charge",
    "Fishing Rod",
    "Flint and Steel",
    "Glass Bottle",
    "Dragon's Breath",
    "Hoe",
    "Lead",
    "Map",
    "Pickaxe",
    "Shears",
    "Shield",
    "Shovel",
    "Sword",
    "Saddle",
    "Spyglass",
    "Totem of Undying",
    "Blaze Powder",
    "Blaze Rod",
    "Bone",
    "Bone meal",
    "Book",
    "Book and Quill",
    "Enchanted Book",
    "Bowl",
    "Brick",
    "Clay",
    "Coal",
    "Charcoal",
    "Cocoa Beans",
    "Copper Ingot",
    "Diamond",
    "Dyes",
    "Ender Pearl",
    "Eye of Ender",
    "Feather",
    "Spider Eye",
    "Fermented Spider Eye",
    "Flint",
    "Ghast Tear",
    "Glistering Melon",
    "Glowstone Dust",
    "Gold Ingot",
    "Gold Nugget",
    "Gunpowder",
    "Ink Sac",
    "Iron Ingot",
    "Iron Nugget",
    "Lapis Lazuli",
    "Leather",
    "Magma Cream",
    "Music Disc",
    "Name Tag",
    "Nether Bricks",
    "Paper",
    "Popped Chorus Fruit",
    "Prismarine Crystal",
    "Prismarine Shard",
    "Rabbit's Foot",
    "Rabbit Hide",
    "Redstone",
    "Seeds",
    "Beetroot Seeds",
    "Nether Wart Seeds",
    "Pumpkin Seeds",
    "Wheat Seeds",
    "Slimeball",
    "Snowball",
    "Spawn Egg",
    "Stick",
    "String",
    "Wheat",
    "Netherite Ingot",
]

class Material:
    """
    Creates materials in a certain format
    """
    
    def __init__(self, name: str, mining_rate: float) -> None:
        """
        Initialises variables

        Parameters:
            name - Name of the material
            mining_rate - How much hunger bars it takes to mine the material

        Complexity: O(1)
        """
        if name == None or mining_rate == None:
            self.random_material()
        self.name = name
        self.mining_rate = mining_rate

    def get_mining_rate(self):
        """
        Getter for mining rate

        Complexity: O(1)
        """
        return self.mining_rate

    def get_name(self):
        """
        Getter for name

        Complexity: O(1)
        """
        return self.name
    
    def __str__(self) -> str:
        """
        Creates a string representation of the class

        Complexity: O(1)
        """
        return f"{self.name} {self.mining_rate}"

    @classmethod
    def random_material(cls):
        """
        Randomizes a material and it's mining rate

        Complexity: O(1)
        """
        return Material(RandomGen.random_choice(RANDOM_MATERIAL_NAMES),round(RandomGen.random_float(),2))

if __name__ == "__main__":
    print(Material.random_material())
