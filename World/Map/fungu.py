from World.Map.maps import Map


class Fungu(Map):
    def __init__(self):
        super().__init__(
            tile_paths={
                0: "assets/Tiles/Fungu/fungu1.png",
                1: "assets/Tiles/Fungu/fungu2.png",
                2: "assets/Tiles/Fungu/fungu3.png",
                3: "assets/Tiles/Fungu/fungu4.png",
                4: "assets/Tiles/Fungu/fungu5.png"
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