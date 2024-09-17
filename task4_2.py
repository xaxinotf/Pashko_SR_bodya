import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

def integrand(u):
    return np.exp(-u**2 / 2)

def f(x):
    result, _ = integrate.quad(integrand, 0, x)
    return (1 / np.sqrt(2 * np.pi)) * result

class NormalDistributionApp:
    def __init__(self, master):
        self.master = master
        master.title("Обчислення функції нормального розподілу")

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
        x_values = [i * m / 10 for i in range(11)]  # 0.(i*m) для i від 0 до 10
        y_values = [f(x) for x in x_values]

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Результати обчислень:\n\n")
        for x, y in zip(x_values, y_values):
            self.result_text.insert(tk.END, f"f({x:.3f}) = {y:.6f}\n")

        self.ax.clear()
        self.ax.plot(x_values, y_values, 'b-', marker='o')
        self.ax.set_title(f"Графік функції для m = {m}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True)
        self.canvas.draw()

root = tk.Tk()
app = NormalDistributionApp(root)
root.mainloop()