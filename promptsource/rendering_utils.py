# Function that detects the type of each input (text, image, etc)
# Should rely on the dataset schema

# Dictionaries of how to render each modality
# {
#     "image": st.img,
#     "audio":
#     str: callable
# }
from typing import Dict
import streamlit as st
import re
import datasets

SPECIAL_VAR_REGEX = "(\<\<[\w_]+\>\>)"

SPECIAL_VAR_RENDERING_FUNCTIONS = {
    # https://docs.streamlit.io/library/api-reference/media/
    datasets.features.image.Image: st.image,
    datasets.features.audio.Audio: st.audio,
    # https://docs.streamlit.io/library/api-reference/media/st.video
}

def st_render(input_sequence: str, special_variables: Dict, dataset_schema: Dict):
    splited_input = re.split(SPECIAL_VAR_REGEX, input_sequence)
    splited_input = list(filter(lambda x: x != "", splited_input))
    for s in splited_input:
        if "<<" in s and ">>" in s:
            s_ = re.sub("[<>]", "", s) # Get the special variable name
            special_var_type = type(dataset_schema[s_]) # Determine what is the type of the special variable
            try:
                rendering_function = SPECIAL_VAR_RENDERING_FUNCTIONS[special_var_type]
            except KeyError:
                raise KeyError(f"No rendering function specified for this type of input {special_var_type}")
            rendering_function(special_variables[s_])
        else:
            st.text(s)