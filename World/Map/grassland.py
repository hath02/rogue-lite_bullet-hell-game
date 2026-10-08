from World.Map.maps import Map


class GrassLand(Map):
    def __init__(self):
        super().__init__(
            tile_paths={
                0: "assets/Tiles/GrassLand/grass1.png",
                1: "assets/Tiles/GrassLand/grass2.png",
                2: "assets/Tiles/GrassLand/grass3.png",
                3: "assets/Tiles/GrassLand/grass4.png",
                4: "assets/Tiles/GrassLand/grass5.png"
            },

            tile_ids=[
                0,
                1,
                2,
                3,
                4
            ],

            tile_weights=[
                0.9,
                0.026,
                0.025,
                0.025,
                0.024
            ]
        )