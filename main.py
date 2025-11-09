import numpy as np
import matplotlib.pyplot as plt

def plot_object(x, title):
    plt.figure(figsize=(5, 5))
    plt.plot(x[0, :], x[1, :], 'b-o', markersize=4)
    plt.plot(0, 0, 'ro', markersize=8)
    plt.title(title)
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def stretch(x, a, b):
    x_copy = x.copy()
    stretch_array = np.array([[a, 0], [0, b]])
    x_modified = stretch_array @ x_copy
    return x_modified, stretch_array

def shear(x, a, b):
    x_copy = x.copy()
    shear_array = np.array([[1, a], [b, 1]])
    x_modified = shear_array @ x_copy
    return x_modified, shear_array

def reflection(x, a, b):
    x_copy = x.copy()

    denominator = a**2 + b**2
    if denominator == 0:
        print("error")
        return x_copy

    reflection_array = (1 / denominator) * np.array([
        [a**2 - b**2, 2 * a * b],
        [2 * a * b, b**2 - a**2]
    ])

    x_modified = reflection_array @ x_copy

    return x_modified, reflection_array

def rotation(x, o):
    x_copy = x.copy()

    cos_o = np.cos(o)
    sin_o = np.sin(o)

    rotation_array = np.array([
        [cos_o, -sin_o],
        [sin_o, cos_o]
    ])
    x_modified = rotation_array @ x_copy
    return x_modified, rotation_array

X_points = [
    [0, 3], [0.5, 1.5], [1.5, 2],
    [1, 0.5], [2, 0], [1.2, -1],
    [2, -2], [0.5, -1.5], [0, -3],
    [-0.5, -1.5], [-2, -2], [-1.2, -1],
    [-2, 0], [-1, 0.5], [-1.5, 2],
    [-0.5, 1.5], [0, 3], [-3, 3],
    [-3.5, 2], [-3, 1], [-2.5, 2],
    [-3, 3]
]
X_t = np.array(X_points).T

X_stretched, stretch_array = stretch(X_t, 0.5, 2)
X_sheared, shear_array = shear(X_t, 0,0.5)
X_reflected, reflection_array = reflection(X_t, 0.5,0.5)
X_rotated, rotation_array = rotation(X_t, np.deg2rad(45))

plot_object(X_t, "initial star")
plot_object(X_stretched, "stretched star")
print(f"the matrix that was used (stretch): {stretch_array}")
plot_object(X_sheared, "sheared star")
print(f"the matrix that was used (shear): {shear_array}")
plot_object(X_reflected, "reflected star")
print(f"the matrix that was used (reflection): {reflection_array}")
plot_object(X_rotated, "rotated star")
print(f"the matrix that was used (rotation): {rotation_array}")