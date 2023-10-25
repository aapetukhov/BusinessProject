import pandas as pd
import numpy as np
from typing import Literal
import streamlit as st
from PIL import Image
import sys

LayoutType = Literal['centered', 'wide']

def init_page(title: str, desc: str, layout: LayoutType = 'wide'): 

    env = 'LOCAL'

    st.set_page_config(layout=layout,
                       page_title=f'{env.capitalize()} Business project - {title}',
                       page_icon = '🤯',)
    
    st.sidebar.markdown(f'# Environment: `{env}`')
    st.sidebar.markdown(f'# {title}')


    st.markdown(f'# {title}')
    st.write(desc)
    st.divider
