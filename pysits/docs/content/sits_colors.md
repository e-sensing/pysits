Function to retrieve sits color table

Returns the default color table.

Args:
    legend (str): One of the accepted legends in sits.

Returns:
    SITSFrame: color names and values.

Notes:
    SITS has a predefined color palette with 238 class names. These colors are
    grouped by typical legends used by the Earth observation community, which
    include "IGBP", "UMD", "ESA_CCI_LC", and "WORLDCOVER". Use
    `sits_colors_show` to see a specific palette. The default color table can
    be extended using `sits_colors_set`.

Examples:
    from pysits import *

    # return the names of all colors supported by SITS
    sits_colors()
