# import random
# import math

# # ---- ACTIVATION FUNCTIONS ----

# def sigmoid(x):
#     return 1 / (1 + math.exp(-x))

# def sigmoid_derivative(x):
#     return x * (1 - x)

# def relu(x):
#     return max(0, x)

# def relu_derivative(x):
#     return 1 if x > 0 else 0


# # ---- MATRIX OPERATIONS ----

# def dot(a, b):
#     result = []
#     for i in range(len(a)):
#         row = []
#         for j in range(len(b[0])):
#             s = 0
#             for k in range(len(b)):
#                 s += a[i][k] * b[k][j]
#             row.append(s)
#         result.append(row)
#     return result

# def transpose(matrix):
#     return list(map(list, zip(*matrix)))

# def apply_function(matrix, func):
#     return [[func(x) for x in row] for row in matrix]

# def subtract(a, b):
#     return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

# def add(a, b):
#     return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

# def scalar_multiply(matrix, scalar):
#     return [[x * scalar for x in row] for row in matrix]

# def multiply(a, b):
#     return [[a[i][j] * b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


# # ---- DATA ----

# X = [
#     [0,0,1],
#     [1,1,1],
#     [1,0,1],
#     [0,1,1]
# ]

# y = [
#     [0],
#     [1],
#     [1],
#     [0]
# ]

# random.seed(1)

# def random_matrix(rows, cols):
#     return [[2 * random.random() - 1 for _ in range(cols)] for _ in range(rows)]

# weights_input_hidden = random_matrix(3, 4)
# weights_hidden_output = random_matrix(4, 1)

# learning_rate = 0.1

# output_layer = []

# # ---- CHOOSE ACTIVATION ----
# activation = "sigmoid"   # change to "sigmoid" if you want

# act = None
# act_deriv = None

# if activation == "sigmoid":
#     act = sigmoid
#     act_deriv = sigmoid_derivative
# elif activation == "relu":
#     act = relu
#     act_deriv = relu_derivative


# # ---- TRAINING ----

# for _ in range(10000):

#     # Forward
#     hidden_raw = dot(X, weights_input_hidden)
#     hidden_layer = apply_function(hidden_raw, act)

#     output_raw = dot(hidden_layer, weights_hidden_output)
#     output_layer = apply_function(output_raw, sigmoid)  
#     # keep sigmoid in output (important for 0–1 output)

#     # Error
#     error = subtract(y, output_layer)

#     # Backprop
#     d_output = multiply(error, apply_function(output_layer, sigmoid_derivative))

#     error_hidden = dot(d_output, transpose(weights_hidden_output))
#     d_hidden = multiply(error_hidden, apply_function(hidden_layer, act_deriv))

#     # Update
#     weights_hidden_output = add(
#         weights_hidden_output,
#         scalar_multiply(dot(transpose(hidden_layer), d_output), learning_rate)
#     )

#     weights_input_hidden = add(
#         weights_input_hidden,
#         scalar_multiply(dot(transpose(X), d_hidden), learning_rate)
#     )

# # Result
# print("Output after training:")
# for row in output_layer:
#     print(row)

import random
import math
import matplotlib.pyplot as plt

# --- Activations ---
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

def relu(x):
    return max(0, x)

def relu_derivative(x):
    return 1 if x > 0 else 0

# --- Matrix helpers ---
def dot(a, b):
    assert len(a[0]) == len(b), f"Shape mismatch: {shape(a)} · {shape(b)}"
    
    result = []
    for i in range(len(a)):
        row = []
        for j in range(len(b[0])):
            s = 0
            for k in range(len(b)):
                s += a[i][k] * b[k][j]
            row.append(s)
        result.append(row)
    return result

def transpose(m):
    return list(map(list, zip(*m)))

def apply(m, f):
    return [[f(x) for x in row] for row in m]

def add(a, b):
    assert len(a[0]) == len(b[0]), f"Column mismatch: {shape(a)} vs {shape(b)}"
    
    result = []
    for i in range(len(a)):
        row = []
        for j in range(len(a[0])):
            b_i = 0 if len(b) == 1 else i
            row.append(a[i][j] + b[b_i][j])
        result.append(row)
    
    return result

def subtract(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def multiply(a, b):
    return [[a[i][j] * b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def scalar(m, s):
    return [[x * s for x in row] for row in m]

def shape(m):
    return (len(m), len(m[0]) if isinstance(m[0], list) else 1)

def debug_matrix(name, m, preview=2):
    print(f"\n{name}:")
    print("Shape:", shape(m))
    
    # show first few rows
    for i in range(min(preview, len(m))):
        print(m[i])

# --- Data ---
X = [
 [0,0,1],
 [1,1,1],
 [1,0,1],
 [0,1,1]
]

y = [
 [0],
 [1],
 [1],
 [0]
]

# --- Init ---
random.seed(1)

def rand(r,c):
    return [[2*random.random()-1 for _ in range(c)] for _ in range(r)]

w1 = rand(3,4)
w2 = rand(4,1)

b1 = [[0,0,0,0]]
b2 = [[0]]

lr = 0.1

print("X shape:", shape(X))
print("w1 shape:", shape(w1))
print("b1 shape:", shape(b1))
print("w2 shape:", shape(w2))
print("b2 shape:", shape(b2))

# --- Setup plot ---
plt.ion()  # interactive mode ON
fig, ax = plt.subplots()
losses = []

# --- Training with live animation ---
for epoch in range(2000):

    # Forward
    h = apply(add(dot(X, w1), b1), relu)
    o = apply(add(dot(h, w2), b2), sigmoid)

    # Loss (MSE)
    loss = sum((y[i][0] - o[i][0])**2 for i in range(len(y))) / len(y)
    losses.append(loss)

    # Backprop
    error = subtract(y, o)
    d_o = multiply(error, apply(o, sigmoid_derivative))

    h_error = dot(d_o, transpose(w2))
    d_h = multiply(h_error, apply(h, relu_derivative))

    # Update weights
    w2 = add(w2, scalar(dot(transpose(h), d_o), lr))
    w1 = add(w1, scalar(dot(transpose(X), d_h), lr))

    # Update bias
    b2 = add(b2, scalar(d_o, lr))
    b1 = add(b1, scalar(d_h, lr))

    # --- Animate every few steps ---
    if epoch % 20 == 0:
        ax.clear()
        ax.plot(losses, color='blue')
        ax.set_title(f"Training Loss (Epoch {epoch})")
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Loss")
        plt.pause(0.01)
    
    if epoch % 500 == 0:
        print("\n===== DEBUG SNAPSHOT =====")
        print("Epoch:", epoch)
        
        debug_matrix("X", X)
        debug_matrix("w1", w1)
        debug_matrix("b1", b1)
        
        h_raw = add(dot(X, w1), b1)
        debug_matrix("Hidden Raw", h_raw)
        
        h = apply(h_raw, relu)
        debug_matrix("Hidden Activated", h)
        
        o_raw = add(dot(h, w2), b2)
        debug_matrix("Output Raw", o_raw)
        
        o = apply(o_raw, sigmoid)
        debug_matrix("Output", o)

plt.ioff()
plt.show()