"""Capacity tab rendering functionality"""

import pandas as pd
import streamlit as st
import utils
import data
import plots
import pymysql
from config import db_config

# Main render function
def render(df: pd.DataFrame):
    # Show available columns for debugging
    # st.write("Available columns:", df.columns.tolist())

    # Compute and display top/bottom performers based on filtered df
    df_top, df_bottom = compute_top_bottom_performers(df)

    with st.expander("🏆 View Top & Bottom Performers", expanded=False):
        st.subheader("🏆 Top 5 Performers")
        if not df_top.empty:
            st.dataframe(df_top)
            csv_top = df_top.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Top 5 as CSV",
                data=csv_top,
                file_name='top_5_performers.csv',
                mime='text/csv'
            )
        else:
            st.info("Top performers data is not available for the selected filter.")

        st.subheader("📉 Bottom 5 Performers")
        if not df_bottom.empty:
            st.dataframe(df_bottom)
            csv_bottom = df_bottom.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Bottom 5 as CSV",
                data=csv_bottom,
                file_name='bottom_5_performers.csv',
                mime='text/csv'
            )
        else:
            st.info("Bottom performers data is not available for the selected filter.")

    st.markdown("---")

    # Show KPI cards and plots
    __build_kpi_cards(df)
    __build_dept_promo_retrench_plots(df)


# Compute top/bottom performers from the filtered DataFrame
def compute_top_bottom_performers(df):
    """Compute top 5 and bottom 5 performers directly from DB (ignoring filter for accurate columns)."""

    conn = pymysql.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        db=db_config["database"]
    )

    
    df = df[df['LastWorkingDay'].isnull()]

    if df.empty:
        return pd.DataFrame(), pd.DataFrame()

    # Compute performance score
    max_hike = df["PercentSalaryHike"].max()
    df["PerformanceScore"] = (
        0.4 * df["PerformanceRating"]
        + 0.2 * df["JobInvolvement"]
        + 0.2 * df["JobSatisfaction"]
        + 0.2 * (df["PercentSalaryHike"] / max_hike)
    )

    df_top = df.sort_values("PerformanceScore", ascending=False).head(5)
    df_bottom = df.sort_values("PerformanceScore", ascending=True).head(5)
    return df_top, df_bottom


# KPI Cards
def __build_kpi_cards(df):
    with st.expander("Overall promotion & retrenchment stats...", expanded=True):
        promo_col, retrench_col = st.columns(2)
        with promo_col:
            __show_promotion_stats(df)
        with retrench_col:
            __show_retrench_stats(df)


# Promotion stats
def __show_promotion_stats(df):
    promo_cnt, not_promo_cnt, promo_pct, no_promo_pct = data.get_promo_count(df)
    utils.render_card(
        key="promo_card",
        title="Promote",
        value=promo_cnt,
        secondary_text=f" ({promo_pct})%",
        icon="fa-sharp fa-solid fa-user-check fa-xs",
        progress_value=int(promo_pct),
        progress_color="green",
    )
    utils.render_card(
        key="no_promo_card",
        title="No Promotion",
        value=not_promo_cnt,
        secondary_text=f" ({no_promo_pct})%",
        icon="fa-sharp fa-solid fa-user-xmark fa-xs",
        progress_value=int(no_promo_pct),
        progress_color="red",
    )
    fig = plots.plot_promotion_donut(df)
    st.plotly_chart(fig, use_container_width=True, key="promotion_donut_chart")


# Retrenchment stats
def __show_retrench_stats(df):
    retrench_cnt, not_retrench_cnt, retrench_pct, not_retrench_pct = data.get_retrench_count(df)
    utils.render_card(
        key="no_retrench_card",
        title="No Retrench",
        value=not_retrench_cnt,
        secondary_text=f" ({not_retrench_pct})%",
        icon="fa-sharp fa-solid fa-user-plus fa-xs",
        progress_value=int(not_retrench_pct),
        progress_color="green",
    )
    utils.render_card(
        key="retrench_card",
        title="Retrench",
        value=retrench_cnt,
        secondary_text=f" ({retrench_pct})%",
        icon="fa-sharp fa-solid fa-user-minus fa-xs",
        progress_value=int(retrench_pct),
        progress_color="red",
    )
    fig = plots.plot_retrench_donut(df)
    st.plotly_chart(fig, use_container_width=True, key="retrench_donut_chart")


# Department-wise plots
def __build_dept_promo_retrench_plots(df):
    with st.expander("Analysis: Department wise promotion & retrenchment...", expanded=True):
        promo_col, retrench_col = st.columns(2)
        with promo_col:
            df_promo = data.get_dept_promo_pct(df)
            fig = plots.plot_dept_promo_bar(df_promo)
            st.plotly_chart(fig, use_container_width=True, key="dept_promo_bar_chart")
        with retrench_col:
            df_retrench = data.get_dept_retrench_pct(df)
            fig = plots.plot_dept_retrench_bar(df_retrench)
            st.plotly_chart(fig, use_container_width=True, key="dept_retrench_bar_chart")
