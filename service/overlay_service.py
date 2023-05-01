from util import config_util, log
import requests
import json
from service import text_service as text
from PIL import Image

# Set of functions related to positioning and grouping 
# individual elements and containers on a background image. These functions allow for 
# manipulation of the display properties of individual elements, assignment of unique IDs 
# to elements, and cascading multiple elements into a single container.

# The code utilize the Python Imaging Library(PIL) for image processing and manipulation, 
# as well as the requests library for retrieving image data from URLs. 

grouped_boxes = {}
project_json = {}


def find_max_height(boxes):
    max_height = 0
    ht_idx = 0
    for idx, box in enumerate(boxes):
        if box[0].size[1] > max_height:
            max_height = box[0].size[1]
            ht_idx = idx
    return max_height, ht_idx


def align_box_to_center_horizontally(container, box, x_offset=0, y_offset=0):
    offset = (x_offset, y_offset)
    container.paste(box, offset)
    return container


def align_box_to_center_vertically(container, box, size, y_offset=0):
    # get center of box
    boxCenter = (int(box.size[0]/2), int(box.size[1]/2))
    # get center of container
    containerCenter = (int(size[0]/2), int(size[1]/2))
    # get offset
    offset = (containerCenter[0]-boxCenter[0],
              containerCenter[1]-boxCenter[1]+y_offset)
    # paste box to container
    container.paste(box, offset)
    return container


def align_box_to_center_vertically(container, box, y_offset=0):
    # get center of box
    boxCenter = (int(box.size[0]/2), int(box.size[1]/2))
    # get center of container
    size = container.size
    containerCenter = (int(size[0]/2), int(size[1]/2))
    # get offset
    offset = (containerCenter[0]-boxCenter[0],
              y_offset)
    # paste box to container
    container.paste(box, offset)
    return container


def align_box_to_left_vertically(container, box, y_offset=0):
    # get center of box
    boxCenter = (int(box.size[0]/2), int(box.size[1]/2))
    # get center of container
    size = container.size
    containerCenter = (int(size[0]/2), int(size[1]/2))
    # get offset
    offset = (0,
              y_offset)
    # paste box to container
    container.paste(box, offset)
    return container


def align_box_to_right_vertically(container, box, y_offset=0):
    # get center of box
    boxCenter = (int(box.size[0]/2), int(box.size[1]/2))
    # get center of container
    size = container.size
    x_offset = size[0] - box.size[0]
    # get offset
    offset = (x_offset,
              y_offset)
    # paste box to container
    container.paste(box, offset)
    return container


def find_max_box_width_height(boxes):
    max_width = 0
    max_height = 0
    for box in boxes:
        if box[0].size[0] > max_width:
            max_width = box[0].size[0]
        if box[0].size[1] > max_height:
            max_height = box[0].size[1]
    return max_width, max_height

# Vertical Cascade Boxes


def cascade_vertically(boxes, y_padding=5, align='right'):
    boxCount = len(boxes)
    max_width, max_height = find_max_box_width_height(boxes)
    size = (max_width, max_height)

    totalHeight = text.get_total_box_height(boxes, y_padding)
    container = Image.new(
        'RGBA', (max_width, totalHeight), (0, 0, 0, 0))
    y_offset = 0
    prev_y_offset = 0
    for i in range(boxCount):
        if i != 0:
            y_offset = y_offset + (boxes[i-1][0].size[1]+y_padding)
        if align == 'center':
            container = align_box_to_center_vertically(
                container, boxes[i][0], y_offset)
        elif align == 'right':
            container = align_box_to_right_vertically(
                container, boxes[i][0], y_offset)
            align_box_to_right_vertically
        else:
            container = align_box_to_left_vertically(
                container, boxes[i][0], y_offset)
    return container, (0, 0, 0)


def cascade_horizantally(boxes, x_padding=5):
    y_offset = 0
    boxCount = len(boxes)
    max_height, ht_idx = find_max_height(boxes)
    totalWidth = text.get_total_box_width(boxes, x_padding)

    container = Image.new(
        'RGBA', (totalWidth, max_height), (0, 0, 0, 0))

    x_offset = 0
    base_box = boxes[ht_idx]
    for i in range(boxCount):
        curr_box = boxes[i]
        if i != 0:
            x_offset = x_offset + (boxes[i-1][0].size[0]+x_padding)

        if i == ht_idx:
            y_offset = container.size[1] - boxes[i][0].size[1]
        else:
            y_offset = (base_box[1][0] + base_box[1][1]) - \
                (curr_box[1][0] + curr_box[1][1])
        container = align_box_to_center_horizontally(
            container, boxes[i][0], x_offset, y_offset)

    return container, boxes[ht_idx][1]


def position_container_on_background(container, align_mode=None, background_image=None):

    xy = align_mode.get('xy', None)
    position = align_mode.get('position', 'center')
    padding = align_mode.get('padding', [0, 0, 0, 0])
    if xy is not None:
        offset = (xy[0] - container[0].size[0] // 2,
                  (xy[1] - container[0].size[1]) // 2)
    else:
        offset = get_element_offset_with_padding(
            container, position, padding, background_image)

    background_image.paste(container[0], offset, container[0])
    return background_image


def get_element_style(element_styles, element_id_ref):
    for idx, element_style in enumerate(element_styles):
        element_id = config_util.get_value(element_style, 'element_id')
        if element_id == element_id_ref:
            return element_style
    return None


def get_element_offset(element_box, align, background_image):
    bg_w, bg_h = background_image.size
    offset = ((bg_w - element_box[0].size[0]) //
              2, (bg_h - element_box[0].size[1]) // 2)
    if align == 'top_left' or align == 'left_top':
        offset = (10, 10)
    elif align == 'top_right' or align == 'right_top':
        offset = (bg_w - element_box[0].size[0] - 10, 10)
    elif align == 'top_center' or align == 'top' or align == 'center_top':
        offset = ((bg_w - element_box[0].size[0]) //
                  2, 10)
    elif align == 'bottom_left' or align == 'left_bottom':
        offset = (10, bg_h - element_box[0].size[1] - 10)
    elif align == 'bottom_center' or align == 'bottom' or align == 'center_bottom':
        offset = ((bg_w - element_box[0].size[0]) //
                  2, bg_h - element_box[0].size[1] - 10)
    elif align == 'bottom_right' or align == 'right_bottom':
        offset = (bg_w - element_box[0].size[0] -
                  10, bg_h - element_box[0].size[1] - 10)

    elif align == 'center':
        offset = ((bg_w - element_box[0].size[0]) //
                  2, (bg_h - element_box[0].size[1]) // 2)
    elif align == 'center_left' or align == 'left' or align == 'left_center':
        offset = (10, (bg_h - element_box[0].size[1]) // 2)
    elif align == 'center_right' or align == 'right' or align == 'right_center':
        offset = (bg_w - element_box[0].size[0] -
                  10, (bg_h - element_box[0].size[1]) // 2)

    return offset


def get_element_offset_with_padding(element_box, align, padding=[0, 0, 0, 0], background_image=None):
    bg_w, bg_h = background_image.size
    offset = ((bg_w - element_box[0].size[0]) //
              2, (bg_h - element_box[0].size[1]) // 2)
    if align == 'top_left' or align == 'left_top':
        offset = (10, 10)
    elif align == 'top_right' or align == 'right_top':
        offset = (bg_w - element_box[0].size[0] - 10, 10)
    elif align == 'top_center' or align == 'top' or align == 'center_top':
        offset = ((bg_w - element_box[0].size[0]) //
                  2, 10)
    elif align == 'bottom_left' or align == 'left_bottom':
        offset = (10, bg_h - element_box[0].size[1] - 10)
    elif align == 'bottom_center' or align == 'bottom' or align == 'center_bottom':
        offset = ((bg_w - element_box[0].size[0]) //
                  2, bg_h - element_box[0].size[1] - 10)
    elif align == 'bottom_right' or align == 'right_bottom':
        offset = (bg_w - element_box[0].size[0] -
                  10, bg_h - element_box[0].size[1] - 10)

    elif align == 'center':
        offset = ((bg_w - element_box[0].size[0]) //
                  2, (bg_h - element_box[0].size[1]) // 2)
    elif align == 'center_left' or align == 'left' or align == 'left_center':
        offset = (10, (bg_h - element_box[0].size[1]) // 2)
    elif align == 'center_right' or align == 'right' or align == 'right_center':
        offset = (bg_w - element_box[0].size[0] -
                  10, (bg_h - element_box[0].size[1]) // 2)

    # given the padding values top,right, botton,left, we need to adjust the offset
    offset = (offset[0] + padding[3], offset[1] + padding[0])
    offset = (offset[0] - padding[1], offset[1] - padding[2])
    return offset


def position_a_element(element_style, background_image, position, xy=None):
    LOGS = []
    if 'image_url' in element_style:
        try:
            logo = Image.open(requests.get(
                element_style['image_url'], stream=True).raw)
            logo = logo.resize((512, 66))
            element_box = [logo, (0, 0, 0)]
        except Exception as e:
            element_box = None
    else:
        element_box = text.get_element_box(element_style)
        if project_json['display_metadata'] == 'true':
            id_box = text.get_id_box(element_style)
            element_box = cascade_horizantally([element_box, id_box])

    if element_box is not None:
        if xy is not None:
            offset = (xy[0] - element_box[0].size[0] // 2,
                      (xy[1] - element_box[0].size[1]) // 2)
        else:
            offset = get_element_offset(
                element_box, position, background_image)
        background_image.paste(element_box[0], offset, element_box[0])
    return background_image, element_box[0].size


def disable_individual_element(individual_elements, e_id):
    for idx, ele in enumerate(individual_elements):
        if 'element_id' in ele and ele['element_id'] == e_id:
            ele['display'] = 'false'
            break
    return individual_elements


def disable_group_elements(group_elements, e_id):
    for idx, ele in enumerate(group_elements):
        if 'element_id' in ele and ele['element_id'] == e_id:
            ele['display'] = 'false'
            break
    return group_elements


def enable_individual_elements(individual_elements, e_id):
    for idx, ele in enumerate(individual_elements):
        if 'element_id' in ele and ele['element_id'] == e_id:
            ele['display'] = 'true'
            break
    return individual_elements

# assign element_id to individual elements if not present


def assign_element_id(individual_elements):
    for idx, ele in enumerate(individual_elements):
        if 'element_id' not in ele:
            ele['element_id'] = 'E' + str(idx+1)
    return individual_elements


def assign_element_id(individual_elements, curr_count):
    for idx, ele in enumerate(individual_elements):
        if 'element_id' not in ele:
            ele['element_id'] = 'E' + str(curr_count+1)
    return individual_elements


def process_group_elements(group_elements, elements):
    global project_json
    cascaded_elements_list = []
    grouped_boxes = {}
    LOGS = []
    for idx, ele in enumerate(group_elements):
        group_id = ele.get("group_id")
        cascade_type = ele.get("cascade_type", "vertical")
        align = ele.get("align", "left")
        position = ele.get("position", "left")
        padding = ele.get("padding", [0, 0, 0, 0])
        element_ids = ele.get("element_ids")
        cascaded_box = None

        element_box_list = []
        if len(element_ids) > 1:
            for element_id in element_ids:
                if element_id.startswith('E'):
                    disable_individual_element(elements, element_id)
                    element_style = get_element_by_id(elements, element_id)
                    element_box = text.get_element_box(element_style)
                    if project_json['display_metadata'] == 'true':
                        id_box = text.get_id_box(element_style)
                        element_box = cascade_horizantally(
                            [element_box, id_box])
                elif element_id.startswith('G'):
                    disable_group_elements(elements, element_id)

                    # Get stored group element
                    if element_id in grouped_boxes:
                        element_box = grouped_boxes[element_id]['box']
                        del grouped_boxes[element_id]

                element_box_list.append(element_box)
        elif len(element_ids) == 1:
            element_style = get_element_style(
                elements, element_ids[0])
            cascaded_box = text.get_element_box(element_style)
            log.log(LOGS, 'cascade: Creating element box element_ref_id: ' +
                    element_ids[0] + 'text: '+element_style.get('text', '') + ' done')

        if len(element_box_list) > 0:
            if cascade_type == 'horizontal':
                cascaded_box = cascade_horizantally(element_box_list, 50)
            elif cascade_type == 'vertical':
                cascaded_box = cascade_vertically(element_box_list, 0, align)
                log.log(LOGS, 'cascade: Cascaded elements vertically aligned : ' +
                        str(len(element_box_list))+' done')

        if project_json['display_metadata'] == 'true' and group_id != 'G500':
            cascaded_box = text.add_top_border(cascaded_box)
            element_style = {
                'element_id': group_id,
            }
            id_box = text.get_id_box(element_style)
            cascaded_box = cascade_vertically(
                [id_box, cascaded_box], 1, 'left')

        grouped_boxes[group_id] = {}
        grouped_boxes[group_id]['box'] = cascaded_box
        grouped_boxes[group_id]['cascade_type'] = cascade_type
        grouped_boxes[group_id]['position'] = position
        grouped_boxes[group_id]['padding'] = padding

    return grouped_boxes


def group_elements(group_elements, elements, background_image, config_json):
    global project_json
    project_json = config_json
    grouped_container_list = {}
    LOGS = []
    grouped_container_list = process_group_elements(
        group_elements, elements)
    if len(grouped_container_list.items()) > 0:
        for key, group in grouped_container_list.items():
            position_on_background = {
                'position': 'center' if group['position'] == None else group['position'],
                'padding': group['padding']
            }
            background_image = position_container_on_background(
                group['box'], position_on_background, background_image)
            # background_image = group['box']
            log.log(LOGS, 'cascade: Positioning grouped container: ' +
                    str(key)+': @ : '+json.dumps(position_on_background)+' done')
    return background_image


def position_individual_elements(individual_elements, background_image, config_json):
    global project_json
    project_json = config_json

    elements_at_position = {}

    for idx, ele in enumerate(individual_elements):
        if 'display' not in ele or ele['display'] == 'true':
            position = ele.get("position", "center")
            if position not in elements_at_position:
                elements_at_position[position] = []
            elements_at_position[position].append(ele)

    for key, values in elements_at_position.items():
        if len(values) == 1:
            ele = values[0]
            position = ele.get("position", "center")
            xy = ele.get("xy", None)
            background_image, _ = position_a_element(
                ele, background_image, position, xy)
        else:
            elementIds = []
            ele = values[0]
            position = ele.get("position", "center")
            agroup = {
                'group_id': 'G500',
                'element_ids': [],
                'cascade_type': 'vertical',
                'align': 'left',
                'position': position,
                'padding': [0, 0, 0, 0]
            }

            for idx, ele in enumerate(values):
                elementIds.append(ele['element_id'])
            agroup['element_ids'] = elementIds

            background_image = group_elements(
                [agroup], individual_elements, background_image, config_json)
    return background_image


def get_element_by_id(elements, element_id):
    for idx, element in enumerate(elements):
        if 'element_id' in element and element['element_id'] == element_id:
            return element
    return None
