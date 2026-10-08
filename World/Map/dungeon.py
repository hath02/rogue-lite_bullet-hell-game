from World.Map.maps import Map


class Dungeon(Map):
    def __init__(self):
        super().__init__(
            tile_paths={
                0: "assets/Tiles/Dungeon/dungeon1.png",
                1: "assets/Tiles/Dungeon/dungeon2.png",
                2: "assets/Tiles/Dungeon/dungeon3.png",
                3: "assets/Tiles/Dungeon/dungeon4.png",
                4: "assets/Tiles/Dungeon/dungeon5.png",
                5: "assets/Tiles/Dungeon/dungeon6.png"
            },

            tile_ids=[
                0,
                1,
                2,
                3,
                4,
                5
            ],

            tile_weights=[
                0.85,
                0.045,
                0.045,
                0.025,
                0.025,
                0.01
            ]
        )