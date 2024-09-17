import numpy as np
from tkinter import *
from tkinter import messagebox
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def is_inside_shape(x, y, z):
    numerator = z**2
    denominator = x**2 + y**2
    with np.errstate(divide='ignore', invalid='ignore'):
        rhs = numerator / denominator
        lhs = (x**2 + y**2 + z**2)**3
        inside = lhs <= rhs
        inside = np.logical_and(inside, denominator != 0)
        inside = np.nan_to_num(inside, nan=False)
    return inside

def calculate_volume(num_points):
    R_max = 1.5  # Радіус обмежуючого боксу
    Z_max = 1.5  # Максимальне значення z

    # Генеруємо випадкові точки в боксі
    x_rand = np.random.uniform(-R_max, R_max, num_points)
    y_rand = np.random.uniform(-R_max, R_max, num_points)
    z_rand = np.random.uniform(0, Z_max, num_points)

    # Перевіряємо, чи точки всередині фігури
    inside = is_inside_shape(x_rand, y_rand, z_rand)
    inside = inside.astype(np.float64)

    # Обчислюємо об'єм
    volume_box = (2 * R_max) * (2 * R_max) * Z_max
    fraction_inside = np.mean(inside)
    volume_shape = volume_box * fraction_inside

    # Обчислюємо стандартну похибку
    std_error = volume_box * np.std(inside) / np.sqrt(num_points)

    return volume_shape, std_error

def plot_shape():
    # Визначаємо сітку
    R_max = 1.5
    Z_max = 1.5
    n = 50
    x = np.linspace(-R_max, R_max, n)
    y = np.linspace(-R_max, R_max, n)
    z = np.linspace(0, Z_max, n)
    X, Y, Z = np.meshgrid(x, y, z)

    # Обчислюємо значення функції
    numerator = Z**2
    denominator = X**2 + Y**2
    with np.errstate(divide='ignore', invalid='ignore'):
        rhs = numerator / denominator
        lhs = (X**2 + Y**2 + Z**2)**3
        F = lhs - rhs
        F = np.nan_to_num(F, nan=1e6, posinf=1e6, neginf=-1e6)

    # Побудова ізоповерхні
    fig = go.Figure(data=go.Isosurface(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=F.flatten(),
        isomin=-0.1,
        isomax=0.1,
        surface_count=1,
        colorscale='Viridis',
        caps=dict(x_show=False, y_show=False, z_show=False),
    ))

    fig.update_layout(title='3D модель фігури', scene=dict(
        xaxis_title='x',
        yaxis_title='y',
        zaxis_title='z',
    ))
    fig.show()

def run_calculation():
    try:
        num_points = int(entry_points.get())
        if num_points <= 0:
            raise ValueError
        volume, std_error = calculate_volume(num_points)
        result_text.set(f"Об'єм фігури: {volume:.6f} ± {std_error:.6f}")
    except ValueError:
        messagebox.showerror("Помилка", "Будь ласка, введіть коректне число точок (позитивне ціле число).")

def plot_convergence():
    try:
        max_points = int(entry_max_points.get())
        if max_points <= 0:
            raise ValueError

        points_range = np.logspace(3, np.log10(max_points), num=10, dtype=int)
        volumes = []
        errors = []

        for num_points in points_range:
            volume, std_error = calculate_volume(num_points)
            volumes.append(volume)
            errors.append(std_error)

        plt.figure(figsize=(10,6))
        plt.errorbar(points_range, volumes, yerr=errors, fmt='o-', ecolor='red', capsize=5)
        plt.xscale('log')
        plt.xlabel('Кількість точок')
        plt.ylabel('Об\'єм фігури')
        plt.title('Збіжність обчислення об\'єму методом Монте-Карло')
        plt.grid(True)
        plt.show()

    except ValueError:
        messagebox.showerror("Помилка", "Будь ласка, введіть коректне максимальне число точок (позитивне ціле число).")

# Створення GUI
root = Tk()
root.title("Обчислення об'єму фігури")

label_points = Label(root, text="Кількість точок для методу Монте-Карло:")
label_points.pack(pady=5)

entry_points = Entry(root)
entry_points.pack(pady=5)

button_calculate = Button(root, text="Обчислити об'єм", command=run_calculation)
button_calculate.pack(pady=10)

button_plot = Button(root, text="Побудувати 3D модель", command=plot_shape)
button_plot.pack(pady=10)

label_max_points = Label(root, text="Максимальна кількість точок для графіку збіжності:")
label_max_points.pack(pady=5)

entry_max_points = Entry(root)
entry_max_points.pack(pady=5)

button_convergence = Button(root, text="Показати графік збіжності", command=plot_convergence)
button_convergence.pack(pady=10)

result_text = StringVar()
label_result = Label(root, textvariable=result_text, font=('Arial', 14))
label_result.pack(pady=10)

root.mainloop()
