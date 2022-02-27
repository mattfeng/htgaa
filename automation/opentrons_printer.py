from opentrons import protocol_api

def cmyk2rgb(c, m, y, cmyk_scale, rgb_scale=255):
    r = int(rgb_scale * (1.0 - c / float(cmyk_scale)))
    g = int(rgb_scale * (1.0 - m / float(cmyk_scale)))
    b = int(rgb_scale * (1.0 - y / float(cmyk_scale)))
    return r, g, b

def make_colors():
    colors = {}
    MAX = 101
    for r in range(0, MAX):
        for g in range(0, MAX - r):
            for b in range(0, MAX - r - g):
                for y in range(0, MAX - r - g - b):
                    if (r, g, b, y) == (0, 0, 0, 0):
                        colors[(255, 255, 255)] = (0, 0, 0, 0)
                        continue

                    color_c = g + b
                    color_m = r + b
                    color_y = r + g + y
                    cmyk_scale = r + b + g + y

                    rgb = cmyk2rgb(color_c, color_m, color_y, cmyk_scale)

                    colors[rgb] = (r, g, b, y)

    return colors

def get_closest_color(color, color_dict):
    cr, cg, cb = color
    min_dist = None
    best_color = None
    for r, g, b in color_dict:
        dist = ((cr - r) * 0.30) ** 2 + ((cg - g) * 0.59) ** 2 + ((cb - b) * 0.11) ** 2

        if min_dist is None or dist < min_dist:
            min_dist = dist
            best_color = (r, g, b)

    return best_color


def test_colors(colors):
    TEST_COLORS = [
        ("red", (255, 0, 0)),
        ("yellow", (255, 255, 0)),
        ("white", (255, 255, 255)),
        ("gray", (100, 100, 100)),
        ("greenish", (83, 127, 18))
    ]

    for label, rgb_color in TEST_COLORS:
        closest_rgb = get_closest_color(rgb_color, colors)
        closest_rgby = colors[closest_rgb]
        print(f"{label}: {rgb_color} -> {closest_rgb} -> {closest_rgby}")

# metadata
metadata = {
    'protocolName': 'Pipette Printer',
    'author': 'Matthew Feng <mattfeng@mit.edu>',
    'description': 'A protocol that takes in an input image and does its best to replicate it using red, green, blue, and yellow dyes on a 96 well plate.',
    'apiLevel': '2.11'
}

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):
    # labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '1')
    palette = protocol.load_labware('usascientific_12_reservoir_22ml', '2')
    canvas = protocol.load_labware('nest_96_wellplate_200ul_flat', '5')

    color = {
        'green': 'A1',
        'blue': 'A2',
        'red': 'A3',
        'yellow': 'A4'
    }

    # pipettes
    left_pipette = protocol.load_instrument(
         'p300_single', 'left', tip_racks=[tiprack])
