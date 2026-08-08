Barlow Twins encoder for image time series

Supervised pre-training using the Barlow Twins loss and a torch encoder. Two
time series with the same class label are passed through a shared encoder +
projector. The Barlow Twins loss makes the cross-correlation matrix of the two
views' embeddings close to the identity: the diagonal -> 1 (invariance) and the
off-diagonal -> 0 (redundancy reduction). No negatives are required.
The function can be used in two ways:
- If `samples` is provided, it trains immediately and returns an encoder-ready
  model object (see Returns).
- If `samples` is `None`, it returns a training function with signature
  `function(samples)` that can be passed to `sits_pre_train` or called later.

Args:
    samples (SITSTimeSeriesModel): Sample time series. If `None` (default),
        returns a training function. If provided, triggers immediate
        training. Base data samples (e.g., `sits_base`) are not supported.
    embedding_dim (int): Dimensionality of the encoder embedding (exported
        features). Default: 64.
    proj_dim (int): Dimensionality of the projector head used only during
        pre-training. Default: 256.
    bt_lambda (float): Weight of the redundancy-reduction (off-diagonal) term
        in the Barlow Twins loss. Default: 5e-3.
    num_pairs (int | None): Total number of pairs to form per epoch. When
        `None` (default), one pair is formed for every sample in the training
        split.
    encoder_model (SITSMachineLearningMethod): Deep learning method that takes
        time series as input and produces latent representations that are used
        to compute the loss function (suggested options: `sits_tempcnn()`,
        `sits_lighttae()`, `sits_resnet()`). Default: `sits_tempcnn()`.
    epochs (int): Maximum number of training epochs.
    batch_size (int): Batch size for training. Larger values improve the
        Barlow Twins cross-correlation estimate. Default: 128.
    validation_split (float): Fraction of samples held out for validation loss
        monitoring, in (0, 1).
    optimizer: A `torch` optimizer constructor (default:
        `torch::optim_adamw`).
    opt_hparams (dict): Optimizer hyperparameters. Common entries: `lr`,
        `eps`, `weight_decay`.
    lr_decay_epochs (int): Step size (in epochs) for LR decay.
    lr_decay_rate (float): Multiplicative LR decay factor.
    patience (int): Early-stopping patience (epochs without improvement).
    min_delta (float): Minimum improvement required to reset the patience
        counter.
    verbose (bool): Whether to print training progress.
    seed (int): Random seed for reproducibility.

Returns:
    R: If `samples` is `None`, a training function with signature
    `function(samples)` that trains a Barlow Twins model and returns a
    pretrained encoder. If `samples` is provided, the result of applying the
    training function to `samples` directly.

Examples:
    from pysits import *

    model = sits_pre_train(
        samples_modis_ndvi,
        sits_barlow_twins(
            embedding_dim=32,
            epochs=20
        )
    )
