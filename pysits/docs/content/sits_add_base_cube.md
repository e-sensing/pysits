Add base maps to a time series data cube

This function add base maps to time series data cube. Base maps have
information that is stable in time (e.g, DEM) which provide relevant
information for modelling and classification.
To add a base cube to an existing data cube, they should share the same
sensor, resolution, bounding box, timeline, and have different bands.

Args:
    cube1 (SITSCubeModel): Data cube.
    cube2 (SITSCubeModel): Base data cube (e.g., DEM).

Returns:
    SITSCubeModel: a merged data cube with the inclusion of base
        information.

Examples:
    from pysits import *
    import tempfile
    import os

    s2_cube = sits_cube(
        source="MPC",
        collection="SENTINEL-2-L2A",
        tiles="18HYE",
        bands=["B8A", "CLOUD"],
        start_date="2022-01-01",
        end_date="2022-03-31"
    )
    output_dir = os.path.join(tempfile.gettempdir(), "reg")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    dem_cube = sits_cube(
        source="MPC",
        collection="COP-DEM-GLO-30",
        tiles="18HYE",
        bands="ELEVATION"
    )
    s2_reg = sits_regularize(
        cube=s2_cube,
        period="P1M",
        res=240,
        output_dir=output_dir,
        multicores=2,
        memsize=4
    )
    dem_reg = sits_regularize(
        cube=dem_cube,
        res=240,
        tiles="18HYE",
        output_dir=output_dir,
        multicores=2,
        memsize=4
    )
    s2_reg = sits_add_base_cube(s2_reg, dem_reg)
