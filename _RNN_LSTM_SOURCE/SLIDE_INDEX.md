# Slide Index

1. Recurrent Neural Networks & LSTMs {.title-slide .nostretch}
2. Why does order matter?
3. Prediction challenge: what comes next?
4. Learning roadmap
5. Prerequisite diagnostic: what do we already know?
6. Four-hour teaching route and checkpoints
7. What is sequential data?
8. Three application families
9. Ordered sequences versus unordered samples
10. Formal notation for sequential learning
11. Causal forecasting and bidirectional encoding
12. Why not just a feedforward network?
13. Sequence-to-output patterns
14. Tensor shapes: the practical foundation
15. Variable-length sequences: padding and masking
16. Tensor shapes: a concrete mini-batch
17. The key idea: carry a hidden state
18. What is a vanilla RNN?
19. Inside a recurrent cell
20. Unrolling through time
21. RNN recurrence as a learned state machine
22. Vanilla RNN parameter count
23. RNN versus a fixed-window regression model
24. Hidden-state equation and dimensions
25. Worked example: two RNN steps
26. Activation saturation changes gradient flow
27. Vector-valued forward pass: dimension check
28. How an RNN produces an output
29. Why weight sharing matters
30. Application: short text sentiment
31. Many-to-one versus per-token sequence supervision
32. Activity: calculate the next state
33. RNN summary and its limitation
34. How does the network learn?
35. Backpropagation Through Time (BPTT)
36. BPTT computational graph over three steps
37. Deriving one recurrent gradient path
38. Why long-range gradients are difficult
39. Vanishing gradients: a toy illustration
40. Gradient products: decay versus explosion
41. Why small activation derivatives matter
42. Exploding gradients: instability
43. Training strategies and tradeoffs
44. Gradient clipping: mathematical rule
45. Truncated BPTT and state detachment
46. Think–pair–share: gradient directions
47. Why better memory is needed
48. From RNN to LSTM
49. The modern LSTM cell
50. Two states: $c_t$ versus $h_t$
51. LSTM history: original cell and later forget gate
52. What is a gate?
53. Forget gate: what to retain?
54. Input gate: what to write?
55. Candidate memory: what to propose?
56. Gate activations: interpretation by dimension
57. Controlled LSTM gate counterfactuals
58. Cell-state update: retain + write
59. Output gate: what to reveal?
60. Hidden-state calculation
61. Output-gate saturation and its derivative
62. What does gating cost in parameters?
63. All LSTM equations on one slide
64. Worked example: one complete LSTM step
65. Why LSTM can help gradients
66. Direct cell-state gradient versus full derivative
67. What LSTMs do not automatically solve
68. Activity: control the gates
69. Workshop: calculate an LSTM step
70. Practical case study: forecast one step
71. Chronological split and leakage
72. Leakage checklist for sequence experiments
73. Rolling-origin validation
74. Creating sliding windows
75. Always include a baseline
76. Fair forecasting baselines: a ladder
77. R implementation: vanilla RNN
78. R implementation: replace RNN with LSTM
79. Keras3 in R: tensor and output shapes
80. R: fit, validate, monitor
81. R: predict and assess test RMSE
82. Forecast residual diagnostics
83. PyTorch: model definitions
84. PyTorch: a training step
85. PyTorch tensor and return-value pitfalls
86. Observed PyTorch test predictions
87. Compare results and diagnose
88. Scientific uncertainty: repeat across seeds
89. Classification metrics for imbalanced sequence tasks
90. Application: sentiment classification
91. From tokens to an LSTM classifier
92. Application: multivariate anomaly detection
93. Calibrating anomaly-score thresholds
94. RNN vs LSTM vs GRU vs Transformer
95. GRU equations in brief
96. How should we choose?
97. Capstone: design a defensible sequence experiment
98. Five essential takeaways
99. Further reading and next steps
