from util.config_util import get_value
from pathlib import Path
from PIL import ImageFont

# This code defines utility functions for working with fonts in image processing. 
# The checkFontExist function checks whether a font file exists in the specified 
# directory. The getFontFile function returns the font file path for a given font 
# name and font type. The get_font_with_size function returns an ImageFont object 
# with the specified font, font type, and font size. The get_element_font function 
# returns the font for a given element, using the get_font_with_size function and 
# the element's font attributes.

# These functions can be used in image processing tasks that involve adding text to 
# images, such as creating image overlays. They ensure that the correct font file is 
# used and that the font size is set correctly. By providing a consistent font across 
# multiple images or elements, these functions can also help to create a cohesive 
# visual style.

def checkFontExist(font):
    return Path('font/'+font).exists()


def getFontFile(font, font_type):
    try:
        font_file = 'font/'+font+'/'+font.capitalize() + \
            '-'+font_type.capitalize()+'.ttf'
        if checkFontExist(font):
            return font_file
        else:
            print('Error: Font '+font.capitalize()+'-' +
                  font_type.capitalize()+'.ttf not found')
            return None
    except Exception as e:
        print(e)
        return None


def get_font_with_size(font, font_type, size):
    fontfile = getFontFile(font, font_type)
    if fontfile is not None:
        return ImageFont.truetype(fontfile, size)
    else:
        return None


def get_element_font(element):
    font = get_value(element, 'font')
    font_type = get_value(element, 'font_type')
    font_size = get_value(element, 'font_size')
    if font is not None and font_type is not None and font_size is not None:
        return get_font_with_size(font, font_type, font_size)
    else:
        return None
