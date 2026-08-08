Convert tile information to ROI in WGS84

Takes a list of tiles from a given grid system and produces a ROI
(region of interest) in WGS84 covering them.

Args:
    tiles (list[str]): Names of tiles from the selected `grid_system`.
    grid_system (str): Grid system that the `tiles` belong to. Currently
        supported grid systems are the MGRS grid (`"MGRS"`, default) and
        those used by the Brazil Data Cube (`"BDC_LG_V2"`, `"BDC_MD_V2"`
        and `"BDC_SM_V2"`).

Returns:
    SITSNamedVector: Valid ROI to use in other SITS functions.

Examples:
    from pysits import *

    # Convert MGRS tiles to a ROI
    roi = sits_tiles_to_roi(["22KGA", "22KGV"])

    # Convert Brazil Data Cube (large grid) tiles to a ROI
    roi = sits_tiles_to_roi(
        ["003004", "003005"], grid_system="BDC_LG_V2"
    )
