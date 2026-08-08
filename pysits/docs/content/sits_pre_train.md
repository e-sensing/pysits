Pre-train deep learning models for sits

Runs self-supervised and pre-training for Earth observation time series
using `sits`. The result of the function is an embedding model that can
be used to produce embeddings from Earth observation data cubes.
The function is a thin wrapper that validates inputs and dispatches to a
user-selected deep learning pre-training method. The method is
responsible for preparing training data, fitting the model, and
returning an encoder that can be used later by `sits_encode`.
Pre-training methods are created by factory functions available. The
package offers three self-supervised learning methods:
- `sits_ssl_lejepa` based on the LeJEPA method proposed by Balestriero
  and LeCun (2025);
- `sits_ssl_vicreg` based on the VICReg method proposed by Bardes,
  Ponce, and LeCun (2022);
- `sits_ssl_mae` based on masked autoencoders adapted to image time
  series, similar to Tseng et al. (2024).
Two supervised learning methods are available:
- `sits_contrastive_learning` that adapts the supervised contrastive
  learning proposed by Khosla et al.(2020) to image time series.
- `sits_barlow_twins` that is a version for labelled time series of the
  approach proposed by Zbontar et al.(2021)
These factories return a function (closure) that implements the full
pre-training procedure when called with `samples`.

Args:
    samples (SITSTimeSeriesModel): Time-series samples. Labels are
        optional and may or may not be used depending on the selected
        pre-training method.
    rl_method (SITSRepresentationLearningMethod): A pre-training
        representation learning method used to build an encoder that
        generates embeddings (e.g., `sits_ssl_lejepa()` or
        `sits_contrastive_learning()`). It must be a function that
        takes `samples` and returns an encoder.

Returns:
    SITSRepresentationLearningMethod: A pre-trained deep learning
    encoder and the metadata required for subsequent encoding (e.g.,
    band order, feature naming, and normalization statistics, when
    applicable).

Examples:
    from pysits import *

    mae_model = sits_pre_train(
        samples=samples_modis_ndvi,
        rl_method=sits_ssl_mae(
            encoder_model=sits_tempcnn(),
            mask_ratio=0.5
        )
    )
