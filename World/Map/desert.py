from World.Map.maps import Map


class Desert(Map):
    def __init__(self):
        super().__init__(
            tile_paths={
                0: "assets/Tiles/Desert/sand1.png",
                1: "assets/Tiles/Desert/sand2.png",
                2: "assets/Tiles/Desert/sand3.png",
                3: "assets/Tiles/Desert/sand4.png",
                4: "assets/Tiles/Desert/sand5.png"
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