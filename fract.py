import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import ttk
from fractpy.models import NewtonFractal
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = tk.Tk()
root.title("Басейни Нютона")

ttk.Label(text="Кількість ітерацій").pack()
niter_input = ttk.Entry()
niter_input.pack()

ttk.Label(text="lambda").pack()
lambda_input = ttk.Entry()
lambda_input.pack()

canvas = None

# Список кольорів для розрізнення коренів.
colors = ['b', 'r', 'g', 'y']

TOL = 1.e-8


def newton(z0, f, fprime, MAX_ITERATIONS=1000):
    """Метод Ньютона-Рафсона, застосований до f(z).

    Повертає знайдений корінь, починаючи з початкового припущення z0, або False
    якщо не було досягнуто збіжності до допуску TOL протягом MAX_IT ітерацій.

    """

    z = z0
    for i in range(MAX_ITERATIONS):
        dz = f(z) / fprime(z)
        if abs(dz) < TOL:
            return z
        z -= dz
    return False


def plot_newton_fractal(f, fprime, n=200, domain=(-3, 3, -3, 3)):
    """Побудуйте фрактал Ньютона, знайшовши корені f(z).

    Областю, яка використовується для зображення фрактала, є область комплексної площини
    (x_min, x_max, y_min, y_max), де z = x + iy, дискретизована на n значень вздовж
    вздовж кожної осі.

    """

    roots = []
    m = np.zeros((n, n))

    def get_root_index(roots, r):
        """Отримати індекс r у корені списку.

        Якщо r не знаходиться у корені, додати його до списку.

        """

        try:
            return np.where(np.isclose(roots, r, atol=TOL))[0][0]
        except IndexError:
            roots.append(r)
            return len(roots) - 1

    x_min, x_max, y_min, y_max = domain
    for ix, x in enumerate(np.linspace(x_min, x_max, n)):
        for iy, y in enumerate(np.linspace(y_min, y_max, n)):
            z0 = x + y*1j
            r = newton(z0, f, fprime)
            if r is not False:
                ir = get_root_index(roots, r)
                m[iy, ix] = ir
    number_of_roots = len(roots)
    if number_of_roots > len(colors):
        # Використовуйте "суцільну" кольорову карту, якщо коренів занадто багато.
        color_map = 'hsv'
    else:
        # Використовуйте список кольорів для кольорової карти: по одному для кожного кореня.
        color_map = ListedColormap(colors[:number_of_roots])
    return color_map


def draw_fractal_from_input_values():
    return plot_fractal(NewtonFractal(lambda_input.get(), nmax=int(niter_input.get())))


plot_button = ttk.Button(root, text="Згенерувати", command=draw_fractal_from_input_values)
plot_button.pack()


def plot_fractal(model, xmin=-3, xmax=3, ymin=-3, ymax=3):
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()

    fig, ax = plt.subplots()
    p = model.plot(xmin, xmax, ymin, ymax, ax, (500, 500))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()


root.mainloop()
