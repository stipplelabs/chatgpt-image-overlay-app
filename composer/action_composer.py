# %%
from PIL import Image
from service import overlay_service
from util import config_util, log

# This code defines a module called action_composer that contains several functions
# for processing user actions on an image overlay design. The module first defines a
# JSON object called overlay_json that represents the current state of the image
# overlay design. The module then defines several functions for manipulating the
# JSON object, including new_element(), edit_element(), delete_element(),
# show_hide_metadata(), new_group_element(), edit_group_element(), and ungroup_delete_group().
# These functions modify the JSON object based on the user's input action and are used
# by the process_action() function to update the overlay design.

# The process_action() function takes a JSON object representing the user's input action
# and uses the previously defined functions to update the overlay_json object accordingly.
# It then calls the apply_action() function to apply the updated JSON object to the
# background image and return the resulting image with the overlay design. The 
# apply_action() function loads the background image specified in the JSON object and
# overlays the individual and group elements based on their specified styles. Finally,
# it returns the resulting image with the overlay design. The module can be used as part
# of a larger image overlay design application to allow users to modify and preview their
# overlay design in real-time.

overlay_json = {
    'background_image': 'running.jpg',
    'display_metadata': 'false',
    'type': 'image',
    'elements': [],
    'groups': []
}


def new_element(user_element):
    element_count = len(overlay_json['elements']) + 1
    elements = overlay_json['elements']

    if 'element_id' not in user_element:
        user_element['element_id'] = 'E' + str(element_count)
        elements.append(user_element)
    overlay_json['elements'] = elements


def edit_element(user_element):
    if 'elements' in overlay_json and len(overlay_json['elements']) > 0:
        elements = overlay_json['elements']
        for idx, ele in enumerate(elements):
            if ele['element_id'] in user_element['element_ids']:
                # compare key values and update the element
                for key, value in user_element.items():
                    if key in ele:
                        ele[key] = value
        overlay_json['elements'] = elements


def delete_element(user_element):
    if 'elements' in overlay_json and len(overlay_json['elements']) > 0:
        elements = overlay_json['elements']
        for idx, ele in enumerate(elements):
            if ele['element_id'] in user_element['element_ids']:
                ele['display'] = 'false'
        overlay_json['elements'] = elements


def show_hide_metadata(show_metadata):

    if show_metadata:
        overlay_json['display_metadata'] = 'true'
    else:
        overlay_json['display_metadata'] = 'false'

################### Groups ############################


def new_group_element(user_group):
    group_count = len(overlay_json['groups']) + 1
    groups = overlay_json['groups']

    elelemts_already_in_group = False
    # iterate groups and check element_id array with user provided group element_id array
    for idx, group in enumerate(groups):
        if group['element_ids'] == user_group['element_ids']:
            # group already exists
            elelemts_already_in_group = True
            break

    if not elelemts_already_in_group:
        if 'group_id' not in user_group:
            user_group['group_id'] = 'G' + str(group_count)
            groups.append(user_group)
        overlay_json['groups'] = groups

# Edit group element


def edit_group_element(user_group):
    if 'groups' in overlay_json and len(overlay_json['groups']) > 0:
        groups = overlay_json['groups']
        for idx, group in enumerate(groups):
            if group['group_id'] in user_group['group_ids']:
                # compare key values and update the element
                for key, value in user_group.items():
                    # if key in group:
                    group[key] = value
        overlay_json['groups'] = groups

# Ungroup elements


def ungroup_delete_group(user_group):
    if 'groups' in overlay_json and len(overlay_json['groups']) > 0:
        groups = overlay_json['groups']
        new_groups = []
        elements = overlay_json['elements']

        for idx, group in enumerate(groups):
            if group['group_id'] not in user_group['group_ids']:
                new_groups.append(group)
                # compare key values and update the element
                # group['display'] = 'false'
        overlay_json['groups'] = new_groups
        # iterate elements and check if any element is part of group
        for idx, ele in enumerate(elements):
            if ele['element_id'] in user_group['group_ids']:
                # compare key values and update the element
                ele['display'] = 'true'
        overlay_json['elements'] = elements


def init():
    individual_elements = config_util.get_value(overlay_json, 'elements')
    for idx, ele in enumerate(individual_elements):
        if 'display' in ele:
            ele['display'] = 'true'

# process action json provided and verify element by element to seggregate the elements
# based on action key and invoke corresponding functions


def process_action(action_json):
    LOGS = []
    init()

    if action_json and len(action_json) > 0:
        # Seggregate the elements based on action key vale new_element

        for idx, element in enumerate(action_json):
            if element['action'] == 'new_element':
                new_element(element)
            if element['action'] == 'edit_element':
                edit_element(element)
            elif element['action'] == 'delete_element':
                delete_element(element)
            elif element['action'] == 'show_metadata':
                show_hide_metadata(True)
            elif element['action'] == 'hide_metadata':
                show_hide_metadata(False)
            elif element['action'] == 'group_elements':
                new_group_element(element)
            elif element['action'] == 'edit_group':
                edit_group_element(element)
            elif element['action'] == 'delete_group':
                ungroup_delete_group(element)

        return apply_action(overlay_json)

# [{"action": "new_element", "text": "Pace", "position": "center", "font": "roboto", "font_type": "mediumitalic", "font_size": 58, "text_color": "#FFFFFF", "background_color": "#ff0000", "padding": [0, 2, 5, 10], "background_alpha": 50}, {"action": "new_element", "text": "6.09/km", "position": "center", "font": "roboto", "font_type": "mediumitalic", "font_size": 58, "text_color": "#FFFFFF", "background_color": "#ff0000", "padding": [0, 2, 5, 10], "background_alpha": 50}]
# This is the main function that processes the action json
# It needs to process the individual elements and display them on the given background image
# and return it.


def apply_action(overlay_json):
    LOGS = []
    # Load the background image
    background_image_name = config_util.get_value(overlay_json,
                                                  'background_image')
    if background_image_name is None:
        # if no background image is specified, use a black background
        background_image = Image.new('RGB', (1080, 1080), (0, 0, 0))
        log.log(
            LOGS, 'json_composer: No background image specified, using black background', 2)
    else:
        # background image is specified, load it
        backgroundPath = 'media/'+background_image_name
        background_image = Image.open(backgroundPath).copy()
        log.log(LOGS, 'json_composer: Background image : '+background_image_name)

    #  get all the element styles
    individual_elements = config_util.get_value(overlay_json, 'elements')
    group_elements = config_util.get_value(overlay_json, 'groups')
    if group_elements and len(group_elements) > 0:
        log.log(LOGS, 'json_composer: Group elements : ' +
                str(len(group_elements)))
        background_image = overlay_service.group_elements(
            group_elements, individual_elements, background_image, overlay_json)

    if individual_elements and len(individual_elements) > 0:
        log.log(LOGS, 'json_composer: Individual elements : ' +
                str(len(individual_elements)))
        background_image = overlay_service.position_individual_elements(
            individual_elements, background_image, overlay_json)

    return background_image
