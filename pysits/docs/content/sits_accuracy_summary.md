Print accuracy summary

Adaptation of the caret::print.confusionMatrix method for the more
common usage in Earth Observation.

Args:
    x (SITSConfusionMatrix): Accuracy assessment object.
    digits (int): Number of significant digits when printed.

Returns:
    SITSData: Called for side effects.
