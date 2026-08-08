Print accuracy summary

Adaptation of the caret::print.confusionMatrix method for the more common
usage in Earth Observation.

Args:
    x (SITSConfusionMatrix): accuracy object to summarize.
    digits (int): number of significant digits when printed.

Returns:
    SITSData: called for side effects.
