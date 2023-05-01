import streamlit as st
from PIL import Image
import numpy as np
from service.openai_api_service import OpenAICore
from util import string_util as su
from composer import action_composer

# This code defines a Streamlit web application that allows users to overlay an image with
# text generated by OpenAI's GPT-3 language model. The application consists of a header with
# the Stipple Labs logo, the app name, and a tagline, followed by an image upload widget and
# a text input prompt for the user. Upon submission, the user's text input is sent to the OpenAI API,
# and the resulting text is used to overlay the original image. The resulting image is displayed
# to the user with a caption indicating the source of the original image.

# The code uses the PIL library to manipulate and display images, the numpy library
# to handle image data as arrays, and the Streamlit framework to create the web application.
# It also relies on several utility functions for text and configuration management.
# The main() function initializes the application and defines its behavior. It first
# sets the layout and styling using Streamlit's set_page_config() and markdown() functions.
# It then displays the Stipple Labs logo, the app name, and the original image using
# Streamlit's image() and markdown() functions. Finally, it creates a form with a text
# input widget and a submit button using Streamlit's form() and form_submit_button() functions.
# When the user submits text input, the function sends a request to the OpenAI API using a custom
# service class and displays the resulting image using Streamlit's image() function.

st.set_page_config(
    layout="centered", page_title="Stipple Labs |  ChatGPT Image Overlay Design App",
    initial_sidebar_state="expanded",
    page_icon="https://www.stipplelabs.com/img/favicons/favicon-32x32.png")
padding = 0

st.markdown(f""" <style>
    .big-font {{
        font-size:20px !important;
        padding: 0px !important;
    }}
    .p-font {{
        font-size:18px !important;
        color: #808080  !important;
        padding: 0px !important;
    }}
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

# This is the main function
#


def main():

    open_api_request_sent = False

    stipplelabs_file = 'media/stipplelabs.png'
    stipplelabs = Image.open(stipplelabs_file)
    icol1, icol2, icol3 = st.columns([2, 2.4, 2])
    icol2.image(stipplelabs, width=256)
    pcol1, pcol2, pcol3 = st.columns([1.5, 1.1, 1])
    pcol2.markdown('<div class="p-font">www.stipplelabs.com</div>',
                   unsafe_allow_html=True)

    st.markdown("***")

    tcol1, tcol2, tcol3 = st.columns([3.1, 4.85, 3])
    tcol2.markdown(
        '<p class="big-font">ChatGPT Image Overlay Design App</p>', unsafe_allow_html=True)

    uploaded_file = 'media/running.jpg'
    input_image = Image.open(uploaded_file)
    input_image = np.array(input_image)
    if 'input_image' not in st.session_state:
        st.session_state.input_image = input_image

    img_loc = st.image(st.session_state.input_image, use_column_width='always',
                       caption='Image courtesy: Youcef Chenzer on unsplash.com', width=640)

    with st.form(key='overlay_form', clear_on_submit=True):
        openai_prompt = st.text_input("User Prompt", key="input_prompt")
        col1, col2 = st.columns([1, 7])

        submit_button = col1.form_submit_button(label='Submit')

    if openai_prompt and submit_button and not open_api_request_sent:
        open_api_request_sent = True
        with col2:
            with st.spinner(text='In progress'):
                api_response = OpenAICore.send_chat_request(openai_prompt)
                json_response = su.extract_json_from_string(
                    api_response['response'])
                st.session_state.input_image = action_composer.process_action(
                    json_response)
                img_loc.image(st.session_state.input_image, use_column_width='always',
                              caption='Image courtesy: Youcef Chenzer on unsplash.com', width=640)
        openai_prompt = None
        open_api_request_sent = False


if __name__ == "__main__":
    main()