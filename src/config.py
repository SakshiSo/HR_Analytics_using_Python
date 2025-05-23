"""All app-specific user defined configurations are defined here"""

from dataclasses import dataclass

import plotly.express as px

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Daql@749#kdp6",
    "database": "hr_analytics"
}
### define all app-wide configuration here, should not be accessed directly hence leading "__"
@dataclass
class __PlotConfig:
    """All plotting configurations are defined here"""

    # Available themes (templates):
    # ['ggplot2', 'seaborn', 'simple_white', 'plotly',
    #  'plotly_white', 'plotly_dark', 'presentation',
    #  'xgridoff', 'ygridoff', 'gridon', 'none']
    theme = "plotly_dark"
    cat_color_map = px.colors.qualitative.T10
    cat_color_map_r = px.colors.qualitative.T10_r
    cont_color_map = px.colors.sequential.amp
    cont_color_map_r = px.colors.sequential.amp_r


### define all app-wide configuration here, should not be accessed directly hence leading "__"
@dataclass
class __AppConfig:
    """All app-wide configurations are defined here"""

  


### make configs available to any module that imports this module
app_config = __AppConfig()
plot_config = __PlotConfig()
