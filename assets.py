import pygame

_images = {}
_sounds = {}


def load_image(path, size=None):
    """Load an image once. Same (path, size) returns the same Surface."""
    key = (path, size)
    img = _images.get(key)

    if img is None:
        print("[assets] loading", key)   # temporary, for testing
        img = pygame.image.load(path).convert_alpha()

        if size is not None:
            img = pygame.transform.scale(img, size)

        _images[key] = img

    return img


def load_frames(paths, size=None):
    """Returns a new list each time, but the Surfaces inside are shared."""
    return [load_image(p, size) for p in paths]


def load_sound(path):
    snd = _sounds.get(path)

    if snd is None:
        snd = pygame.mixer.Sound(path)
        _sounds[path] = snd

    return snd