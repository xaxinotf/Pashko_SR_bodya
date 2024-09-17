import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import math

def integrand(x, n):
    return x**(n-1) * np.exp(-x)

def monte_carlo_integration(n, num_points=1000000):
    # Використовуємо експоненціальний розподіл для генерації точок
    x = np.random.exponential(1, num_points)
    y = integrand(x, n)
    return np.mean(y)

class GammaFunctionApp:
    def __init__(self, master):
        self.master = master
        master.title("Обчислення інтегралу (Гамма-функція)")

        self.frame = ttk.Frame(master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.frame, text="Номер студента (m):").grid(row=0, column=0, sticky=tk.W)
        self.m_entry = ttk.Entry(self.frame)
        self.m_entry.grid(row=0, column=1)
        self.m_entry.insert(0, "1")

        self.calculate_button = ttk.Button(self.frame, text="Обчислити", command=self.calculate)
        self.calculate_button.grid(row=1, column=0, columnspan=2)

        self.result_text = tk.Text(self.frame, height=10, width=50)
        self.result_text.grid(row=2, column=0, columnspan=2)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2)

    def calculate(self):
        m = int(self.m_entry.get())
        n_values = [0.5, 1, 1.5, 2, (m+5)/2]
        results = [monte_carlo_integration(n) for n in n_values]

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Результати обчислень:\n\n")
        for n, result in zip(n_values, results):
            self.result_text.insert(tk.END, f"n = {n:.2f}: {result:.6f}\n")

        # Обчислення точних значень (для порівняння)
        exact_values = [math.gamma(n) for n in n_values]

        self.ax.clear()
        x = np.arange(len(n_values))
        width = 0.35
        self.ax.bar(x - width/2, results, width, alpha=0.8, label='Монте-Карло')
        self.ax.bar(x + width/2, exact_values, width, alpha=0.8, label='Точне значення')
        self.ax.set_xticks(x)
        self.ax.set_xticklabels([f'{n:.2f}' for n in n_values])
        self.ax.set_xlabel('n')
        self.ax.set_ylabel('Значення інтегралу')
        self.ax.set_title(f'Порівняння результатів для m = {m}')
        self.ax.legend()
        self.canvas.draw()

root = tk.Tk()
app = GammaFunctionApp(root)
root.mainloop()