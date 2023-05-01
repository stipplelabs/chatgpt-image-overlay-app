from PIL import Image, ImageDraw
from service import font_service
from util.config_util import get_value

# The code contains a set of functions related to image manipulation 
# and drawing text. The functions enable users to generate images with text and 
# various background colors and alpha values. Additionally, the code provides functions 
# for cascading and positioning multiple images horizontally and vertically, as well 
# as adding borders to the generated images. The code also includes a function for 
# calculating the width and height of a set of boxes.

def get_alpha_box(size, alpha=80):
    return Image.new('RGBA', size, (0, 0, 0, alpha))


def get_alpha_color_box(size, background_color='#000000', alpha=255):
    box = Image.new('RGBA', size, background_color)
    box.putalpha(alpha)
    return box


def get_text_dimensions(text_string, font):
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    ascent, descent = font.getmetrics()
    (width, height), (offset_x, offset_y) = font.font.getsize(text_string)
    red_height = offset_y
    green_height = ascent - offset_y
    blue_height = descent
    return (offset_x, text_width, red_height, green_height, blue_height)


def draw_text_with_color_background(text, font, text_color='#FFFFFF', background_color='#000000', background_alpha=100):
    offset_x, text_width, r, g, b = get_text_dimensions(text, font)
    text_width = text_width + 2*r
    y = 0
    if background_alpha == 0:
        y = -int(r/2)
    size = (text_width, r + g + b+y)
    box = get_alpha_color_box(size, background_color, background_alpha)
    draw = ImageDraw.Draw(box)
    draw.text((r, y), text, fill=text_color, font=font)
    return box, (r, g, b)


def draw_idtext_with_color_background(text, font, text_color='#FFFFFF', background_color='#000000', background_alpha=255):
    offset_x, text_width, r, g, b = get_text_dimensions(text, font)
    text_width = text_width + 2*r
    y = 0
    if background_alpha == 255:
        y = -int(r/2)-1
    size = (text_width, r + g + b+y)
    box = get_alpha_color_box(size, background_color, background_alpha)
    draw = ImageDraw.Draw(box)
    draw.text((r, y+2), text, fill=text_color, font=font)
    return box, (r, g, b)


def get_element_box_old(element_style):
    text = get_value(element_style, 'text')
    text = str(text)
    if text in [None, '']:
        text = 'Missing Text'

    text_color = get_value(element_style, 'font_style.text_color')
    if text_color in [None, '']:
        text_color = '#000000'
    background_color = get_value(element_style, 'background_color')
    if background_color in [None, '']:
        background_color = '#FFFFFF'
    background_alpha = get_value(element_style, 'background_alpha')

    if background_alpha not in [None, '']:
        background_alpha = int((background_alpha / 100) * 255)
    else:
        background_alpha = 255

    font = font_service.get_element_font(element_style)
    if text is not None and font is not None:
        return draw_text_with_color_background(text, font, text_color, background_color, background_alpha)
    else:
        return None


def get_element_box(element_style):
    text = get_value(element_style, 'text')
    text = str(text)
    if text in [None, '']:
        text = 'Missing Text'

    text_color = get_value(element_style, 'text_color')
    if text_color in [None, '']:
        text_color = '#000000'
    background_color = get_value(element_style, 'background_color')
    if background_color in [None, '']:
        background_color = '#FFFFFF'
    background_alpha = get_value(element_style, 'background_alpha')

    if background_alpha not in [None, '']:
        background_alpha = int((background_alpha / 100) * 255)
    else:
        background_alpha = 255

    # print('aplha: ', background_alpha)
    font = font_service.get_element_font(element_style)
    if text is not None and font is not None:
        return draw_text_with_color_background(text, font, text_color, background_color, background_alpha)
    else:
        return None


def get_total_box_width(boxes, xPadding=0):
    width = 0
    for idx, box in enumerate(boxes):
        if idx < len(boxes) - 1:
            width += box[0].size[0] + xPadding
        else:
            width += box[0].size[0]

    return width


def get_total_box_height(boxes, yPadding=0):
    height = 0
    for idx, box in enumerate(boxes):
        if idx < len(boxes) - 1:
            height += box[0].size[1] + yPadding
        else:
            height += box[0].size[1]
    return height

# horizantally cascade boxes


def get_id_box(element_style):
    text = str(element_style['element_id'])
    background_color = '#000000'
    background_alpha = 0
    text_color = '#DFFF00'

    style = {
        'font':  'roboto',
        'font_type': 'medium',
        'font_size': 24,
        'text_color': text_color
    }
    font = font_service.get_element_font(style)
    if text is not None and font is not None:
        return draw_idtext_with_color_background(text, font, text_color)
    else:
        return None


def add_bottom_border(box, border_color='#909090', border_width=5):
    image = ImageDraw.Draw(box[0])
    width, height = box[0].size
    image.rectangle([(0, height - border_width),
                    (width, height)], fill=border_color)
    return box


def add_top_border(box, border_color='#909090', border_width=1):
    image = ImageDraw.Draw(box[0])
    width, height = box[0].size
    image.rectangle([(0, 0), (width, border_width)], fill=border_color)
    return box


def add_top_border_with_padding(box, border_color='#909090', border_width=1, bottom_padding=3):
    width, height = box[0].size
    new_height = height + border_width + bottom_padding
    new_image = Image.new('RGB', (width, new_height), (0, 0, 0))
    new_image.paste(box[0], (0, border_width))

    draw = ImageDraw.Draw(box[0])
    draw.rectangle([(0, 0), (width, border_width)], fill=border_color)
    return (new_image, (0, 0, 0))
