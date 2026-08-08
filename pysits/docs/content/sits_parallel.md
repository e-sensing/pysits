Configure or query sits parallel processing

`sits_parallel` starts, restarts, stops, or gets a persistent `PSOCK`
cluster used by `sits` functions that support parallel processing.
To stop the cluster and free resources, call `sits_parallel(workers = 0)`
(recommended). Calling with `workers = 1` has the same effect (parallel
disabled).
When called with no arguments, `sits_parallel()` returns the current
cluster object. If no cluster is active, it returns `None`.

Args:
    workers (int): Number of workers to use. - `workers >= 2`: start or
        restart a `PSOCK` cluster with `workers` workers. -
        `workers <= 1`: stop any active cluster.
    log (bool): If `True`, enables worker log/debug mode.
    output_dir (str | pathlib.Path): Output directory where log files are
        written when `log = True`.

Returns:
    None: If called with no arguments, returns the current `parallel`
        cluster object or `None` if no cluster is active. If called with
        `workers`, returns `None`.

Notes:
    This function is intended for long pipelines and production
    environments where repeatedly creating and stopping clusters inside
    each `sits` call is expensive. After `sits_parallel(workers = N)` is
    called, `sits` functions can reuse the same cluster across multiple
    calls.
    When `workers >= 2`, worker processes inherit the current library
    paths (`.libPaths()`) and selected environment variables required for
    data access (for example, variables starting with `AWS_`).
    When the streaming GPU pipeline is enabled
    (`SITS_GPU_PIPELINE=stream`), `sits` functions attach the pipeline's
    read and write stages to this cluster instead of creating a private
    worker pool. Reads use at most `workers - 1` nodes and writes use one
    node, so for a classification with `multicores` read slots start the
    cluster with `workers = multicores + 1`.
