import pygame, random

from settings import TILE_SIZE

class Chunks:
    def __init__(
        self, 
        width, 
        height,
        tile_ids,
        tile_weights
    ):
        
        self.width = width
        self.height = height
        
        self.tile_ids = tile_ids
        self.tile_weights = tile_weights

        self.tiles = []
        
        self.generate()
        
    def generate(self):
        self.tiles = []
        
        for y in range(self.height):
            row = []
            
            for x in range(self.width):
                tile_id = random.choices(
                    self.tile_ids,                          # Randomly choose between the available tile IDs
                    weights = self.tile_weights             # Adjust the weights to control the frequency of each tile
                )[0]                                        # Get the first element of the array returned by random.choices()
                
                row.append(tile_id)
                
            self.tiles.append(row)
    
class Map:
    def __init__(
        self,
        tile_paths,
        tile_ids,
        tile_weights,
        chunk_width = 8,
        chunk_height = 8
    ):
        # Chunks settings
        self.chunk_width = chunk_width
        self.chunk_height = chunk_height
        
        self.chunk_pixel_width = (
            self.chunk_width * TILE_SIZE
        )
        
        self.chunk_pixel_height = (
            self.chunk_height * TILE_SIZE
        )
        
        # Generate chunks
        self.chunks = {}
        
        self.tile_ids = tile_ids
        self.tile_weights = tile_weights
        
        # Load the tile image
        self.tileset = self.load_tiles(tile_paths)
    
    # Load all tiles
    def load_tiles(self, tile_paths):
        tiles = {}
        
        for tile_id, path in tile_paths.items():
            image = pygame.image.load(path).convert_alpha()
            
        # Source artwork is 64x64
        # Scale it to the desired tile size
            image = pygame.transform.scale(
                image, 
                (TILE_SIZE, TILE_SIZE)
            )
            
            tiles[tile_id] = image
            
        return tiles
    
    # Get chunks
    def get_chunk(self, chunk_x, chunk_y):
        position = (
            chunk_x,
            chunk_y
        )
        
        # Return the chunk if it already exists, otherwise generate a new one
        if position in self.chunks:
            return self.chunks[position]
        
        # Generate a new chunk based on the chunk coordinates
        chunk = Chunks(
            self.chunk_width, 
            self.chunk_height,
            self.tile_ids,
            self.tile_weights
        )
        
        self.chunks[position] = chunk
        
        return chunk
    
    # Player chunks
    def get_player_chunk(self, player_position):
        chunk_x = int(
            player_position.x 
            // self.chunk_pixel_width
        )
        
        chunk_y = int(
            player_position.y 
            // self.chunk_pixel_height
        )
        
        return chunk_x, chunk_y
    
    def update(self, player):
        player_chunk_x, player_chunk_y = (
            self.get_player_chunk(player.position)
        )
        
        # Generate 3x3 chunks around the player
        for y in range(
            player_chunk_y - 1, 
            player_chunk_y + 2
        ):
            for x in range(
                player_chunk_x - 1, 
                player_chunk_x + 2
            ):
                self.get_chunk(x, y)
        
    def draw(self, screen, camera):
        for (chunk_x, chunk_y), chunk in self.chunks.items():
            
            # World position of the chunk
            chunk_world_x = (
                chunk_x 
                * self.chunk_pixel_width
            )
            
            chunk_world_y = (
                chunk_y 
                * self.chunk_pixel_height
            )
            
            # Draw every tile in the chunk
            for y in range(chunk.height):
                for x in range(chunk.width):
                    
                    tile_id = chunk.tiles[y][x]
                    
                    tile = self.tileset[tile_id]
                    
                    # Tile world position
                    world_x = (
                        chunk_world_x 
                        + x * TILE_SIZE
                    )
                    
                    world_y = (
                        chunk_world_y 
                        + y * TILE_SIZE
                    )
                    
                    # Convert world position to screen position
                    screen_position = camera.apply(
                        pygame.Vector2(
                            world_x, 
                            world_y
                        )
                    )
                    
                    screen.blit(
                        tile, 
                        screen_position
                    )