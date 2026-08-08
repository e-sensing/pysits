Self-supervised VICReg pre-training with time-warping augmentation

Self-supervised pre-training using the VICReg (Variance-Invariance-Covariance
Regularization) loss and a torch encoder. Two views of each sample are created
on-the-fly using the resampling augmentation of Saget et al. (2025): the time
series is upsampled, two disjoint subsequences are drawn with a temporal
coverage constraint, and each is resampled back to the original length. No
labels are required.
Both views are passed through a shared encoder and projector. The VICReg loss
combines three objectives:
1. Invariance: MSE between the projected representations of the two views 

ce loss combines three objectives:
1. Invariance: MSE between the projected representations of the two views 
   pulls paired embeddings together.
2. Variance: a hinge loss that keeps the standard deviation of each embedding
   feature above a threshold of 1 across the batch 
   prevents informational collapse.
3. Covariance: penalizes off-diagonal entries of the embedding covariance
   matrix 
   decorrelates features.
The function can be used in two ways:
- If `samples` is provided, it trains immediately and returns an encoder-ready
  model object (see Returns).
- If `samples` is `None`, it returns a training function that can be passed to
  `sits_pre_train` or called later.

The augmentation strategy creates two views of each sample using the resampling
method of Saget et al. (2025). The original time series (length `T`) is
upsampled to `2T` timesteps by linear interpolation. Two disjoint subsequences
of `T/2` timesteps are drawn from the upsampled series, with a constraint that
at least `floor((T/2)/4)` timesteps fall in each temporal quarter. Each
subsequence is then resampled back to `T` positions by rescaling its timestamps
and interpolating, producing two views that preserve overall temporal structure
while differing in fine-grained detail. Because the subsampling is random,
views differ at every epoch.

Args:
    samples (SITSTimeSeriesModel): Samples object. If `None` (default),
        returns a training function. If provided, triggers immediate
        training. Base data samples are not supported.
    embedding_dim (int): Dimensionality of the encoder embedding (exported
        features). Default: 64.
    proj_dim (int): Dimensionality of the projector head used only during
        pre-training. Default: 128.
    sim_coeff (float): Weight of the invariance (MSE) term in the VICReg
        loss. Default: 25.0.
    std_coeff (float): Weight of the variance (hinge) term in the VICReg
        loss. Default: 25.0.
    cov_coeff (float): Weight of the covariance (off-diagonal) term in the
        VICReg loss. Default: 1.0.
    encoder_model (SITSMachineLearningMethod): Deep learning method that
        takes time series as input and produces latent representations that
        are used to compute the loss function (suggested options:
        `sits_tempcnn()`, `sits_lighttae()`, `sits_resnet()`). Default:
        `sits_tempcnn()`.
    epochs (int): Maximum number of training epochs.
    batch_size (int): Batch size for training. Default: 128.
    validation_split (float): Fraction of samples held out for validation
        loss monitoring, in (0, 1).
    optimizer: A `torch` optimizer constructor (default:
        `torch::optim_adamw`).
    opt_hparams (dict): Optimizer hyperparameters. Common entries: `lr`,
        `eps`, `weight_decay`.
    lr_decay_epochs (int): Step size (in epochs) for LR decay.
    lr_decay_rate (float): Multiplicative LR decay factor.
    patience (int): Early-stopping patience (epochs without improvement).
    min_delta (float): Minimum improvement required to reset the patience
        counter.
    verbose (bool): Print training progress?
    seed (int): Random seed for reproducibility.

Returns:
    R: If `samples` is `None`, a training function that trains a VICReg model
    and returns a pretrained encoder. If `samples` is provided, the result of
    applying the training function to `samples` directly.

Examples:
    from pysits import *

    model = sits_pre_train(
        samples_modis_ndvi,
        sits_ssl_vicreg(
            embedding_dim=32,
            epochs=20
        )
    )
