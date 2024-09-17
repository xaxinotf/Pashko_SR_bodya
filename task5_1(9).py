import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from mpl_toolkits.mplot3d import Axes3D

def random_search(func, bounds, num_iterations):
    best_x = None
    best_f = None
    for _ in range(num_iterations):
        x = np.array([np.random.uniform(low, high) for (low, high) in bounds])
        f = func(*x)
        if best_f is None or f > best_f:
            best_x = x
            best_f = f
    return best_x, best_f

def objective_function(x1, x2):
    return x1**2 * (4 - x1) - x2**2 * (4 * x2**2 - 4)

def run_random_search():
    try:
        iterations = int(entry_iterations.get())
        if iterations <= 0:
            raise ValueError
        bounds = [(-4, 4), (-4, 4)]
        best_x, best_f = random_search(objective_function, bounds, iterations)
        result_text.set(f"Найкраще x: {best_x}\nМаксимальне f(x): {best_f}")
        plot_results(best_x)
    except ValueError:
        messagebox.showerror("Помилка", "Будь ласка, введіть коректне число ітерацій (позитивне ціле число).")

def plot_results(best_x):
    x1 = np.linspace(-4, 4, 200)
    x2 = np.linspace(-4, 4, 200)
    X1, X2 = np.meshgrid(x1, x2)
    Z = objective_function(X1, X2)

    # 2D Контурний графік
    plt.figure(figsize=(8,6))
    contour = plt.contourf(X1, X2, Z, levels=50, cmap='viridis')
    plt.colorbar(contour)
    plt.plot(best_x[0], best_x[1], 'ro', label='Найкраща точка')
    plt.title('Результати випадкового пошуку (2D контурний графік)')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.legend()
    plt.show()

    # 3D Графік поверхні
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.8)
    ax.scatter(best_x[0], best_x[1], objective_function(best_x[0], best_x[1]), color='r', s=50, label='Найкраща точка')
    ax.set_title('Результати випадкового пошуку (3D графік)')
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('f(x1, x2)')
    ax.legend()
    plt.show()

# Створення GUI
root = Tk()
root.title("Метод випадкового пошуку")

label_iterations = Label(root, text="Кількість ітерацій:")
label_iterations.pack(pady=5)

entry_iterations = Entry(root)
entry_iterations.pack(pady=5)

button_run = Button(root, text="Запустити пошук", command=run_random_search)
button_run.pack(pady=10)

result_text = StringVar()
label_result = Label(root, textvariable=result_text, justify=LEFT)
label_result.pack(pady=5)

root.mainloop()
