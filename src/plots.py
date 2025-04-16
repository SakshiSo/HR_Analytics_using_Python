"""All app-specific plots are implemented here"""

import plotly.express as px
import plotly.io as io
import pandas as pd
from pandas import DataFrame
from plotly.graph_objects import Figure
from config import plot_config

# setup app-wide plotly theme
io.templates.default = plot_config.theme

### Summary tab plots

def plot_age_hist(df: DataFrame) -> Figure:
    fig = px.histogram(
        data_frame=df,
        x="Age",
        marginal="violin",
        title="Employee's age distribution overall",
        color_discrete_sequence=plot_config.cat_color_map,
    )
    return fig


def plot_age_marital_status_pie(df: DataFrame) -> Figure:
    df_group = (
        df.groupby("MaritalStatus", as_index=False)
        .size()
        .sort_values(by="size", ascending=True)
    )
    fig = px.pie(
        data_frame=df_group,
        names="MaritalStatus",
        values="size",
        color="MaritalStatus",
        hole=0.7,
        title="Employee count by marital-status",
        color_discrete_sequence=plot_config.cat_color_map,
    ).update_traces(textfont_color="white")
    return fig


def plot_age_marital_status_box(df: DataFrame) -> Figure:
    fig = px.box(
        data_frame=df,
        x="MaritalStatus",
        y="Age",
        color="MaritalStatus",
        title="Employee's age distribution by marital-status",
        color_discrete_sequence=plot_config.cat_color_map,
    )
    return fig


def plot_age_gender_box(df: DataFrame) -> Figure:
    fig = px.box(
        data_frame=df,
        x="Gender",
        y="Age",
        color="Gender",
        title="Employee's age distribution by gender",
        color_discrete_sequence=plot_config.cat_color_map,
    )
    return fig


def plot_dept_gender_count_sunburst(df: DataFrame) -> Figure:
    df_group = (
        df.groupby(["Department", "Gender"], as_index=False)
        .size()
        .assign(Top="Company")
    )
    fig = px.sunburst(
        data_frame=df_group,
        path=["Top", "Department", "Gender"],
        values="size",
        color_discrete_sequence=px.colors.qualitative.T10,
        title="Employee count in each department<br>segmented by gender",
    )
    fig.update_traces(
        textfont_color="white",
        textinfo="label+percent parent",
        textfont_size=18,
    )
    fig.update_layout(
        margin=dict(t=20, l=0, r=0, b=0),
        autosize=False,
        height=700,
    )

    return fig


def plot_dept_curr_mgr_scatter(df: DataFrame) -> Figure:
    df_group = (
        df.groupby("Department")["YearsWithCurrentManager"]
        .mean()
        .to_frame()
        .reset_index()
        .sort_values(by="YearsWithCurrentManager", ascending=False)
    )
    fig = px.scatter(
        data_frame=df_group,
        x="YearsWithCurrentManager",
        y="Department",
        color="Department",
        size="YearsWithCurrentManager",
        title="Avg number of years with curr manager",
    )
    return fig


def plot_tot_work_exp_bar(df):
    tot_emp = len(df)
    
    # Define experience ranges
    bins = [0, 5, 10, 15, 20, 25, 30, float("inf")]
    labels = ["0-5", "6-10", "11-15", "16-20", "21-25", "26-30", "30+"]
    
    # Create experience groups
    df["WorkExperienceRange"] = pd.cut(df["WorkExperience"], bins=bins, labels=labels, right=True)
    
    # Group by experience range
    df_group = df.groupby("WorkExperienceRange", as_index=False).size()
    df_group["size"] = df_group["size"] / tot_emp * 100

    # Sort the ranges in correct order
    df_group["WorkExperienceRange"] = pd.Categorical(df_group["WorkExperienceRange"], categories=labels, ordered=True)
    df_group = df_group.sort_values(by="WorkExperienceRange", ascending=False)

    # Create horizontal bar plot
    fig = px.bar(
        data_frame=df_group,
        x="size",
        y="WorkExperienceRange",
        color="WorkExperienceRange",
        color_discrete_sequence=plot_config.cat_color_map,  # Ensure colors are soft
        orientation="h",
        title="Total Workforce Distribution by Work Experience",
    ).update_traces(
        text=df_group["size"].apply(lambda x: f"{x:.1f}%"),
        textposition="inside",
        textfont_color="white",
    )

    fig.update_layout(
        xaxis_title="% of Employees",
        yaxis_title="Work Experience",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,  # Hide legend for cleaner visualization
    )

    return fig


def plot_cmp_work_exp_scatter(df, annot_text):
    fig = px.scatter(
        data_frame=df,
        x="TotalWorkingYears",
        y="YearsAtCompany",
        size="PctAtCompany",
        color="PctAtCompany",
        opacity=0.7,  # Increased for better visibility
        color_continuous_scale="Reds",  # Enhanced contrast
    )

    # Add annotation outside the plot to avoid overlap
    fig.add_annotation(
        x=1.02,  # Moved outside the main chart area
        y=0.5,  # Centered vertically
        xref="paper",
        yref="paper",
        text=annot_text,
        align="left",
        showarrow=False,
        font=dict(family="Arial", size=14, color="white"),
        bordercolor="black",
        borderwidth=1,
        borderpad=4,
        bgcolor="rgba(76, 120, 168, 0.8)",  # Semi-transparent blue
    )

    # Improve layout
    fig.update_layout(
        xaxis_title="Total Working Years",
        yaxis_title="Years at Company",
        coloraxis_colorbar_title="% at Company",
        plot_bgcolor="rgba(0,0,0,0)",  # Clean background
        paper_bgcolor="rgba(0,0,0,0)",
    )

    # Improve marker appearance
    fig.update_traces(marker=dict(line=dict(width=0.5, color="white")))

    return fig


###
### Capacity tab plots - Promotion and Retrenchment
###
def plot_promotion_donut(df):
    df_group = (
        df["ToBePromoted"]
        .value_counts()
        .to_frame()
        .reset_index()
        .rename({"ToBePromoted": "Promotion", "count": "Count"}, axis=1)
    )
    fig = px.pie(
        df_group,
        names="Promotion",
        values="Count",
        hole=0.6,
        color_discrete_sequence=plot_config.cat_color_map,
        title="Company wide promotion",
    )
    fig.update_layout(
        legend_title_text="Promotion?",
        margin=dict(t=45, l=0, r=0, b=0),
    )
    fig.update_traces(pull=[0.1, 0])
    return fig


def plot_retrench_donut(df):
    df_group = (
        df["ToBeRetrenched"]
        .value_counts()
        .to_frame()
        .reset_index()
        .rename({"ToBeRetrenched": "Retrench", "count": "Count"}, axis=1)
    )

    fig = px.pie(
        df_group,
        names="Retrench",
        values="Count",
        hole=0.6,
        color_discrete_sequence=plot_config.cat_color_map_r,
        title="Company wide retrenchment",
    )
    fig.update_layout(
        legend_title_text="Retrench?",
        margin=dict(t=45, l=0, r=0, b=0),
    )
    fig.update_traces(pull=[0.1, 0])
    return fig


def plot_dept_promo_bar(df):
    fig = px.bar(
        data_frame=df,
        x="Department",
        y="PromotionPercentage",
        color="Department",
        barmode="group",
        color_discrete_sequence=plot_config.cat_color_map,
        title="To be promoted<br>in each department",
    )
    fig.update_traces(
        texttemplate="%{y:.1f}%",
        textposition="auto",
        textfont_color="white",
    )
    return fig


def plot_dept_retrench_bar(df):
    df_group = df
    fig = px.bar(
        data_frame=df_group,
        x="Department",
        y="RetrenchPercentage",
        color="Department",
        barmode="group",
        color_discrete_sequence=plot_config.cat_color_map_r,
        title="To be retrenched<br>in each department",
    )
    fig.update_traces(
        texttemplate="%{y:.1f}%",
        textposition="auto",
        textfont_color="white",
    )
    return fig


###
### Capacity tab plots - Attrition
###
def plot_dept_attrition(df):
    fig = px.pie(
        data_frame=df,
        names="Department",
        values="AttritionCount",
        hole=0.4,
        color_discrete_sequence=plot_config.cat_color_map_r,
        title="Attrition by Department",
    )
    fig.update_traces(
        textfont_color="white", textinfo="label+percent", showlegend=False
    )
    fig.update_layout(
        legend_title_text="Department",
        # margin=dict(t=0, l=0, r=0, b=0),
    )
    return fig


def plot_gender_attrition(df):
    fig = px.pie(
        data_frame=df,
        names="Gender",
        values="% Attrition",
        hole=0.4,
        color_discrete_sequence=plot_config.cat_color_map_r,
        title="Attrition by Gender",
    ).update_traces(textfont_color="white", textinfo="label+percent", showlegend=False)
    fig.update_layout(
        legend_title_text="Gender",
    )
    return fig


def plot_dist_attrition(df):
    fig = px.bar(
        data_frame=df,
        y="WorkplaceProximity",
        x="% Attrition",
        color="WorkplaceProximity",
        color_discrete_sequence=plot_config.cat_color_map_r,
        title="Attrition by Distance",
        orientation="h"
    )
    fig.update_traces(
        texttemplate="%{x:.1f}%",
        textposition="auto",
        textfont_color="white",
        showlegend=False,
    )
    return fig


def plot_jobrole_attrition(df):
    fig = px.bar(
        data_frame=df,
        x="JobRole",
        y="AttritionCount",
        color="JobRole",
        color_discrete_sequence=plot_config.cat_color_map,
        title="Attrition by Job Role",
    )
    fig.update_traces(
        texttemplate="%{y:.1f}%",
        textposition="auto",
        textfont_color="white",
        showlegend=False,
    )
    return fig


def plot_satis_attrition(df):
    fig = px.bar(
        data_frame=df,
        y="JobSatisfaction",
        x="% Attrition",
        color="JobSatisfaction",
        color_discrete_sequence=plot_config.cat_color_map,
        title="Attrition by Job Satisfaction",
        orientation="h",
    )
    fig.update_traces(
        texttemplate="%{x:.1f}%",
        textposition="auto",
        textfont_color="white",
        showlegend=False,
    )
    return fig


def plot_ages_attrition(df):
    # Define age groups
    bins = [20, 25, 30, 35, 40, 45, 50, 55, 60]
    labels = ["20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55+"]
    df["Age Group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)

    # Aggregate by age group
    df_grouped = df.groupby("Age Group")["% Attrition"].mean().reset_index()

    # Define a subtle color palette
    color_palette = ["#7f8c8d", "#3498db", "#9b59b6", "#e67e22", "#f1c40f", "#1abc9c", "#2c3e50", "#d35400"]

    # **Reverse the order of Age Groups**
    df_grouped["Age Group"] = pd.Categorical(df_grouped["Age Group"], categories=labels[::-1], ordered=True)
    df_grouped = df_grouped.sort_values("Age Group")

    fig = px.bar(
        data_frame=df_grouped,
        y="Age Group",
        x="% Attrition",
        text="% Attrition",
        title="Attrition by Age",
        orientation="h",
        color="Age Group",  # Different colors for each bar
        color_discrete_sequence=color_palette,  # Apply subtle colors
    )

    fig.update_traces(
        texttemplate="%{x:.1f}%", 
        textposition="inside",
    )

    fig.update_layout(
        xaxis_title="% Attrition",
        yaxis_title="Age Group",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,  # Hide legend for simplicity
    )

    return fig

def plot_exp_attrition(df):
    # Bin work experience into groups
    bins = [0, 5, 10, 15, 20, 25, 30, 35]
    labels = ["0-5", "6-10", "11-15", "16-20", "21-25", "26-30", "30+"]
    df["Experience Group"] = pd.cut(df["WorkExperience"], bins=bins, labels=labels, right=False)

    # Aggregate by experience group
    df_grouped = df.groupby("Experience Group")["% Attrition"].mean().reset_index()

    # Define a subtle color palette
    color_palette = ["#7f8c8d", "#3498db", "#9b59b6", "#e67e22", "#f1c40f", "#1abc9c", "#2c3e50"]

    # **Reverse the order of Experience Groups**
    df_grouped["Experience Group"] = pd.Categorical(df_grouped["Experience Group"], categories=labels[::-1], ordered=True)
    df_grouped = df_grouped.sort_values("Experience Group")

    fig = px.bar(
        data_frame=df_grouped,
        y="Experience Group",
        x="% Attrition",
        text="% Attrition",
        title="Attrition by Work Experience",
        orientation="h",
        color="Experience Group",  # Different colors for each bar
        color_discrete_sequence=color_palette,  # Apply subtle colors
    )

    fig.update_traces(
        texttemplate="%{x:.1f}%", 
        textposition="inside",
    )

    fig.update_layout(
        xaxis_title="% Attrition",
        yaxis_title="Work Experience",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,  # Hide legend for simplicity
    )

    return fig