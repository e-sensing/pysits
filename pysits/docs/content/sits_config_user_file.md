Create a user configuration file.

Creates a user configuration file.

Args:
    file_path (str | pathlib.Path): file to store the user
        configuration file.
    overwrite (bool): replace current configuration file?

Returns:
    None: called for side effects.

Examples:
    from pysits import *
    import tempfile

    user_file = tempfile.gettempdir() + "/my_config_file.yml"
    sits_config_user_file(user_file)
