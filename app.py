import plotly.express as px
from palmerpenguins import load_penguins
from shiny.express import input, ui, render
from shinywidgets import render_widget, render_plotly
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

penguins = load_penguins()

ui.page_opts(title="Penguins Dashboard", fillable=True)

with ui.sidebar(position="right", bg="#f8f8f8", open="open"):
    ui.h2("Interactive Options")
#  Dropdown input to choose a column
    ui.input_selectize(  
        "select_attribute",  
        "Select column to visualize",  
        choices=["bill_length_mm","bill_depth_mm","flipper_length_mm", "body_mass_g"],
        selected=["bill_length_mm"])

    ui.input_numeric("plotly_bin_count", "Plotly bin numeric",1,min=1,max=10)
    
    ui.input_slider("seaborn_bin_count", "Seaborn bin count", 10, 100, 20,
                    step=5, animate=True)
    ui.input_checkbox_group(
        "selected_species_list",
        "Select a species",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        selected="Adelie", inline=True)
    ui.hr()
    ui.h5("GitHub Code Repository")
    ui.a("cintel-02-data", href="https://github.com/bncodes19/cintel-02-data", target="_blank")

with ui.layout_columns():
#   a Plotly Histogram
    with ui.card():
        ui.card_header("Plotly Histogram")
        @render_plotly
        def plotly_histogram():
            return px.histogram(penguins,x=input.selected_attribute(),nbins=input.plotly_bin_count(),color="species")

with ui.layout_columns():
#   a DataTable (showing all data)
    with ui.card():
        ui.card_header("Data Table")
        @render.data_frame
        def data_table():
            return render.DataTable(penguins) 
#   a Data Grid (showing all data)
    with ui.card():
        ui.card_header("Data Grid")
        @render.data_frame
        def data_grid():
            return render.DataGrid(penguins)

with ui.layout_columns():
#    a Plotly Scatterplot (showing all species)
    with ui.card():
        ui.card_header("All Species (Plotly Scatterplot)")
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                data_frame=penguins, x="body_mass_g", y="bill_depth_mm",
                color="species",
                labels={"bill_depth_mm": "Bill Depth (grams)",
                    "body_mass_g": "Body Mass (millimeters)"},)

#    a Seaborn Histogram (showing all species)
    with ui.card():
        ui.card_header("All Species (Seaborn Histogram)")
        @render.plot
        def seaborn_histogram():
            hist = sns.histplot(data=penguins, x="body_mass_g", bins=input.seaborn_bin_count())  
            hist.set_xlabel("Mass (grams)")
            hist.set_ylabel("Count")
            return hist
