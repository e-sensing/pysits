Function to save color table as QML style for data cube

Saves a color table associated to a classified data cube as a QGIS
style file

Args:
    cube (SITSCubeModel): a classified data cube.
    file (str | pathlib.Path): a QGIS style file to be written to.

Returns:
    None: called for side effects.

Examples:
    from pysits import *
    import os
    import tempfile

    data_dir = r_package_dir("extdata/raster/classif", package="sits")
    ro_class = sits_cube(
        source="MPC",
        collection="SENTINEL-2-L2A",
        data_dir=data_dir,
        parse_info=[
            "X1", "X2", "tile", "start_date", "end_date",
            "band", "version"
        ],
        bands="class",
        labels={
            "1": "Clear_Cut_Burned_Area",
            "2": "Clear_Cut_Bare_Soil",
            "3": "Clear_Cut_Vegetation",
            "4": "Forest"
        }
    )
    qml_file = os.path.join(tempfile.gettempdir(), "qgis.qml")
    sits_colors_qgis(ro_class, qml_file)
