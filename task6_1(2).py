import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import dblquad
from tkinter import *
from tkinter import messagebox


def heart_function(x, y):
    return x ** 2 + (y - np.sqrt(np.abs(x))) ** 2 - 2


def y_lower(x):
    return -np.sqrt(2 - x ** 2) + np.sqrt(np.abs(x))


def y_upper(x):
    return np.sqrt(2 - x ** 2) + np.sqrt(np.abs(x))


def calculate_area():
    x_max = np.sqrt(2)
    area, error = dblquad(
        lambda y, x: 1,
        -x_max, x_max,
        y_lower, y_upper
    )
    return area


def plot_heart():
    x = np.linspace(-np.sqrt(2), np.sqrt(2), 400)
    y1 = y_upper(x)
    y2 = y_lower(x)

    plt.figure(figsize=(8, 8))
    plt.fill_between(x, y1, y2, where=(y1 >= y2), color='red', alpha=0.5)
    plt.plot(x, y1, 'r')
    plt.plot(x, y2, 'r')
    plt.title('Фігура "Сердечко"')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('equal')
    plt.grid(True)
    plt.show()


def show_area():
    try:
        area = calculate_area()
        result_text.set(f"Площа фігури: {area:.4f}")
    except Exception as e:
        messagebox.showerror("Помилка", f"Виникла помилка при обчисленні площі: {e}")


def plot():
    plot_heart()


# Створення GUI
root = Tk()
root.title('Фігура "Сердечко"')

button_area = Button(root, text="Обчислити площу", command=show_area)
button_area.pack(pady=10)

button_plot = Button(root, text="Побудувати графік", command=plot)
button_plot.pack(pady=10)

result_text = StringVar()
label_result = Label(root, textvariable=result_text, font=('Arial', 14))
label_result.pack(pady=10)

root.mainloop()
