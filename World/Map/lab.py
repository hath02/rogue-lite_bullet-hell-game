from World.Map.maps import Map


class Lab(Map):
    def __init__(self):
        super().__init__(
            tile_paths={
                0: "assets/Tiles/Lab/lab1.png",
                1: "assets/Tiles/Lab/lab2.png",
                2: "assets/Tiles/Lab/lab3.png",
                3: "assets/Tiles/Lab/lab4.png",
                4: "assets/Tiles/Lab/lab5.png"
            },

            tile_ids=[
                0,
                1,
                2,
                3,
                4
            ],

            tile_weights=[
                0.4,
                0.01,
                0.45,
                0.012,
                0.02
            ]
        )