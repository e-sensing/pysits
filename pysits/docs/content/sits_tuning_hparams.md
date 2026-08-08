Tuning machine learning models hyper-parameters

This function allow user building the hyper-parameters space used by
`sits_tuning()` function search randomly the best parameter combination.
Users should pass the possible values for hyper-parameters as constants or by
calling the following random functions:
- `uniform(min = 0, max = 1, n = 1)`: returns random numbers from a uniform
  distribution with parameters min and max.
- `choice(..., replace = True, n = 1)`: returns random objects passed to
  `**kwargs` with replacement or not (parameter `replace`).
- `randint(min, max, n = 1)`: returns random integers from a uniform
  distribution with parameters min and max.
- `normal(mean = 0, sd = 1, n = 1)`: returns random numbers from a normal
  distribution with parameters min and max.
- `lognormal(meanlog = 0, sdlog = 1, n = 1)`: returns random numbers from a
  lognormal distribution with parameters min and max.
- `loguniform(minlog = 0, maxlog = 1, n = 1)`: returns random numbers from a
  loguniform distribution with parameters min and max.
- `beta(shape1, shape2, n = 1)`: returns random numbers from a beta
  distribution with parameters min and max.
These functions accepts `n` parameter to indicate how many values should be
returned.

Args:
    **kwargs (dict): Used to prepare hyper-parameter space.

Returns:
    TuningFunctionCall: the hyper-parameter space to be passed to
        `sits_tuning()`'s `params` parameter.
