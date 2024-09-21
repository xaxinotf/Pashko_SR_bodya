import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, chisquare

# Параметри розподілу Пуассона
lambda_poisson = 3  # середнє значення (λ)
size = 1000  # кількість реалізацій

# Крок 1: Генеруємо реалізації розподілу Пуассона
# Використовуємо np.random.poisson для створення випадкової вибірки з Пуассонівського розподілу
data = np.random.poisson(lambda_poisson, size)

# Крок 2: Оцінюємо експериментальні частоти
# np.unique дозволяє знайти унікальні значення та їх частоти
unique, counts = np.unique(data, return_counts=True)
frequencies = counts / size  # Отримуємо частоти для кожного значення

# Крок 3: Обчислюємо теоретичні ймовірності для порівняння
# poisson.pmf обчислює ймовірність для Пуассонівського розподілу
theoretical_probs = poisson.pmf(unique, lambda_poisson)

# Крок 4: Нормалізуємо теоретичні ймовірності
# Це гарантує, що сума ймовірностей дорівнює 1
theoretical_probs_normalized = theoretical_probs / theoretical_probs.sum()

# Крок 5: Перевіряємо гіпотезу за допомогою критерію хі-квадрат
# chisquare перевіряє, чи узгоджуються спостережені частоти з очікуваними
chi2_stat, p_value = chisquare(counts, f_exp=theoretical_probs_normalized * size)

# Крок 6: Візуалізуємо результати
# Створюємо графік для порівняння експериментальних частот і теоретичних ймовірностей
plt.figure(figsize=(10, 5))
plt.bar(unique, frequencies, width=0.4, label='Експериментальні частоти', alpha=0.7)
plt.plot(unique, theoretical_probs, 'ro-', label='Теоретичні ймовірності', markersize=6)
plt.xlabel('Значення k')
plt.ylabel('Частота/Ймовірність')
plt.title('Порівняння експериментальних частот і теоретичних ймовірностей (розподіл Пуассона)')
plt.legend()
plt.show()

# Крок 7: Виведемо результати перевірки гіпотези
print(f"Статистика хі-квадрат: {chi2_stat}")
print(f"p-value: {p_value}")