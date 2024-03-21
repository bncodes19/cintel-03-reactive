import plotly.express as px
from palmerpenguins import load_penguins
from shiny.express import input, ui, render
from shiny import reactive
from shinywidgets import render_widget, render_plotly
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#   Load penguins dataset into a dataframe
penguins_df = load_penguins()

#   Interactive Dashboard Title
ui.page_opts(title="Penguins Dashboard", fillable=True)

#   Interactive Sidebar Options
with ui.sidebar(position="right", bg="#f8f8f8", open="open"):
    ui.h2("Interactive Options")
    ui.input_selectize("select_attribute","Select attribute",
                       choices=["bill_length_mm","bill_depth_mm","flipper_length_mm", "body_mass_g"],
                       selected=["bill_length_mm"])
    ui.input_numeric("plotly_bin_count", "Plotly bin numeric",20,min=1,max=100)    
    ui.input_slider("seaborn_bin_count", "Seaborn bin count", 10, 100, 20,step=5, animate=True)
    ui.input_checkbox_group("selected_species_list","Select a species",
                            choices=["Adelie", "Gentoo", "Chinstrap"],selected=["Adelie", "Gentoo", "Chinstrap"], inline=True)
    ui.input_checkbox_group("selected_island_list","Select an island",
                            choices=["Torgersen", "Biscoe", "Dream"],selected=["Torgersen", "Biscoe", "Dream"], inline=True)
    ui.input_select(  
    "selected_sex_list","Select Sex (M/F)",{"male": "Male", "female": "Female"},selected=["male","female"],multiple=True)
    ui.hr()
    ui.h5("GitHub Code Repository")
    ui.a("cintel-03-reactive", href="https://github.com/bncodes19/cintel-03-reactive/blob/main/app.py", target="_blank")

#   a Plotly Histogram (showing all species)
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram")
        @render_plotly
        def plotly_histogram():
            return px.histogram(
                filtered_data(),
                x=input.select_attribute(),
                nbins=input.plotly_bin_count(),
                color="species")

with ui.layout_columns():
#   a DataTable (showing all data)
    with ui.card():
        ui.card_header("Data Table")
        @render.data_frame
        def data_table():
            return render.DataTable(filtered_data()) 
#   a Data Grid (showing all data)
    with ui.card():
        ui.card_header("Data Grid")
        @render.data_frame
        def data_grid():
            return render.DataGrid(filtered_data())

#    a Plotly Scatterplot (showing all species)
with ui.layout_columns():
    with ui.card():
        ui.card_header("All Species (Plotly Scatterplot)")
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                data_frame=filtered_data(), x="body_mass_g", y="bill_depth_mm",
                color="species",
                labels={"bill_depth_mm": "Bill Depth (grams)",
                    "body_mass_g": "Body Mass (millimeters)"},)

#    a Seaborn Histogram (showing all species)
    with ui.card():
        ui.card_header("All Species (Seaborn Histogram)")
        @render.plot
        def seaborn_histogram():
            hist = sns.histplot(data=filtered_data(), x="body_mass_g", bins=input.seaborn_bin_count())  
            hist.set_xlabel("Mass (grams)")
            hist.set_ylabel("Count")
            return hist

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.
    
    @reactive.calc
    def filtered_data():
        species_input = input.selected_species_list()
        island_input = input.selected_island_list()
        sex_input = input.selected_sex_list()
        filtered_data = penguins_df[ (penguins_df['species'].isin(species_input))
                                   & (penguins_df['island'].isin(island_input))
                                   & (penguins_df['sex'].isin(sex_input))]
        return filtered_data
