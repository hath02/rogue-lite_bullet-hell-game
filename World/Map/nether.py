from World.Map.maps import Map


class Nether(Map):
    def __init__(self):
        super().__init__(
            tile_paths={
                0: "assets/Tiles/Nether/nether1.png",
                1: "assets/Tiles/Nether/nether2.png",
                2: "assets/Tiles/Nether/nether3.png",
                3: "assets/Tiles/Nether/nether4.png",
                4: "assets/Tiles/Nether/nether5.png"
            },

            tile_ids=[
                0,
                1,
                2,
                3,
                4
            ],

            tile_weights=[
                0.2,
                0.2,
                0.2,
                0.2,
                0.2
            ]
        )