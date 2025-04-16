"""Attrition tab rendering functionality"""

import pandas as pd
import streamlit
import utils
import data
import plots

###
### render the attrition analysis page
###
def render(df: pd.DataFrame):
    # Show KPI & plots
    __build_attrition_plots(df)

###
### module's internal functions
###
def __build_attrition_plots(df):
    with streamlit.expander("Analysis: Employee Attrition...", expanded=True):
        
        ### Gather attrition statistics
        attrition_stats = data.get_attrition_stats(df)
        
        ### Overall, male, and female attrition rates
        with streamlit.container():
            c1_col1, c1_col2, c1_col3 = streamlit.columns(3)
            with c1_col1:
                attr_tot = attrition_stats["CompanyWide"]["Total Attrition"]
                attr_pct = attrition_stats["CompanyWide"]["Attrition Rate"]
                utils.render_card(
                    key="attrition_card1",
                    title="Overall Attrition",
                    value=attr_tot,
                    secondary_text=f" ({attr_pct}%)",
                    icon="fa-sharp fa-solid fa-venus-mars fa-xs",
                    progress_value=min(int(attr_pct), 100),
                    progress_color="red",
                )
            with c1_col2:
                male_attr_tot = attrition_stats.get("Male", {}).get("Total Attrition", 0)
                male_attr_pct = attrition_stats.get("Male", {}).get("Attrition Rate", 0)
                utils.render_card(
                    key="attrition_card2",
                    title="Male Attrition",
                    value=male_attr_tot,
                    secondary_text=f" ({male_attr_pct}%)",
                    icon="fa-sharp fa-solid fa-mars fa-xs",
                    progress_value=min(int(male_attr_pct), 100),
                    progress_color="red",
                )
            with c1_col3:
                female_attr_tot = attrition_stats.get("Female", {}).get("Total Attrition", 0)
                female_attr_pct = attrition_stats.get("Female", {}).get("Attrition Rate", 0)
                utils.render_card(
                    key="attrition_card3",
                    title="Female Attrition",
                    value=female_attr_tot,
                    secondary_text=f" ({female_attr_pct}%)",
                    icon="fa-sharp fa-solid fa-venus fa-xs",
                    progress_value=min(int(female_attr_pct), 100),
                    progress_color="red",
                )
        utils.sep()

        ### Attrition by department & job role
        with streamlit.container():
            c2_col1, c2_col2 = streamlit.columns(2)
            with c2_col1:
                streamlit.plotly_chart(
                    plots.plot_dept_attrition(pd.DataFrame(
                        list(attrition_stats["Department"].items()), columns=["Department", "AttritionCount"])),
                    use_container_width=True, key = "attrition_department_chart"
                )
            with c2_col2:
                streamlit.plotly_chart(
                    plots.plot_jobrole_attrition(pd.DataFrame(
                        list(attrition_stats["JobRole"].items()), columns=["JobRole", "AttritionCount"])),
                    use_container_width=True, key = "attrition_jobrole_chart"
                )
        utils.sep()

        ### Attrition by workplace proximity & job satisfaction
        with streamlit.container():
            c3_col1, c3_col2 = streamlit.columns(2)
            with c3_col1:
                streamlit.plotly_chart(
                    plots.plot_dist_attrition(pd.DataFrame(
                        list(attrition_stats["WorkplaceProximity"].items()), columns=["WorkplaceProximity", "% Attrition"])),
                    use_container_width=True, key = "attrition_distance_chart"
                )
            with c3_col2:
                streamlit.plotly_chart(
                    plots.plot_satis_attrition(pd.DataFrame(
                        list(attrition_stats["JobSatisfaction"].items()), columns=["JobSatisfaction", "% Attrition"])),
                    use_container_width=True, key = "attrition_satisfaction_chart"
                )
        utils.sep()

        ### Attrition by age & work experience
        with streamlit.container():
            c4_col1, c4_col2 = streamlit.columns(2)
            with c4_col1:
                streamlit.plotly_chart(
                    plots.plot_ages_attrition(pd.DataFrame(
                        list(attrition_stats["Ages"].items()), columns=["Age", "% Attrition"])),
                    use_container_width=True, key = "attrition_age_chart"
                )
            with c4_col2:
                streamlit.plotly_chart(
                    plots.plot_exp_attrition(pd.DataFrame(
                        list(attrition_stats["WorkExperience"].items()), columns=["WorkExperience", "% Attrition"])),
                    use_container_width=True, key = "attrition_experience_chart"
                )
        utils.sep()

    