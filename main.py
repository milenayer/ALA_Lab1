import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

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

def stretch_shear_rotation(x, stretch_params, shear_params, rotation_param):
    x_1, st = stretch(x, *stretch_params)
    x_2, sh = shear(x_1, *shear_params)
    x_final, ro = rotation(x_2, rotation_param)

    final_array = ro @ sh @ st

    return x_final, final_array

def shear_stretch_rotation(x, stretch_params, shear_params, rotation_param):
    x_1, sh = shear(x, *shear_params)
    x_2, st = stretch(x_1, *stretch_params)
    x_final, ro = rotation(x_2, rotation_param)

    final_array = ro @ st @ sh

    return x_final, final_array

def stretch_rotation_shear(x, stretch_params, shear_params, rotation_param):
    x_1, st = stretch(x, *stretch_params)
    x_2, ro = rotation(x_1, rotation_param)
    x_final, sh = shear(x_2, *shear_params)

    final_array = sh @ ro @ st

    return x_final, final_array

def main1():
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
    X_sheared, shear_array = shear(X_t, 0, 0.5)
    X_reflected, reflection_array = reflection(X_t, 0.5, 0.5)
    X_rotated, rotation_array = rotation(X_t, np.deg2rad(45))

    plot_object(X_t, "initial star")
    plot_object(X_stretched, "stretched star")
    print(f"the matrix that was used (stretch): {stretch_array}")
    plot_object(X_sheared, "sheared star")
    print(f"the matrix that was used (shear): {shear_array}")
    plot_object(X_reflected, "reflected star")
    print(f"the matrix that was used (reflection): {reflection_array}")
    plot_object(X_rotated, "rotated star")
    print(f"the matrix that was used (rotation):\n {rotation_array}")

    X_final_1, array_final_1 = stretch_shear_rotation(X_t, (0.5, 1.5), (0.4, 0), np.deg2rad(30))
    plot_object(X_final_1, "stretch -> shear -> rotation")
    print(f"the stretch -> shear -> rotation matrix: \n {array_final_1}")

    X_final_2, array_final_2 = shear_stretch_rotation(X_t, (0.5, 1.5), (0.4, 0), np.deg2rad(30))
    plot_object(X_final_2, "shear -> stretch -> rotation")
    print(f"the shear -> stretch -> rotation matrix:\n {array_final_2}")

    X_final_3, array_final_3 = stretch_rotation_shear(X_t, (0.5, 1.5), (0.4, 0), np.deg2rad(30))
    plot_object(X_final_3, "stretch -> rotation -> shear")
    print(f"the stretch -> rotation -> shear matrix:\n {array_final_3}")

def read_off(filename: str):
    with open(filename, 'r') as f:
        if 'OFF' != f.readline().strip():
            raise ValueError('Not a valid OFF header')
        n_verts, n_faces, _ = map(int, f.readline().strip().split())

        verts = [list(map(float, f.readline().strip().split())) for _ in range(n_verts)]

        faces = [list(map(int, f.readline().strip().split()[1:])) for _ in range(n_faces)]

        return np.array(verts), faces

def plot_off(vertices, faces, title="3D"):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    mesh = Poly3DCollection([vertices[face] for face in faces], alpha=0.3, edgecolor='k')
    ax.add_collection3d(mesh)

    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], s=2, c='r')

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ax.auto_scale_xyz(vertices[:, 0], vertices[:, 1], vertices[:, 2])
    plt.title(title)
    plt.show()

def rotate_xy(x, o):
    x_copy = x.copy()
    cos_t = np.cos(o)
    sin_t = np.sin(o)
    rotation_array = np.array([
        [cos_t, -sin_t, 0],
        [sin_t, cos_t, 0],
        [0, 0, 1]
    ])
    x_modified = rotation_array @ x_copy
    return x_modified, rotation_array

def rotate_yz(x, o):
    x_copy = x.copy()
    cos_t = np.cos(o)
    sin_t = np.sin(o)
    rotation_array = np.array([
        [1, 0, 0],
        [0, cos_t, -sin_t],
        [0, sin_t, cos_t]
    ])
    x_modified = rotation_array @ x_copy
    return x_modified, rotation_array

def rotate_xz(x, o):
    x_copy = x.copy()
    cos_t = np.cos(o)
    sin_t = np.sin(o)
    rotation_array = np.array([
        [cos_t, 0, -sin_t],
        [0, 1, 0],
        [sin_t, 0, cos_t]
    ])
    x_modified = rotation_array @ x_copy
    return x_modified, rotation_array

def rotations_3d(x, param_xy, param_yz, param_xz):
    x_1, xy_1 = rotate_xy(x, param_xy)
    x_2, yx_2 = rotate_yz(x_1, param_yz)
    x_final, xy_3 = rotate_xz(x_2, param_xz)
    final_array = xy_3 @ yx_2 @ xy_1
    return x_final, final_array


def main2():
    file_name = "airplane_0627.off"
    try:
        vertices, faces = read_off(file_name)
        print(f"file {file_name} downloaded")

        vertices_t = vertices.T
        print(f"original shape of the top: {vertices.shape}")
        print(f"transposed form for calculations: {vertices_t.shape}")

        plot_off(vertices, faces, "original 3d model")

        angle_rad_45 = np.deg2rad(45)

        X_rot_xy, A_rot_xy = rotate_xy(vertices_t, angle_rad_45)

        plot_off(X_rot_xy.T, faces, "xy (45°)")
        print("matrix xy:\n", A_rot_xy)

        X_rot_yz, A_rot_yz = rotate_yz(vertices_t, angle_rad_45)
        plot_off(X_rot_yz.T, faces, "yz (45°)")
        print("matrix yz:\n", A_rot_yz)

        X_rot_xz, A_rot_xz = rotate_xz(vertices_t, angle_rad_45)
        plot_off(X_rot_xz.T, faces, "xz (45°)")
        print("matrix xz:\n", A_rot_xz)

        params_3d = (np.deg2rad(30), np.deg2rad(60), np.deg2rad(90))

        X_final_3d, A_final_3d = rotations_3d(vertices_t, *params_3d)
        plot_off(X_final_3d.T, faces, "3d composition (30°, 60°, 90°)")
        print("final 3d matrix:\n", A_final_3d)

    except FileNotFoundError:
        print(f"\nerror")
        print(f"file '{file_name}' not found")
    except Exception as e:
        print(f"\nerror: {e}")

#main1()
main2()