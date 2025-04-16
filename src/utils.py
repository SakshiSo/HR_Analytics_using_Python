"""App agnostic reusable utility functionality"""

from typing import List
import streamlit as st
from streamlit_kpi import streamlit_kpi as card


def setup_app(config):
    

    st.sidebar.title("HR Analytics")
    st.sidebar.write("Welcome to the HR Dashboard.")
    

def create_tabs(tabs: List[str]):
    """Creates streamlit tabs"""
    return st.tabs(tabs)


def sep():
    """Renders a horizontal separator"""
    st.markdown("---")


def render_card(
    key,
    title,
    value,
    secondary_text="",
    progress_value=100,
    progress_color="#007a99",
    icon="fa-globe",
):
    """Renders a custom KPI card with optional icon and progress-bar"""
    try:
        the_card = card(
            key=key,
            title=title,
            value=int(value),
            unit=secondary_text,
            icon=icon,
            iconTop=5,
            iconLeft=98,
            height=150,
            progressValue=progress_value,
            progressColor=progress_color,
            backgroundColor="#003d4d",
            titleColor="#FFFF",
            valueColor="#FFFF",
        )
        return the_card
    except Exception as e:
        st.error(f"Error rendering KPI card: {e}")
        return None


def download_file(btn_label, data, file_name, mime_type):
    """Creates a download button for data download"""
    st.download_button(
        label=btn_label, data=data, file_name=file_name, mime=mime_type
    )


def show_questions(questions: List[str]):
    q = "QUESTIONS:\n" + "\n".join(questions)
    # st.info(q, icon=app_config.icon_question)


def show_insights(insights: List[str]):
    a = "INSIGHTS:\n" + "\n".join(insights)
    # st.warning(a, icon=app_config.icon_insight)




  
