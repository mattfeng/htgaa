from opentrons import protocol_api
# from PIL import Image, ImageDraw
from collections import OrderedDict
# import pickle
import random

# metadata
metadata = {
    'protocolName': 'Pipette Printer',
    'author': 'Matthew Feng <mattfeng@mit.edu>',
    'description': 'A protocol that takes in an input image and does its best to replicate it using red, green, blue, and yellow dyes on a 96 well plate.',
    'apiLevel': '2.11'
}

# def cmyk2rgb(c, m, y, cmyk_scale, rgb_scale=255):
#     r = int(rgb_scale * (1.0 - c / float(cmyk_scale)))
#     g = int(rgb_scale * (1.0 - m / float(cmyk_scale)))
#     b = int(rgb_scale * (1.0 - y / float(cmyk_scale)))
#     return r, g, b

# def make_colors():
#     colors = {}
#     MAX = 101
#     for r in range(0, MAX):
#         for g in range(0, MAX - r):
#             for b in range(0, MAX - r - g):
#                 for y in range(0, MAX - r - g - b):
#                     if (r, g, b, y) == (0, 0, 0, 0):
#                         colors[(255, 255, 255)] = (0, 0, 0, 0)
#                         continue

#                     color_c = g + b
#                     color_m = r + b
#                     color_y = r + g + y
#                     # cmyk_scale = color_c + color_m + color_y
#                     cmyk_scale = r + b + g + y

#                     rgb = cmyk2rgb(color_c, color_m, color_y, cmyk_scale)

#                     colors[rgb] = (r, g, b, y)

#     return colors

# def get_closest_color(color, color_dict):
#     cr, cg, cb = color
#     min_dist = None
#     best_color = None
#     for r, g, b in color_dict:
#         dist = ((cr - r) * 0.30) ** 2 + ((cg - g) * 0.59) ** 2 + ((cb - b) * 0.11) ** 2

#         if min_dist is None or dist < min_dist:
#             min_dist = dist
#             best_color = (r, g, b)

#     return best_color


# def test_colors(colors):
#     # TEST_COLORS = [
#     #     ("red", (255, 0, 0)),
#     #     ("yellow", (255, 255, 0)),
#     #     ("white", (255, 255, 255)),
#     #     ("gray", (100, 100, 100)),
#     #     ("greenish", (83, 127, 18))
#     # ]

#     TEST_COLORS = [tuple(random.randint(0, 255) for _ in range(3)) for _ in range(25)]

#     for rgb_color in TEST_COLORS:
#         closest_rgb = get_closest_color(rgb_color, colors)
#         closest_rgby = colors[closest_rgb]
#         # print(f"{label}: {rgb_color} -> {closest_rgb} -> {closest_rgby}")
#         im = Image.new("RGB", (500, 250))
#         draw = ImageDraw.Draw(im)
#         draw.rectangle([0, 0, 250, 250], fill=rgb_color)
#         draw.rectangle([250, 0, 500, 250], fill=closest_rgb)
#         im.show()



# def load_and_process_image(filename):
#     img = Image.open(filename)
#     return img

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

    amounts = OrderedDict([('A1', {'r': 0, 'g': 0, 'b': 13, 'y': 72}), ('A2', {'r': 0, 'g': 0, 'b': 13, 'y': 72}), ('A3', {'r': 0, 'g': 0, 'b': 13, 'y': 72}), ('A4', {'r': 0, 'g': 0, 'b': 13, 'y': 72}), ('A5', {'r': 0, 'g': 0, 'b': 18, 'y': 67}), ('A6', {'r': 7, 'g': 0, 'b': 18, 'y': 60}), ('A7', {'r': 17, 'g': 0, 'b': 18, 'y': 50}), ('A8', {'r': 30, 'g': 0, 'b': 16, 'y': 39}), ('A9', {'r': 39, 'g': 0, 'b': 16, 'y': 30}), ('A10', {'r': 51, 'g': 0, 'b': 21, 'y': 26}), ('A11', {'r': 50, 'g': 0, 'b': 29, 'y': 21}), ('A12', {'r': 45, 'g': 8, 'b': 27, 'y': 7}), ('B1', {'r': 0, 'g': 0, 'b': 13, 'y': 72}), ('B2', {'r': 0, 'g': 0, 'b': 13, 'y': 72}), ('B3', {'r': 0, 'g': 0, 'b': 13, 'y': 72}), ('B4', {'r': 0, 'g': 0, 'b': 15, 'y': 70}), ('B5', {'r': 3, 'g': 0, 'b': 18, 'y': 64}), ('B6', {'r': 13, 'g': 0, 'b': 18, 'y': 54}), ('B7', {'r': 25, 'g': 0, 'b': 16, 'y': 44}), ('B8', {'r': 22, 'g': 0, 'b': 9, 'y': 20}), ('B9', {'r': 50, 'g': 0, 'b': 20, 'y': 30}), ('B10', {'r': 52, 'g': 0, 'b': 25, 'y': 23}), ('B11', {'r': 46, 'g': 0, 'b': 33, 'y': 18}), ('B12', {'r': 38, 'g': 11, 'b': 23, 'y': 0}), ('C1', {'r': 0, 'g': 0, 'b': 13, 'y': 72}), ('C2', {'r': 0, 'g': 0, 'b': 13, 'y': 72}), ('C3', {'r': 0, 'g': 0, 'b': 13, 'y': 72}), ('C4', {'r': 0, 'g': 0, 'b': 18, 'y': 67}), ('C5', {'r': 8, 'g': 0, 'b': 18, 'y': 59}), ('C6', {'r': 19, 'g': 0, 'b': 18, 'y': 48}), ('C7', {'r': 31, 'g': 0, 'b': 16, 'y': 38}), ('C8', {'r': 41, 'g': 0, 'b': 16, 'y': 28}), ('C9', {'r': 27, 'g': 0, 'b': 11, 'y': 13}), ('C10', {'r': 47, 'g': 0, 'b': 28, 'y': 19}), ('C11', {'r': 51, 'g': 10, 'b': 30, 'y': 6}), ('C12', {'r': 42, 'g': 13, 'b': 36, 'y': 0}), ('D1', {'r': 0, 'g': 0, 'b': 13, 'y': 72}), ('D2', {'r': 0, 'g': 0, 'b': 13, 'y': 72}), ('D3', {'r': 0, 'g': 0, 'b': 15, 'y': 70}), ('D4', {'r': 4, 'g': 0, 'b': 18, 'y': 63}), ('D5', {'r': 14, 'g': 0, 'b': 18, 'y': 53}), ('D6', {'r': 27, 'g': 0, 'b': 16, 'y': 42}), ('D7', {'r': 36, 'g': 0, 'b': 16, 'y': 33}), ('D8', {'r': 42, 'g': 0, 'b': 18, 'y': 25}), ('D9', {'r': 38, 'g': 0, 'b': 20, 'y': 17}), ('D10', {'r': 40, 'g': 2, 'b': 27, 'y': 13}), ('D11', {'r': 47, 'g': 14, 'b': 31, 'y': 0}), ('D12', {'r': 38, 'g': 13, 'b': 45, 'y': 0}), ('E1', {'r': 0, 'g': 0, 'b': 13, 'y': 72}), ('E2', {'r': 0, 'g': 0, 'b': 8, 'y': 43}), ('E3', {'r': 0, 'g': 0, 'b': 11, 'y': 40}), ('E4', {'r': 10, 'g': 0, 'b': 18, 'y': 57}), ('E5', {'r': 22, 'g': 0, 'b': 16, 'y': 47}), ('E6', {'r': 32, 'g': 0, 'b': 16, 'y': 37}), ('E7', {'r': 41, 'g': 0, 'b': 16, 'y': 28}), ('E8', {'r': 43, 'g': 0, 'b': 20, 'y': 22}), ('E9', {'r': 42, 'g': 0, 'b': 26, 'y': 17}), ('E10', {'r': 36, 'g': 9, 'b': 20, 'y': 2}), ('E11', {'r': 40, 'g': 13, 'b': 37, 'y': 0}), ('E12', {'r': 32, 'g': 12, 'b': 51, 'y': 0}), ('F1', {'r': 0, 'g': 0, 'b': 13, 'y': 72}), ('F2', {'r': 0, 'g': 0, 'b': 16, 'y': 69}), ('F3', {'r': 5, 'g': 0, 'b': 18, 'y': 62}), ('F4', {'r': 15, 'g': 0, 'b': 18, 'y': 52}), ('F5', {'r': 27, 'g': 0, 'b': 16, 'y': 42}), ('F6', {'r': 23, 'g': 0, 'b': 9, 'y': 19}), ('F7', {'r': 43, 'g': 0, 'b': 18, 'y': 24}), ('F8', {'r': 31, 'g': 0, 'b': 16, 'y': 13}), ('F9', {'r': 50, 'g': 5, 'b': 32, 'y': 13}), ('F10', {'r': 46, 'g': 14, 'b': 32, 'y': 0}), ('F11', {'r': 33, 'g': 11, 'b': 41, 'y': 0}), ('F12', {'r': 17, 'g': 8, 'b': 37, 'y': 0}), ('G1', {'r': 0, 'g': 0, 'b': 8, 'y': 43}), ('G2', {'r': 1, 'g': 0, 'b': 18, 'y': 66}), ('G3', {'r': 11, 'g': 0, 'b': 18, 'y': 56}), ('G4', {'r': 23, 'g': 0, 'b': 16, 'y': 46}), ('G5', {'r': 33, 'g': 0, 'b': 16, 'y': 36}), ('G6', {'r': 42, 'g': 0, 'b': 16, 'y': 27}), ('G7', {'r': 44, 'g': 0, 'b': 20, 'y': 21}), ('G8', {'r': 42, 'g': 0, 'b': 27, 'y': 16}), ('G9', {'r': 51, 'g': 14, 'b': 28, 'y': 1}), ('G10', {'r': 42, 'g': 14, 'b': 41, 'y': 0}), ('G11', {'r': 25, 'g': 10, 'b': 43, 'y': 0}), ('G12', {'r': 19, 'g': 11, 'b': 55, 'y': 0}), ('H1', {'r': 0, 'g': 0, 'b': 16, 'y': 69}), ('H2', {'r': 6, 'g': 0, 'b': 18, 'y': 61}), ('H3', {'r': 16, 'g': 0, 'b': 18, 'y': 51}), ('H4', {'r': 29, 'g': 0, 'b': 16, 'y': 40}), ('H5', {'r': 38, 'g': 0, 'b': 16, 'y': 31}), ('H6', {'r': 44, 'g': 0, 'b': 18, 'y': 23}), ('H7', {'r': 26, 'g': 0, 'b': 14, 'y': 11}), ('H8', {'r': 50, 'g': 7, 'b': 31, 'y': 10}), ('H9', {'r': 47, 'g': 14, 'b': 35, 'y': 0}), ('H10', {'r': 35, 'g': 13, 'b': 47, 'y': 0}), ('H11', {'r': 25, 'g': 12, 'b': 57, 'y': 0}), ('H12', {'r': 17, 'g': 10, 'b': 60, 'y': 0})])

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