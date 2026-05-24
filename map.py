import pytmx
import constants
import pygame

tile_cache = {}

def get_scaled_tile(tile, size):

    key = (id(tile), size)

    if key not in tile_cache:

        tile_cache[key] = pygame.transform.scale(tile, size)

    return tile_cache[key]

def draw_map(tmx_data, window, camera_x, camera_y):

    for layer in tmx_data.visible_layers:

        if isinstance(layer, pytmx.TiledTileLayer):

            for x, y, gid in layer:

                tile = tmx_data.get_tile_image_by_gid(gid)

                if tile:

                    scaled_tile = get_scaled_tile(
                        tile,
                        (
                            tmx_data.tilewidth * constants.SCALE_MAP,
                            tmx_data.tileheight * constants.SCALE_MAP
                        )
                    )

                    world_x = x * tmx_data.tilewidth * constants.SCALE_MAP
                    world_y = y * tmx_data.tileheight * constants.SCALE_MAP

                    window.blit(
                        scaled_tile,
                        (
                            world_x - camera_x,
                            world_y - camera_y
                        )
                    )

def load_collisions(tmx_data):

    collision_rects = []

    for obj in tmx_data.get_layer_by_name("Collisions"):

        rect = pygame.Rect(
            obj.x * constants.SCALE_MAP,
            obj.y * constants.SCALE_MAP,
            obj.width * constants.SCALE_MAP,
            obj.height * constants.SCALE_MAP
        )

        collision_rects.append(rect)
    return collision_rects

def draw_colliders(collision_rects, window, camera_x, camera_y):
    for rect in collision_rects:

        pygame.draw.rect(
            window,
            (255, 0, 0),
            (
                rect.x - camera_x,
                rect.y - camera_y,
                rect.width,
                rect.height
            ),
            2
        )