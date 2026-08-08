Supervised contrastive learning for time series

Supervised contrastive (SupCon) pre-training of encoders, based on the
loss proposed by Khosla et al. (2020). The method learns an embedding space in
which time-series samples sharing the same label are pulled together while
samples with different labels are pushed apart.
For each batch, two views per sample are created by pairing every anchor with a
same-class sample. Both views are passed through a shared encoder and
projection head and are L2-normalized. The resulting `2B` embeddings are pooled
and each embedding is contrasted against every other embedding (excluding
itself) using temperature-scaled cosine similarity, with positives defined by
matching labels.
After pre-training, the projection head is discarded and only the encoder is
kept for downstream use via `sits_encode`.
The function can be used in two ways:
- If `samples` is provided, it trains immediately and returns an encoder-ready
  model object (see Returns).
- If `samples = None`, it returns a training function with signature
  `function(samples)` that can be passed to `sits_pre_train` or called later.

The supervised contrastive (SupCon) loss generalizes the InfoNCE/NT-Xent
objective by allowing multiple positives per anchor. For each of the `2B`
L2-normalized embeddings in a batch, all other embeddings that share the
anchor's label act as positives and the remaining embeddings act as negatives.
Pairwise cosine similarities are divided by the temperature `scaling` and
combined in a log-softmax form; the loss is averaged over the positives of each
anchor and then over the batch.
The `scaling` parameter (temperature) controls the sharpness of the similarity
distribution. Lower temperatures sharpen it and place more weight on the
hardest negatives, encouraging stronger separation at the cost of noisier
gradients; higher temperatures soften it. The default of `0.07` follows Khosla
et al. (2020). Larger batches also help, since they expose more positives and
negatives per anchor and yield a stronger contrastive signal.

Args:
    samples (SITSTimeSeriesModel | None): Sample time series. If `None`
        (default), returns a training function. If provided, triggers
        immediate training. Base data samples (e.g., `sits_base`) are not
        supported.
    embedding_dim (int): Dimensionality of the encoder embedding (exported
        features). Default: 64.
    proj_dim (int): Dimensionality of the projection head output used only
        during pre-training (discarded afterwards). Default: 128.
    scaling (float): Scaling for the contrastive loss. Lower values sharpen
        the similarity distribution. Default: 0.07.
    num_pairs (int | None): Total number of pairs to form. When `None`
        (default), one pair is formed per sample.
    encoder_model (SITSMachineLearningMethod): Deep learning method that takes
        time series as input and produces latent representations that are used
        to compute the loss function (suggested options: `sits_tempcnn()`,
        `sits_lighttae()`, `sits_resnet()`). Default: `sits_tempcnn()`.
    epochs (int): Maximum number of training epochs.
    batch_size (int): Batch size for training. Larger batches provide more
        positives/negatives per sample. Default: 128.
    validation_split (float): Fraction of samples in (0, 1) held out for
        validation loss monitoring.
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
    R: If `samples = None`, a training function with signature
    `function(samples)` that trains a supervised contrastive model and returns
    a pretrained encoder. If `samples` is provided, the result of applying the
    training function to `samples` directly.

Examples:
    from pysits import *

    model = sits_pre_train(
        samples_modis_ndvi,
        sits_contrastive_learning(
            embedding_dim=32,
            epochs=20
        )
    )
