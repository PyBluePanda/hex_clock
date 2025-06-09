import streamlit as st
from datetime import datetime
import time
import pytz
from pytz import all_timezones
from streamlit_javascript import st_javascript

st.set_page_config(
    page_title="Time Color Clock",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def get_tint_shade_text_colour(hex_colour, mix_ratio=0.4):
    hex_colour = hex_colour.lstrip('#')
    r, g, b = [int(hex_colour[i:i+2], 16) for i in (0, 2, 4)]

    luminance = 0.299 * r + 0.587 * g + 0.114 * b

    if luminance < 128:
        ## dark background - text tint (mix with white)
        mix_r, mix_g, mix_b = 255, 255, 255
    else:
        ## light background - text shade (mix with black)
        mix_r, mix_g, mix_b = 0, 0, 0

    new_r = int(r * (1 - mix_ratio) + mix_r * mix_ratio)
    new_g = int(g * (1 - mix_ratio) + mix_g * mix_ratio)
    new_b = int(b * (1 - mix_ratio) + mix_b * mix_ratio)

    return f'rgb({new_r}, {new_g}, {new_b})'

## automatically detect timezone from browser
browser_timezone = st_javascript("Intl.DateTimeFormat().resolvedOptions().timeZone") or "Europe/London"

with st.sidebar:
    st.header("Hex Clock")
    show_hex_text = st.toggle("Show Hex Code", value=True)
    show_24hours = st.toggle("24 Hour Clock", value=False)
    timezone = st.selectbox(
        "Select Timezone",
        options=all_timezones,
        index=all_timezones.index(browser_timezone) if browser_timezone in all_timezones else all_timezones.index("Europe/London")
    )
    
st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        .stApp {
            transition: background-color 1s ease;
        }
        /* Style sidebar background */
        [data-testid="stSidebar"] > div:first-child {
            transition: background-color 1s ease;
        }
        .big-time {
            font-size: 72px;
            font-weight: bold;
            text-align: center;
        }
        .hex-code {
            font-size: 58px;
            text-align: center;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)


placeholder = st.empty()

while True:
    now = datetime.now(pytz.timezone(timezone))
    time_display = now.strftime("%I:%M:%S %p")
    time_display_24 = now.strftime("%H:%M:%S")
    hex_colour = f"#{now.strftime('%H%M%S')}"
    text_colour = get_tint_shade_text_colour(hex_colour)

    ## CSS for background colours
    st.markdown(f"""
        <style>
            .stApp {{
                background-color: {hex_colour};
            }}
            [data-testid="stSidebar"] > div:first-child {{
                background-color: {text_colour};
                color: {hex_colour};
            }}
            /* Sidebar text elements */
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] h4,
            [data-testid="stSidebar"] h5,
            [data-testid="stSidebar"] h6,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] span {{
                color: {hex_colour} !important;
            }}
            /* Toggle switch styling */
            [data-testid="stSidebar"] .stSwitch > div {{
                background-color: {hex_colour} !important;
                border-color: {hex_colour} !important;
            }}
            [data-testid="stSidebar"] .stSwitch input:checked + div {{
                background-color: {hex_colour} !important;
                border-color: {hex_colour} !important;
            }}
            [data-testid="stSidebar"] .stSwitch input:checked + div:after {{
                background-color: {text_colour} !important;
            }}
            [data-testid="stSidebar"] .stSwitch div:after {{
                background-color: {hex_colour} !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    with placeholder.container():
        st.markdown(
            f"<div class='big-time' style='color:{text_colour};'>{time_display_24 if show_24hours else time_display}</div>",
            unsafe_allow_html=True
        )

        if show_hex_text:
            st.markdown(f"<div class='hex-code' style='color:{text_colour};'>{hex_colour}</div>", unsafe_allow_html=True)
        else:
            st.markdown("")

    time.sleep(1)
