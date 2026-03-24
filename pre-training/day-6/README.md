# Project Name

> One-line description of what this project does.

This project builds and trains a simple neural network that learns to map inputs to correct outputs by adjusting its weights through forward propagation and backpropagation

Input (3 values)
   ↓
Layer 1 (4 neurons, ReLU)
   ↓
Layer 2 (2 neurons, Sigmoid)
   ↓
Final Output (2 values)

---

## Explain forward propagation in your own words

Passing of data from input neuron to output neuron.

---

## What would need to happen for this network to actually learn something (Hint: what's missing?)

Network is missing a proper learning mechanism (learning rate + true gradient-based update logic).

## What does each weight represent?

Each weight controls how important an input is.

- If w1 is large → input x1 has strong influence
- If w2 is near 0 → input x2 barely matters
- If weight is negative → input suppresses output

## What does the bias do?

- Activate even when inputs are zero
- Move decision boundary left/right

## Sigmoid vs ReLU

### Sigmoid

- Smooth curve
- Good for probabilities
- Problem: vanishing gradients (slow learning)

### ReLU

- Fast and simple
- Turns negatives into 0
- Helps deep networks learn faster
