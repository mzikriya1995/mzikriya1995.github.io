# Graduate RNN/LSTM lecture: R implementation using Keras3 / TensorFlow.
# Run from the project root: Rscript R/train_models.R
# Install once (interactive R):
# install.packages(c("keras3", "tensorflow", "reticulate"))
# keras3::install_keras(backend = "tensorflow")

Sys.setenv(KERAS_BACKEND = "tensorflow")
suppressPackageStartupMessages(library(keras3))
set.seed(42)
try(tensorflow::tf$random$set_seed(42L), silent = TRUE)

# When run from inside the source folder or from any working directory, find data.
args <- commandArgs(trailingOnly = TRUE)
project <- if (length(args) > 0) args[[1]] else "."
if (!file.exists(file.path(project, "data", "synthetic_series.csv"))) {
  stop("Run from quarto-source (or pass its absolute path as the first argument).")
}
y_orig <- read.csv(file.path(project, "data", "synthetic_series.csv"))$value
stopifnot(length(y_orig) == 500L)
lookback <- 24L
train_end <- 300L
val_end <- 400L
# Compute training-only normalization: R's sd uses n-1; use population SD to match Python.
mu <- mean(y_orig[1:train_end])
sigma <- sqrt(mean((y_orig[1:train_end] - mu)^2))
y_scaled <- (y_orig - mu) / sigma

# X[i, t, f] has [sample, timestep, feature] ordering.
n_windows <- length(y_scaled) - lookback
X <- array(0, dim = c(n_windows, lookback, 1L))
Y <- matrix(0, n_windows, 1L)
target_index <- integer(n_windows)
for (i in seq_len(n_windows)) {
  X[i, , 1] <- y_scaled[i:(i + lookback - 1L)]
  Y[i, 1] <- y_scaled[i + lookback]
  target_index[i] <- i + lookback
}
train <- which(target_index <= train_end)
valid <- which(target_index > train_end & target_index <= val_end)
test <- which(target_index > val_end)

build_model <- function(cell = c("rnn", "lstm")) {
  cell <- match.arg(cell)
  model <- keras_model_sequential()
  if (cell == "rnn") {
    model |> layer_simple_rnn(units = 16L, activation = "tanh",
                              input_shape = c(lookback, 1L)) -> model
  } else {
    model |> layer_lstm(units = 16L, input_shape = c(lookback, 1L)) -> model
  }
  model <- model |> layer_dense(units = 1L)
  model |> compile(optimizer = optimizer_adam(learning_rate = 0.01), loss = "mse")
  model
}

outdir <- file.path(project, "outputs")
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
actual <- y_orig[target_index[test]]
naive <- X[test, lookback, 1] * sigma + mu
rmse <- function(p, a) sqrt(mean((as.numeric(p) - as.numeric(a))^2))
metrics <- data.frame(model = "naive", test_rmse = rmse(naive, actual))
preds <- data.frame(t = target_index[test] - 1L,
                    actual = actual, naive = as.numeric(naive))
for (cell in c("rnn", "lstm")) {
  model <- build_model(cell)
  model |> fit(
    x = X[train, , , drop = FALSE], y = Y[train, , drop = FALSE],
    validation_data = list(X[valid, , , drop = FALSE], Y[valid, , drop = FALSE]),
    epochs = 35L, batch_size = 32L, verbose = 2L,
    callbacks = list(callback_early_stopping(
      monitor = "val_loss", patience = 7L, restore_best_weights = TRUE
    ))
  ) -> training_history
  pred <- as.numeric(predict(model, X[test, , , drop = FALSE], verbose = 0L)) * sigma + mu
  preds[[cell]] <- pred
  metrics <- rbind(metrics, data.frame(model = cell, test_rmse = rmse(pred, actual)))
  write.csv(data.frame(epoch = seq_along(training_history$metrics$loss),
                       train_mse = unlist(training_history$metrics$loss),
                       val_mse = unlist(training_history$metrics$val_loss)),
            file.path(outdir, paste0("r_", cell, "_history.csv")), row.names = FALSE)
}
write.csv(preds, file.path(outdir, "r_predictions.csv"), row.names = FALSE)
write.csv(metrics, file.path(outdir, "r_metrics.csv"), row.names = FALSE)
print(metrics)
cat("R and Python implementations share the dataset and split; fitted results may differ.\n")
