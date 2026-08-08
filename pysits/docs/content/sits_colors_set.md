Function to set sits color table

Includes new colors in the SITS color sets. If the colors exist, replace them
with the new HEX value. Optionally, the new colors can be associated to a
legend. In this case, the new legend name should be informed. The colors
parameter should be a `pandas.DataFrame` with name and HEX code. Colour
names should be one character string only. Composite names need to be combined
with underscores (e.g., use "Snow_and_Ice" and not "Snow and Ice").
This function changes the global sits color table and the global set of sits
color legends. To undo these effects, please use "sits_colors_reset()".

Args:
    colors (pandas.DataFrame): New color table with name and HEX code.
    legend (str): Legend associated to the color table (optional).

Returns:
    SITSFrame: A modified sits color table (invisible).

Examples:
    from pysits import *
    import pandas as pd

    # Define a color table based on the Anderson Land Classification System
    us_nlcd = pd.DataFrame({
        "name": [
            "Urban_Built_Up",
            "Agricultural_Land",
            "Rangeland",
            "Forest_Land",
            "Water",
            "Wetland",
            "Barren_Land",
            "Tundra",
            "Snow_and_Ice",
        ],
        "color": [
            "#85929E",
            "#F0B27A",
            "#F1C40F",
            "#27AE60",
            "#2980B9",
            "#D4E6F1",
            "#FDEBD0",
            "#EBDEF0",
            "#F7F9F9",
        ],
    })

    # Load the color table into `sits`
    sits_colors_set(colors=us_nlcd, legend="US_NLCD")

    # Show the new color table used by sits
    sits_colors_show("US_NLCD")

    # Change colors in the sits global color table
    # First show the default colors for the UMD legend
    sits_colors_show("UMD")
    # Then change some colors associated to the UMD legend
    mycolors = pd.DataFrame({
        "name": ["Savannas", "Grasslands"],
        "color": ["#F8C471", "#ABEBC6"],
    })
    sits_colors_set(colors=mycolors)
    # Notice that the UMD colors change
    sits_colors_show("UMD")
    # Reset the color table
    sits_colors_reset()
    # Show the default colors for the UMD legend
    sits_colors_show("UMD")
