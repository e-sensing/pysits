List the cloud collections supported by sits

Prints the collections available in each cloud service supported by sits.
Users can select to get information only for a single service by using the
`source` parameter.

Args:
    source (str): Data source to be shown in detail.

Returns:
    None: Prints collections available in each cloud service supported by
        sits.

Examples:
    from pysits import *

    # show the names of the collections supported by SITS
    sits_list_collections()
