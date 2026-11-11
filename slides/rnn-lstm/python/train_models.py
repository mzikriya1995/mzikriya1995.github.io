"""Graduate RNN/LSTM lecture: reproducible PyTorch forecasting demo.

Run from any directory with: python path/to/train_models.py
Uses the shared CSV and chronological splits. No future observations enter
training scaler estimates; validation/test windows may use historical inputs.
"""
from __future__ import annotations
from pathlib import Path
import copy
import json
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader

PROJECT = Path(__file__).resolve().parents[1]
LOOKBACK = 24
TRAIN_END, VALID_END = 300, 400  # first 300 observations train
SEED = 42

class SequenceRegressor(nn.Module):
    def __init__(self, cell: str) -> None:
        super().__init__()
        if cell == 'rnn':
            self.core = nn.RNN(1, 16, batch_first=True, nonlinearity='tanh')
        elif cell == 'lstm':
            self.core = nn.LSTM(1, 16, batch_first=True)
        else:
            raise ValueError('cell must be rnn or lstm')
        self.head = nn.Linear(16, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # output: (batch, lookback, hidden_size); take the last timestep
        sequence_states, _ = self.core(x)
        return self.head(sequence_states[:, -1, :])

def prepare_data():
    original = pd.read_csv(PROJECT / 'data' / 'synthetic_series.csv')['value'].to_numpy(dtype='float64')
    mu, sd = original[:TRAIN_END].mean(), original[:TRAIN_END].std()
    scaled = (original - mu) / sd
    target_indices = np.arange(LOOKBACK, len(original))
    windows = np.stack([scaled[i-LOOKBACK:i] for i in target_indices]).astype('float32')[:, :, None]
    targets = scaled[LOOKBACK:].astype('float32')[:, None]
    train = target_indices < TRAIN_END
    valid = (target_indices >= TRAIN_END) & (target_indices < VALID_END)
    test = target_indices >= VALID_END
    return original, mu, sd, windows, targets, train, valid, test

def main():
    torch.set_num_threads(1)
    original, mu, sd, windows, targets, train, valid, test = prepare_data()
    xtr, ytr = map(torch.from_numpy, (windows[train], targets[train]))
    xva, yva = map(torch.from_numpy, (windows[valid], targets[valid]))
    xte = torch.from_numpy(windows[test])
    results = {}
    forecast = pd.DataFrame({'t': np.arange(VALID_END, len(original)), 'actual': original[VALID_END:]})
    forecast['naive'] = windows[test, -1, 0] * sd + mu
    results['naive'] = float(np.sqrt(np.mean((forecast.naive - forecast.actual)**2)))
    output = PROJECT / 'outputs'
    output.mkdir(exist_ok=True)
    for cell in ('rnn', 'lstm'):
        torch.manual_seed(SEED)
        model = SequenceRegressor(cell)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
        loss_fn = nn.MSELoss()
        generator = torch.Generator().manual_seed(SEED)
        batches = DataLoader(TensorDataset(xtr, ytr), batch_size=32, shuffle=True, generator=generator)
        best_val, best_state, best_epoch = float('inf'), None, 0
        history = []
        for epoch in range(1, 36):
            model.train()
            total = 0.0
            for xb, yb in batches:
                optimizer.zero_grad()
                loss = loss_fn(model(xb), yb)
                loss.backward()
                nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()
                total += loss.item() * len(xb)
            model.eval()
            with torch.no_grad():
                validation_loss = float(loss_fn(model(xva), yva))
            train_loss = total / len(xtr)
            history.append({'epoch': epoch, 'train_mse': train_loss, 'val_mse': validation_loss})
            if validation_loss < best_val:
                best_val, best_epoch = validation_loss, epoch
                best_state = copy.deepcopy(model.state_dict())
            if epoch - best_epoch >= 7:
                break
        model.load_state_dict(best_state)
        model.eval()
        with torch.no_grad():
            prediction = model(xte).numpy().ravel() * sd + mu
        forecast[cell] = prediction
        results[cell] = float(np.sqrt(np.mean((prediction - forecast.actual)**2)))
        pd.DataFrame(history).to_csv(output / f'{cell}_history.csv', index=False)
        torch.save(model.state_dict(), output / f'{cell}_weights.pt')
    forecast.to_csv(output / 'pytorch_predictions.csv', index=False)
    (output / 'metrics.json').write_text(json.dumps(results, indent=2))
    print('One-step-ahead test RMSE in original data units:')
    for name, rmse in results.items():
        print(f'  {name:>5s}: {rmse:.4f}')
    print('The lowest observed RMSE wins; performance is data and seed dependent.')
    print(f'Files written to {output}')

if __name__ == '__main__':
    main()
