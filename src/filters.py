"""Handles dashboard filters"""

import data
import streamlit as st

def apply(df):
    """Filters the dataframe using active filters and returns the filtered dataframe."""
    
    # Get all filter elements from dataset
    filter_elem = data.get_filter_options(df)

    # Ensure "Active Employees" is always included in filters
    if "Active Employees" not in filter_elem:
        filter_elem["Active Employees"] = ["Yes", "No"]

    # Build UI and store user-selected filters
    user_filters = __build_filter_ui(df, filter_elem)

    # Apply filters to the dataframe
    df = __apply_filters(df, filter_elem, user_filters)

    return df

def __apply_filters(df, filter_elem, user_filters):
    """Applies filters based on user selection"""
    
    filter_conditions = []
    
    for key, selected_value in user_filters.items():
        if selected_value:  # Apply filter only if selection is made
            
            if key == "Active Employees":  # Special case
                if selected_value == "Yes":
                    filter_conditions.append("LastWorkingDay.isnull()")
                elif selected_value == "No":
                    filter_conditions.append("LastWorkingDay.notnull()")
            
            elif isinstance(selected_value, list) and selected_value:  # Categorical filter
                filter_conditions.append(f"{key} in {selected_value}")
            
            elif isinstance(selected_value, tuple):  # Numeric range filter
                filter_conditions.append(f"({selected_value[0]} <= {key} <= {selected_value[1]})")

    # Show Current Active Filters in Sidebar
    with st.sidebar.expander("Current Active Filters", expanded=True):
        if filter_conditions:
            st.markdown("🚀 " + " AND ".join(filter_conditions))
        else:
            st.markdown("🔹 No filters applied")

    # Apply the filter conditions to the dataframe
    return df.query(" and ".join(filter_conditions)) if filter_conditions else df


### Internal Functions
# def __build_filter_ui(df, filter_elem):
#     """Creates filter UI in sidebar"""
#     st.sidebar.markdown("# REPORT FILTERS")
#     st.sidebar.markdown("---")

#     # Reset filters if the user clicks 'Clear Filters'
#     if st.sidebar.button("Clear Filters"):
#         for key in filter_elem.keys():
#             session_key = f"filter_{key.replace(' ', '_')}"
            
#             if key == "Active Employees":
#                 st.session_state[session_key] = "All"  # Ensure valid default
#             elif isinstance(filter_elem[key], list) and isinstance(filter_elem[key][0], str):
#                 st.session_state[session_key] = []  # Clear categorical filters
#             elif isinstance(filter_elem[key], list) and isinstance(filter_elem[key][0], (int, float)):
#                 st.session_state[session_key] = (filter_elem[key][0], filter_elem[key][1])  # Reset range filters
        
#         st.sidebar.selectbox("Gender", ["All", "Male", "Female"], key="filter_Gender")
#         st.rerun()  # Force UI refresh
        
#     st.sidebar.markdown("---")

#     # Create a dictionary to store user-selected filters
#     user_filters = {}

#     # Iterate through filters and build UI
#     for key, options in filter_elem.items():
#         st.sidebar.markdown(f"**{key}**")  # Section title

#         # Ensure unique key for each filter to avoid Streamlit errors
#         unique_key = f"filter_{key.replace(' ', '_')}"

#         # Special handling for "Active Employees"
#         if key == "Active Employees":
#             user_filters[key] = st.sidebar.radio(
#                 "Show Active Employees?",
#                 options=["All", "Yes", "No"],
#                 index=0,  # Default to "All"
#                 key=unique_key,
#             )
#         elif isinstance(options[0], str):  # Categorical Filters
#             user_filters[key] = st.sidebar.multiselect(
#                 f"Select {key}",
#                 options=options,
#                 default=st.session_state.get(unique_key, []),  # No default selection
#                 key=unique_key,
#             )
#         else:  # Numeric Filters
#             user_filters[key] = st.sidebar.slider(
#                 f"Select {key} Range",
#                 min_value=int(options[0]),
#                 max_value=int(options[1]),
#                 value=st.session_state.get(unique_key, (int(options[0]), int(options[1]))),
#                 key=unique_key,
#             )

#         st.sidebar.markdown("---")  # Divider between filters

#     return user_filters  # Return user-selected filters

def __build_filter_ui(df, filter_elem):
    """Creates filter UI in sidebar"""
    st.sidebar.markdown("# REPORT FILTERS")
    st.sidebar.markdown("---")

    # Reset filters if the user clicks 'Clear Filters'
    if st.sidebar.button("Clear Filters"):
        for key in filter_elem.keys():
            session_key = f"filter_{key.replace(' ', '_')}"

            if key == "Active Employees":
                st.session_state[session_key] = "All"  # Ensure valid default

            elif key == "Gender":
                st.session_state[session_key] = ["Male", "Female"]  # Show both genders by default

            elif isinstance(filter_elem[key], list) and isinstance(filter_elem[key][0], str):
                st.session_state[session_key] = []  # Clear categorical filters

            elif isinstance(filter_elem[key], list) and isinstance(filter_elem[key][0], (int, float)):
                st.session_state[session_key] = (filter_elem[key][0], filter_elem[key][1])  # Reset range filters

        st.rerun()  # Force UI refresh

    st.sidebar.markdown("---")

    # Create a dictionary to store user-selected filters
    user_filters = {}

    # Iterate through filters and build UI
    for key, options in filter_elem.items():
        st.sidebar.markdown(f"**{key}**")  # Section title
        unique_key = f"filter_{key.replace(' ', '_')}"

        # Special handling for "Active Employees"
        if key == "Active Employees":
            user_filters[key] = st.sidebar.radio(
                "Show Active Employees?",
                options=["All", "Yes", "No"],
                index=0,
                key=unique_key,
            )

        # Special handling for "Gender"
        elif key == "Gender":
            gender_options = ["Male", "Female"]
            user_filters[key] = st.sidebar.multiselect(
                "Select Gender",
                options=gender_options,
                default=st.session_state.get(unique_key, gender_options),
                key=unique_key,
            )

        elif isinstance(options[0], str):  # Other categorical filters
            user_filters[key] = st.sidebar.multiselect(
                f"Select {key}",
                options=options,
                default=st.session_state.get(unique_key, []),
                key=unique_key,
            )

        else:  # Numeric Filters
            user_filters[key] = st.sidebar.slider(
                f"Select {key} Range",
                min_value=float(options[0]),
                max_value=float(options[1]),
                value=st.session_state.get(unique_key, (float(options[0]), float(options[1]))),
                step=0.1,
                key=unique_key,
            )

        st.sidebar.markdown("---")  # Divider between filters

    return user_filters

