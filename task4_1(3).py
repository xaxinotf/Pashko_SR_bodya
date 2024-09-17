import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk


def integrand(x):
    return 1 / (1 - x + x ** 2)


def monte_carlo_integration(num_points):
    x = np.random.uniform(0, 1, num_points)
    y = np.random.uniform(0, 2, num_points)  # Максимальне значення функції приблизно 2

    under_curve = y < integrand(x)
    integral = np.sum(under_curve) / num_points * 2  # Множимо на 2, оскільки висота прямокутника 2

    return integral, x, y, under_curve


class MonteCarloApp:
    def __init__(self, master):
        self.master = master
        master.title("Метод Монте-Карло для обчислення інтегралу")

        self.frame = ttk.Frame(master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.frame, text="Кількість точок:").grid(row=0, column=0, sticky=tk.W)
        self.points_entry = ttk.Entry(self.frame)
        self.points_entry.grid(row=0, column=1)
        self.points_entry.insert(0, "10000")

        self.calculate_button = ttk.Button(self.frame, text="Обчислити", command=self.calculate)
        self.calculate_button.grid(row=1, column=0, columnspan=2)

        self.result_label = ttk.Label(self.frame, text="")
        self.result_label.grid(row=2, column=0, columnspan=2)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2)

    def calculate(self):
        num_points = int(self.points_entry.get())
        integral, x, y, under_curve = monte_carlo_integration(num_points)

        self.result_label.config(text=f"Обчислене значення інтегралу: {integral:.6f}")

        self.ax.clear()
        self.ax.scatter(x[~under_curve], y[~under_curve], color='red', alpha=0.1, s=1)
        self.ax.scatter(x[under_curve], y[under_curve], color='blue', alpha=0.1, s=1)

        x_plot = np.linspace(0, 1, 1000)
        self.ax.plot(x_plot, integrand(x_plot), 'g-', lw=2)

        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 2)
        self.ax.set_title("Візуалізація методу Монте-Карло")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

        self.canvas.draw()


root = tk.Tk()
app = MonteCarloApp(root)
root.mainloop()