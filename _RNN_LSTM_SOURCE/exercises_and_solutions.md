# Student Exercises and Worked Solutions

## 1. Tensor interpretation (5 minutes)

**Prompt:** For 120 customer sequences, 10 days and 4 feature channels, state the input tensor shape and scalar target shape. Explain the meaning of the second axis.

**Solution:** X has shape (120,10,4); y for one numeric target per customer has shape (120,1) or (120,). The second dimension is time, not the number of variables.

## 2. Scalar RNN forward pass (8 minutes)

**Prompt:** Calculate h1,h2 for h0=0, x1=1, x2=0, Wxh=0.5, Whh=0.4, b=0.

**Solution:** h1=tanh(0.5)=0.462117; h2=tanh(0.4×0.462117)=tanh(0.184847)≈0.18277. Only one set of weights is used at both timesteps.

## 3. Vector RNN step (8 minutes)

**Prompt:** For x=(1,2)^T, hprev=(0.1,-0.1)^T, Wxh=[[0.2,0.1],[-0.1,0.3]], Whh=diag(0.5,0.5), zero bias, find hnew.

**Solution:** Wxh x=(0.4,0.5); Whh hprev=(0.05,-0.05); preactivation=(0.45,0.45); hnew=tanh componentwise≈(0.421899,0.421899).

## 4. Jacobian products and gradient size (8 minutes)

**Prompt:** Compare products of 20 factors each 0.75 or 1.15. How would this change your expectations of gradients passing through 20 recurrent steps?

**Solution:** 0.75^20≈0.00317 and 1.15^20≈16.37. Real BPTT uses matrices and varying activation derivatives, so these values illustrate possible shrinking/growth but are not measured RNN gradients.

## 5. Global norm clipping (5 minutes)

**Prompt:** The gradient is (3,4), clipping threshold 1. Find the clipped gradient.

**Solution:** Norm=5. Scale by 1/5: (0.6,0.8). Norm becomes 1; direction preserved.

## 6. LSTM arithmetic (10 minutes)

**Prompt:** Given cprev=0.4, f=0.8, i=0.5, candidate=0.6, o=0.7, calculate c and h.

**Solution:** c=0.8×0.4+0.5×0.6=0.62; h=0.7×tanh(0.62)≈0.3858.

## 7. Gate counterfactuals (10 minutes)

**Prompt:** Set cprev=0.7 and candidate=-0.2. Compare (f,i)=(1,0), (0,1), and (0.8,0.5).

**Solution:** c values are 0.7, -0.2, and 0.46 respectively. Output gate o controls how much tanh(c) becomes visible in h; it does not directly reset c.

## 8. Detect leakage (10 minutes)

**Prompt:** A researcher standardizes all 500 time observations using full-sample mean and standard deviation, then creates overlapping windows and randomizes them into train/test. Identify two problems and repair them.

**Solution:** Full-sample scaling accesses future test distribution; use training-only statistics. Randomly split overlapping windows can place near-duplicates across partitions; split by target time with latest observations as test. Verify target index is strictly after the last permitted input.

## 9. Fair model selection (10 minutes)

**Prompt:** The test RMSEs are naive=0.24, RNN=0.22, LSTM=0.26. Which is best on this test segment, and what additional evidence is required for a scientific ranking?

**Solution:** RNN has lowest RMSE on that segment, but single-seed single-period differences are insufficient for universal claims. Repeat seeds, consider multiple forecast origins, compare tuning budgets, quantify variability and test stronger baselines.

## 10. Capstone group assignment (20 minutes)

**Prompt:** Design a one-step electricity-demand forecast using 24 historical hourly steps and optionally known temperature information. Specify target, input shape, chronological evaluation, baselines, model candidates, metric and leakage checks.

**Solution sketch:** X shape (N,24,F) with F matching observed-at-origin features. Fit normalization on training only. Use persistence and seasonal naive, then a lagged regression, RNN and LSTM. Choose hyperparameters through rolling validation and preserve a final holdout test. Report RMSE and MAE in original units, compute per-period errors, compare multiple seeds and assess forecast availability of exogenous covariates.
