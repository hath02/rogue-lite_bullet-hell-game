from World.Map.__init__ import *

maps = {
    "deserst": {
        "layout": Desert,
        "ambient": "assets/sounds/maps/desert.mp3"
    },
    
    "dungeon": {
        "layout": Dungeon,
        "ambient": "assets/sounds/maps/dungeon.mp3"
    },
    
    "fungu": {
        "layout": Fungu,
        "ambient": "assets/sounds/maps/desert.mp3"
    },
        
    "grassland": {
        "layout": GrassLand,
        "ambient": "assets/sounds/maps/grassland.mp3"
    },
    
    "lab": {
        "layout": Lab,
        "ambient": "assets/sounds/maps/lab.mp3"
    },
    
    "nether": {
        "layout": Nether,
        "ambient": "assets/sounds/maps/desert.mp3"
    }    
}

def get_map(map_name):
    map_data = maps.get(map_name)
    
    if map_data is None:
        raise ValueError(
            f"Unknown map: {map_name}"
        )
        
    return map_data["layout"]()

def get_map_ambient(map_name):
    map_data = maps.get(map_name)
    
    if map_data is None:
        raise ValueError(
            f"Unknown map: {map_name}"
        )
        
    return map_data["ambient"]

def get_map_names():
    return list(maps.keys())