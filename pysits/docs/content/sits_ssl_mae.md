Pre-train a Masked Autoencoder for self-supervised learning of time series

`sits_ssl_mae()` Implements a masked autoencoder (MAE) algorithm. It performs
self-supervised learning by masking a subset of timesteps in each sample time
series, training an encoder-decoder model to reconstruct the original signal,
and returning the pretrained encoder as a `torch` module.
The function can be used in two ways:
- If `samples` is provided, it trains immediately and returns an encoder-ready
  model object (see Value).
- If `samples = None`, it returns a training function with signature
  `function(samples)` that can be passed to `sits_pre_train` or called later.

During training, the procedure:
1. Masks each sample time series according to `masking_method`, `mask_ratio`,
   `mask_value`, and `masked_bands`.
2. Normalizes inputs and targets using quantile-based statistics derived from
   the original samples.
3. Splits data into training and validation partitions according to
   `validation_split`.
4. Trains an encoder-decoder model with a masked MSE objective, where loss is
   computed only over masked positions.
5. Applies early stopping and step learning-rate scheduling.
6. Discards the decoder after training, returning the pretrained encoder for
   use in downstream tasks.
The decoder used during pretraining is a multilayer perceptron (MLP)
specifically designed for MAE reconstruction. This decoder maps latent
embeddings back to full time-series representations before being discarded
after pretraining.
Note: unlike the original vision MAE (He et al., 2022), where the encoder
processes only visible (unmasked) patches, this implementation feeds the full
time series to the encoder with masked positions replaced by `mask_value`. This
simplification is standard for temporal data and functions as a denoising
autoencoder variant of the MAE objective.
When GPU execution is enabled in the environment, training may run on GPU via
`luz` accelerators. Otherwise, it runs on CPU.

Args:
    samples (SITSTimeSeriesModel): Samples object. If `None` (default),
        returns a training function. If provided, triggers immediate
        training. Base data samples are not supported.
    embedding_dim (int): Dimensionality of the latent embedding produced by
        the encoder (Default: 32).
    encoder_model (SITSMachineLearningMethod): Deep learning method that
        takes time series as input and produces latent representations that
        are used to compute the loss function (suggested options:
        `sits_tempcnn()`, `sits_lighttae()`, `sits_resnet()`). Default:
        `sits_tempcnn()`.
    decoder_width (int): Width of the decoder MLP hidden layer.
    dropout_rate (float): Dropout rates (0,1) for the linear module of the
        decoder.
    masking_method (str): Mask selection strategy. Options are `"random"`
        or `"contiguous"`.
    mask_ratio (float): Fraction of timesteps to mask, in (0, 1).
    mask_value (float): Fill value used for masked timesteps.
    masked_bands (list[str]): Which bands to mask. If `None`, all bands are
        eligible for masking.
    epochs (int): Maximum number of training epochs.
    batch_size (int): Batch size used for training and validation.
    validation_split (float): Fraction of samples held out for validation
        loss monitoring, in (0, 1).
    optimizer: A `torch` optimizer constructor, such as
        `torch::optim_adamw`.
    opt_hparams (dict): Optimizer hyperparameters passed to `optimizer`.
        Common entries include `lr`, `eps`, and `weight_decay`. Only
        parameters supported by the chosen optimizer are accepted.
    lr_decay_epochs (int): Step size (in epochs) for learning-rate decay
        when using the step scheduler.
    lr_decay_rate (float): Multiplicative decay factor applied by the
        learning-rate scheduler.
    patience (int): Number of epochs without improvement in validation loss
        before early stopping.
    min_delta (float): Minimum decrease in validation loss required to reset
        the early-stopping patience counter.
    verbose (bool): If `True`, prints training progress and per-epoch losses.
    seed (int): Random seed used to initialize Torch randomness.

Returns:
    R: If `samples = None`, returns a training function with signature
    `function(samples)` that trains an MAE and returns a pretrained encoder (a
    `torch` module).
    If `samples` is provided, returns the result of applying the training
    function to `samples` (i.e., a pretrained encoder-ready model object used
    by the pretraining pipeline).

Examples:
    from pysits import *

    model = sits_pre_train(
        samples_modis_ndvi,
        sits_ssl_mae(
            embedding_dim=32,
            epochs=20
        )
    )
