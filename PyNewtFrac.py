import pygame
from time import time
from pygame.locals import *
import random
import math


def pixels(screen, color, pos, thickness):
    for i in range(-thickness, thickness):
        for j in range(-thickness, thickness):
            screen.fill(color, ((pos[0] + i, pos[1] + j), (1, 1)))


def newton_iter(f, f1, x0):
    x = x0
    if f1(x) == 0:
        return

    x = x - f(x) / f1(x)
    return x


def newton_repeat(n, f, f1, x0):
    res = x0
    for i in range(n):
        res = newton_iter(f, f1, res)
    return res


def runPG(A, roots, root_colors, f, f1, x0):
    winsize = 500

    side = math.floor(math.sqrt(len(A)))

    w1 = math.floor((winsize)/2)
    # Set up the drawing window
    screen = pygame.display.set_mode([winsize, winsize])
    screen.fill((10, 10, 10))

    scale = 1
    while True:
        print("rendering...")

        A_remapped = pygame.surfarray.pixels2d(screen)
        print(A_remapped[0][0])
        t = time()
        for i in range(-w1, w1):
            for j in range(-w1, w1):
                (x, y) = (math.floor((i + w1) * side / winsize), math.floor((j + w1) * side / winsize))

                corr_value = math.floor((side - side/scale)/(2))
                (x, y) = (math.floor(x/scale) + corr_value, math.floor(y/scale) + corr_value)

                index = x + side * y
                c = root_colors[A[index]]
                A_remapped[i + w1][j + w1] = pygame.Color(c[0], c[1], c[2])

        t1 = time()
        print("Rendered in: " + str(t1 - t) + " seconds")
        # Flip the display
        print("waiting for input...")
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN and event.key == K_w:
                scale += 0.5
                break
            if event.type == KEYDOWN and event.key == K_s and scale > 1:
                scale -= 0.5
                break
            if event.type == KEYDOWN and event.key == K_i:
                x0 = input("Enter the lambda value to start (for example '-3+2j'): ")
                newton_roots_coloring(f, f1, x0, winsize)
                break
            if event.type == KEYDOWN and event.key == K_c:
                for i in range(len(root_colors)):
                    r = random.randint(50,150)
                    g = random.randint(50,150)
                    b = random.randint(50,150)
                    root_colors[i] = (r, g, b)
                break
            pygame.display.flip()

    pygame.quit()


def newton_roots_coloring(f, f1, x0, winsize):
    w1 = math.floor((winsize)/2)

    A = []
    roots = []

    for i in range(-w1, w1):
        for j in range(-w1, w1):
            if j != 0 and i != 0:
                x0 = i + j * 1j
                newt = newton_repeat(50, f, f1, x0)

                found = 0
                current_root_index = 0

                for r in range(len(roots)):
                    if abs(newt - roots[r]) < .0001:
                        found += 1
                        current_root_index = r
                        break

                if len(roots) == 0:
                    roots.append(newt)
                    found = 1

                if found == 0:
                    roots.append(newt)

                A.append(current_root_index)
            else:
                A.append(0)
        if i % (winsize/10) == 0:
            print(str((i+w1)/(winsize/100)) + "%")

    root_colors = []
    for r in roots:
        r = random.randint(50,150)
        g = random.randint(50,150)
        b = random.randint(50,150)
        root_colors.append((r, g, b))

    print(root_colors)

    runPG(A, roots, root_colors, *[f, f1, x0])
