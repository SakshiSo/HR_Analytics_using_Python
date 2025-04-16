"""Summary tab rendering functionality"""

import pandas as pd
import streamlit
import data
import plots
import utils

###
### render the summary page
###
def render(df: pd.DataFrame):
    # Show sample data in a dataframe
    __show_sample_data(df)
    # Show KPI cards section
    __build_kpi_cards(df)
    # Show plots
    __build_age_plots(df)
    __build_dept_plots(df)
    __build_exp_plots(df)

###
### module's internal functions
###
def __show_sample_data(df: pd.DataFrame):
    """Display sample data as pandas DataFrame"""
    with streamlit.expander("View sample data | Download dataset..."):
        streamlit.markdown("#### Top 5 rows")
        streamlit.dataframe(df.head(5))
        streamlit.markdown("#### Bottom 5 rows")
        streamlit.dataframe(df.tail(5))
        # read the file again and then download
        csv = data.df_to_csv(df)
        utils.download_file(
            btn_label="Download As CSV",
            data=csv,
            file_name="hr_data_downloaded.csv",
            mime_type="text/csv",
        )

def __build_kpi_cards(df: pd.DataFrame):
    """display total, male, female employees cards"""
    with streamlit.expander("View Gender Stats...", expanded=True):
        ## List questions/objectives
        utils.show_questions([
            "* Do we have a balanced workforce in terms of gender?",
        ])

        # total and gender wise emp count
        __show_emp_count_card(df)
          

def __show_emp_count_card(df):
    (
        tot_emp_cnt,
        male_emp_cnt,
        female_emp_cnt,
        male_pct,
        female_pct,
    ) = data.get_gender_count(df)

    with streamlit.container():
        g_col1, g_col2, g_col3 = streamlit.columns(3)
        with g_col1:
            utils.render_card(
                key="tot_card",
                title="Total<br>Employees",
                value=tot_emp_cnt,
                icon="fa-sharp fa-solid fa-venus-mars fa-xs",
            )
        with g_col2:
            utils.render_card(
                key="male_card",
                title="Males",
                value=male_emp_cnt,
                secondary_text=f" ({male_pct})%",
                icon="fa-sharp fa-solid fa-mars fa-xs",
                progress_value=int(male_pct),
                progress_color="#186ee8",
            )
        with g_col3:
            utils.render_card(
                key="female_card",
                title="Females",
                value=female_emp_cnt,
                secondary_text=f" ({female_pct})%",
                icon="fa-sharp fa-light fa-venus fa-xs",
                progress_value=int(female_pct),
                progress_color="#ff6d6d",
            )

def __build_age_plots(df: pd.DataFrame):
    ### age distribution
    with streamlit.expander("Analysis: Age & Marital Status...", expanded=True):
        utils.show_questions([
            "* Are we an ageing or young organization?",
            "* Do we need to recruit more young or more experienced people?",
            "* Should we target recruiting employees for a particular age group and gender?",
            "* Do we have a balanced distribution of employees by their marital status?",
        ])

        (age_dist_col1, age_dist_col2) = streamlit.columns(2)
        with age_dist_col1:
            fig_age_hist = plots.plot_age_hist(df)
            streamlit.plotly_chart(fig_age_hist, use_container_width=True, key="age_hist")
        with age_dist_col2:
            fig_age_box = plots.plot_age_gender_box(df)
            streamlit.plotly_chart(fig_age_box, use_container_width=True, key="age_gender_box")
        with age_dist_col1:
            fig_age_box = plots.plot_age_marital_status_pie(df)
            streamlit.plotly_chart(fig_age_box, use_container_width=True, key="age_marital_pie")
        with age_dist_col2:
            fig_age_box = plots.plot_age_marital_status_box(df)
            streamlit.plotly_chart(fig_age_box, use_container_width=True, key="age_marital_box")

def __build_dept_plots(df: pd.DataFrame):
    ### department stats
    with streamlit.expander("Analysis: Departments...", expanded=True):
        
        fig_dept_gender_count = plots.plot_dept_gender_count_sunburst(df)
        streamlit.plotly_chart(fig_dept_gender_count, use_container_width=True, key="dept_gender_sunburst")
        with streamlit.container():
            ## department stats table
            utils.sep()
            streamlit.markdown("###### Department Stats")
            df_dept_stats = data.get_dept_stats_df(df)

            # Round and convert only numeric columns
            numeric_cols = df_dept_stats.select_dtypes(include=['number']).columns
            df_dept_stats[numeric_cols] = df_dept_stats[numeric_cols].round(0).astype(int)

            streamlit.dataframe(
                df_dept_stats.style.background_gradient(cmap="Oranges"),
                use_container_width=True,
            )


def __build_exp_plots(df: pd.DataFrame):
    ### experience stat
    with streamlit.expander("Analysis: Work experience...", expanded=True):
        
        exp_stat_col1, exp_stat_col2 = streamlit.columns(2)
        with exp_stat_col1:
            fig_plot_tot_work_exp = plots.plot_tot_work_exp_bar(df)
            streamlit.plotly_chart(fig_plot_tot_work_exp, use_container_width=True, key="tot_work_exp")
        with exp_stat_col2:
            pct_at_cmp = data.get_pct_at_cmp(df)
            annot_text = __get_pct_at_cmp_annot_text(pct_at_cmp)
            fig_plot_cmp_work_exp = plots.plot_cmp_work_exp_scatter(df, annot_text)
            streamlit.plotly_chart(fig_plot_cmp_work_exp, use_container_width=True, key="cmp_work_exp")

def __get_pct_at_cmp_annot_text(pct_at_cmp):
    """Returns formatted annotation text for YearsAtCompany percentage plot."""
    annot_text = ""
    for key, value in zip(pct_at_cmp["YearsAtCompany"], pct_at_cmp["Percentage"]):
        try:
            key = str(key)
            value = float(value)
            annot_text += key + "\t: " + f"{value * 100:.2f}%<br>"
        except (ValueError, TypeError):
            annot_text += str(key) + "\t: Data Error<br>"
    return annot_text
