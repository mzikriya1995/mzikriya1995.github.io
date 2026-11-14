# Instructor Guide — RNNs and LSTMs, Extended Graduate Lecture

## Audience and teaching position

Graduate students with introductory statistics or mathematics, but no prior study of recurrent neural networks. Explain each symbol before using matrix notation. Sequence learning is presented as a modeling decision subject to empirical validation, not a guaranteed improvement over simpler models.

## Suggested pacing

The source contains the full original 60-slide lecture plus the extended slides. Notes in the source provide a suggested duration and detailed teaching script on **every slide**. The full extended plan deliberately exceeds four hours to accommodate live questions and demonstrations. For a strict four-hour session, treat long mathematical worked exercises and the capstone discussion as selected optional segments.

| Lecture block | Topics | Suggested time |
|---|---|---:|
| Intro and sequence literacy | What is ordered data? Targets, features, tensors, masks | 35–45 min |
| Vanilla RNN | Hidden state, recurrence, shape and parameter count, supervised outputs | 40–50 min |
| BPTT and optimization | Jacobian chains, saturation, clipping, truncated BPTT | 40–50 min |
| LSTM mechanics | All gates, cell/hidden states, mathematics, numeric exercises | 55–70 min |
| Implementation and evaluation | R/Keras3, Python/PyTorch, splits, leakage, baselines, errors | 55–70 min |
| Applications and capstone | NLP, anomaly scores, GRUs, model selection and research design | 30–45 min |

The exact maximum note timings sum to about **307 minutes**; any four-hour delivery should select the shorter path in the ranges above. A break may be scheduled between the gradient and LSTM blocks.

## Recommended opening narrative

Ask whether shuffling a sentence preserves meaning. Demonstrate the contrast with a tabular regression row whose ordering is irrelevant to the task. Introduce a sequence as ordered feature vectors rather than independent observations. Contrast a lagged feedforward model with a recurrent hidden state. Write `h_t = tanh(W_x x_t + W_h h_{t-1} + b)` and identify each object before discussing why the weights are shared.

## Mathematical teaching checkpoints

**Checkpoint 1 — Shape discipline.** Ask students to represent 32 windows of 24 hours and three signals as (32,24,3). Discuss why targets have shape (32,1) for scalar next-step prediction. A label sequence would have a different target structure.

**Checkpoint 2 — Scalar RNN forward pass.** Set h0=0, x1=1, x2=0, Wxh=0.5, Whh=0.4, b=0. Obtain h1≈0.4621 and h2≈0.1828. Check the application of tanh after addition.

**Checkpoint 3 — Three-step BPTT.** For a scalar recurrence, derive ∂h_t/∂h_(t−1) = w(1−h_t²), then multiply two or more local derivatives. Explain that vector models require matrix Jacobian products. Use the gradient-product plot only as an illustration.

**Checkpoint 4 — LSTM update.** Define f,i,o, candidate c̃ and both c_t and h_t. With previous cell 0.4, f=0.8, i=0.5, candidate=0.6, o=0.7, obtain c_t=0.62 and h_t≈0.3858. Explain that gate values in the exercise are supplied, not inferred from pretrained parameters.

**Checkpoint 5 — Leakage-free evaluation.** Fit scaling statistics to the training observations only; split by target time rather than random overlapping windows. Make the naive forecast predict the previous observed target. Evaluate in original units. Discuss why a later test segment must remain untouched by hyperparameter selection.

**Checkpoint 6 — Scientific reasoning.** Show that models with more parameters can lose against a simple baseline. Do not claim an LSTM always outperforms an RNN. Discuss differences between architecture comparisons made across software frameworks and across seeds.

## Notes, fragments and slide controls

- Speaker notes: press **S** while displaying RevealJS slides.
- Use **right arrow** to progress through fragments and slides.
- Use **Esc** for an overview of the deck.
- Press **B** to black out the screen during a board calculation where supported by RevealJS.
- During the 4+ hour session, reduce slide pace deliberately and prioritize working calculations aloud rather than only reading slide text.

## Figure labeling and scientific accuracy

Every non-data scientific figure should be introduced as an illustration. The PyTorch prediction chart and residual plot refer to the packaged synthetic-data demonstration; they are not benchmark evidence for a real application. Do not infer causality from gates or state trajectories.

## Software requirements

Quarto is needed to render. R Keras3 / TensorFlow is only needed to execute R training; Python with torch, numpy and pandas is only needed to execute PyTorch training. Scripts are independent of the render to avoid environment-related slide failures.
