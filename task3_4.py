import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def generate_normal_distribution(mu, sigma, size):
    return [random.gauss(mu, sigma) for _ in range(size)]


def analyze_distribution(data):
    mean = np.mean(data)
    variance = np.var(data)
    _, p_value = stats.normaltest(data)
    return mean, variance, p_value


def plot_histogram(data, ax):
    ax.clear()
    ax.hist(data, bins=30, density=True, alpha=0.7, color='skyblue')
    xmin, xmax = ax.get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, np.mean(data), np.std(data))
    ax.plot(x, p, 'k', linewidth=2)
    ax.set_title("Гістограма та теоретична крива")
    ax.set_xlabel("Значення")
    ax.set_ylabel("Щільність")


class NormalDistributionApp:
    def __init__(self, master):
        self.master = master
        master.title("Моделювання нормального розподілу")

        self.frame = ttk.Frame(master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.frame, text="Середнє значення (μ):").grid(row=0, column=0, sticky=tk.W)
        self.mu_entry = ttk.Entry(self.frame)
        self.mu_entry.grid(row=0, column=1)
        self.mu_entry.insert(0, "0")

        ttk.Label(self.frame, text="Стандартне відхилення (σ):").grid(row=1, column=0, sticky=tk.W)
        self.sigma_entry = ttk.Entry(self.frame)
        self.sigma_entry.grid(row=1, column=1)
        self.sigma_entry.insert(0, "1")

        ttk.Label(self.frame, text="Кількість точок:").grid(row=2, column=0, sticky=tk.W)
        self.size_entry = ttk.Entry(self.frame)
        self.size_entry.grid(row=2, column=1)
        self.size_entry.insert(0, "1000")

        self.generate_button = ttk.Button(self.frame, text="Згенерувати та проаналізувати",
                                          command=self.generate_and_analyze)
        self.generate_button.grid(row=3, column=0, columnspan=2)

        self.result_text = tk.Text(self.frame, height=6, width=50)
        self.result_text.grid(row=4, column=0, columnspan=2)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2)

    def generate_and_analyze(self):
        mu = float(self.mu_entry.get())
        sigma = float(self.sigma_entry.get())
        size = int(self.size_entry.get())

        data = generate_normal_distribution(mu, sigma, size)
        mean, variance, p_value = analyze_distribution(data)

        result = f"Теоретичне середнє: {mu}\n"
        result += f"Оцінене середнє: {mean:.4f}\n"
        result += f"Теоретична дисперсія: {sigma ** 2}\n"
        result += f"Оцінена дисперсія: {variance:.4f}\n"
        result += f"p-значення тесту на нормальність: {p_value:.4f}\n"

        if p_value < 0.05:
            result += "Гіпотеза про нормальний розподіл відхилена (p < 0.05)"
        else:
            result += "Гіпотеза про нормальний розподіл не відхилена (p >= 0.05)"

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

        plot_histogram(data, self.ax)
        self.canvas.draw()


root = tk.Tk()
app = NormalDistributionApp(root)
root.mainloop()



