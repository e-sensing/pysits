Self-supervised LeJEPA pre-training with resampling augmentation

Self-supervised pre-training using the LeJEPA (Lean Joint-Embedding Predictive
Architecture) loss and a torch encoder. Two views of each sample are created
on-the-fly using the resampling augmentation of Saget et al. (2025). No labels
are required.
The LeJEPA loss combines two terms:
1. Invariance: MSE between each view's projected embedding and the mean across
   views \u2014 pulls views together.
2. SIGReg (Sketched Isotropic Gaussian Regularization): constrains embeddings
   to an isotropic Gaussian distribution by comparing 1-D projections to the
   Gaussian characteristic function \u2014 prevents representational collapse
   without teacher-student networks or stop-gradients.
These two terms are balanced by a single hyperparameter `lambda`.
The function can be used in two ways:
- If `samples` is provided, it trains immediately and returns an encoder-ready
  model object (see Value).
- If `samples = None`, it returns a training function with signature
  `function(samples)` that can be passed to `sits_pre_train` or called later.

The augmentation strategy uses the resampling method of Saget et al. (2025):
the time series is upsampled, two disjoint subsequences are drawn with a
temporal coverage constraint, and each is resampled back to the original
length.
Unlike VICReg (which uses three separate regularization terms), LeJEPA replaces
all collapse-prevention heuristics with the single SIGReg objective, yielding a
simpler and more theoretically grounded method with a single trade-off
hyperparameter.

Args:
    samples (SITSTimeSeriesModel): samples object. If `None` (default),
        returns a training function. If provided, triggers immediate
        training.
    embedding_dim (int): Dimensionality of the encoder embedding. Default:
        64.
    proj_dim (int): Dimensionality of the projector head used only during
        pre-training. Default: 128.
    lambda (float): Trade-off in (0, 1) between invariance (`1 - lambda`)
        and SIGReg (`lambda`). Default: 0.02.
    num_knots (int): Number of quadrature knots for the SIGReg
        characteristic function test. Default: 17.
    num_slices (int): Number of random projection directions for SIGReg.
        Default: 256.
    encoder_model (SITSMachineLearningMethod): Deep learning method that
        takes time series as input and produces latent representations that
        are used to compute the loss function (suggested options:
        `sits_tempcnn()`, `sits_lighttae()`, `sits_resnet()`). Default:
        `sits_tempcnn()`.
    epochs (int): Maximum number of training epochs.
    batch_size (int): Batch size for training. Default: 512.
    validation_split (float): Fraction in (0, 1) of samples held out for
        validation loss monitoring.
    optimizer: A `torch` optimizer constructor (default:
        `torch::optim_adamw`).
    opt_hparams (dict): Optimizer hyperparameters.
    lr_decay_epochs (int): Step size (in epochs) for LR decay.
    lr_decay_rate (float): Multiplicative LR decay factor.
    patience (int): Early-stopping patience.
    min_delta (float): Minimum improvement for early stopping.
    verbose (bool): Print training progress?
    seed (int): Random seed for reproducibility.

Returns:
    R: If `samples = None`, a training function. If `samples` is provided, a
        pretrained encoder closure.

Examples:
    from pysits import *

    model = sits_pre_train(
        samples_modis_ndvi,
        sits_ssl_lejepa(
            embedding_dim=32,
            epochs=20
        )
    )
