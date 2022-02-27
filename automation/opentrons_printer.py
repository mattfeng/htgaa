from ast import Or
from opentrons import protocol_api
from PIL import Image, ImageDraw
from collections import OrderedDict
import pickle
import random

# metadata
metadata = {
    'protocolName': 'Pipette Printer',
    'author': 'Matthew Feng <mattfeng@mit.edu>',
    'description': 'A protocol that takes in an input image and does its best to replicate it using red, green, blue, and yellow dyes on a 96 well plate.',
    'apiLevel': '2.11'
}

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
                    # cmyk_scale = color_c + color_m + color_y
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
    # TEST_COLORS = [
    #     ("red", (255, 0, 0)),
    #     ("yellow", (255, 255, 0)),
    #     ("white", (255, 255, 255)),
    #     ("gray", (100, 100, 100)),
    #     ("greenish", (83, 127, 18))
    # ]

    TEST_COLORS = [tuple(random.randint(0, 255) for _ in range(3)) for _ in range(25)]

    for rgb_color in TEST_COLORS:
        closest_rgb = get_closest_color(rgb_color, colors)
        closest_rgby = colors[closest_rgb]
        # print(f"{label}: {rgb_color} -> {closest_rgb} -> {closest_rgby}")
        im = Image.new("RGB", (500, 250))
        draw = ImageDraw.Draw(im)
        draw.rectangle([0, 0, 250, 250], fill=rgb_color)
        draw.rectangle([250, 0, 500, 250], fill=closest_rgb)
        im.show()



def load_and_process_image(filename):
    img = Image.open(filename)
    return img

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):
    # labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '1')
    palette = protocol.load_labware('usascientific_12_reservoir_22ml', '2')
    canvas = protocol.load_labware('nest_96_wellplate_200ul_flat', '5')

    colorwells = {
        'g': 'A1',
        'b': 'A2',
        'r': 'A3',
        'y': 'A4'
    }

    # pipettes
    left_pipette = protocol.load_instrument(
         'p300_single', 'left', tip_racks=[tiprack])

    amounts = pickle.load(open("gradient2.pkl", "rb"))

    for color in "rgby":
        left_pipette.pick_up_tip()

        for well, amt in amounts.items():
            if amt[color] == 0:
                continue
            left_pipette.aspirate(amt[color], palette[colorwells[color]])
            left_pipette.dispense(amt[color], canvas[well])

        left_pipette.drop_tip()

# im = load_and_process_image("gradient2.png")
# imdata = im.getdata()
# preview = Image.new("RGB", (12, 8))
# w, h = im.size

# colorspace = make_colors()

# amounts = OrderedDict()
# preview_data = []

# for ir, row in enumerate("ABCDEFGH"):
#     for col in range(0, 12):
#         imcolor = imdata[ir * 12 + col]
#         closest_rgb = get_closest_color(imcolor, colorspace)
#         preview_data.append(closest_rgb)
#         r, g, b, y = colorspace[closest_rgb]
#         amounts[f"{row}{col + 1}"] = {
#             "r": r,
#             "g": g,
#             "b": b,
#             "y": y
#         }

# print(amounts)
# pickle.dump(amounts, open("gradient2.pkl", "wb"))

# preview.putdata(preview_data)
# preview.show()

# colors = make_colors()
# test_colors(colors)