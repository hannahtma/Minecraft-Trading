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

    """
    
    def __init__(self, name: str, mining_rate: float) -> None:
        if name not in RANDOM_MATERIAL_NAMES:
            self.name = Material.random_material()
        else:
            self.name = name
        self.mining_rate = mining_rate

    
    def get_name(self):
        return self.name

    def get_mining_rate(self):
        return self.mining_rate
    
    def __str__(self) -> str:
        material_string = f"{self.name}, {self.mining_rate}"
        return material_string

    @classmethod
    def random_material(cls):
        return Material(RandomGen.random_choice(RANDOM_MATERIAL_NAMES),round(RandomGen.randint(1,50),2))

if __name__ == "__main__":
    print(Material("Coal", 4.5))
    print(len(RANDOM_MATERIAL_NAMES))
