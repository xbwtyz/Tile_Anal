from PIL import Image
import sys

def find_grid_color(image):
    width, height = image.size
    for x in range(width):
        color = image.getpixel((x, 0))
        if all(image.getpixel((x, y)) == color for y in range(1, height)):
            return color
    return None

def detect_tile_dimensions(image, grid_color):
    width, height = image.size

    def detect_dimension(coord, max_value, is_line):
        size = 1
        while coord + size < max_value and is_line(coord + size, grid_color):
            size += 1
        return size

    tile_width = detect_dimension(0, width, lambda x, gc: image.getpixel((x, 0)) != gc)
    tile_height = detect_dimension(0, height, lambda y, gc: image.getpixel((0, y)) != gc)

    return tile_width, tile_height

def analyze_tileset(image_path):
    try:
        image = Image.open(image_path)
    except IOError:
        print(f"Error opening the image file: {image_path}")
        sys.exit(1)

    grid_color = find_grid_color(image)
    if grid_color is None:
        print("Unable to find grid lines.")
        sys.exit(1)

    tile_width, tile_height = detect_tile_dimensions(image, grid_color)
    img_width, img_height = image.size

    tiles_x = (img_width + 1) // (tile_width + 1)
    tiles_y = (img_height + 1) // (tile_height + 1)

    return {
        'tile_width': tile_width,
        'tile_height': tile_height,
        'spacing_x': 1,
        'spacing_y': 1,
        'tiles_x': tiles_x,
        'tiles_y': tiles_y,
    }

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python analyze_tileset.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    result = analyze_tileset(image_path)

    print(f"Tile width: {result['tile_width']}")
    print(f"Tile height: {result['tile_height']}")
    print(f"Spacing in X: {result['spacing_x']}")
    print(f"Spacing in Y: {result['spacing_y']}")
    print(f"Number of tiles in X: {result['tiles_x']}")
    print(f"Number of tiles in Y: {result['tiles_y']}")