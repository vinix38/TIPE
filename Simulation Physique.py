import matplotlib.pyplot as plt
import numpy as np
import time

def euler(x=0, y=0, Vx=0, Vy=0, tmax=3600, delta=0.1, BdF=lambda: 0) -> None:
    """
    Arguments x, y, Vx, Vy : conditions initiales.
    Argument tmax : temps de simulation 
    Arguments delta : intervalles de temps de simulation 
    Argument BdF : fonction renvoyant l'accélération.
    Tous les paramètres doivent être en unités SI.
    """
    t = 0

    lx = []
    ly = []
    lVx = []
    lVy = []
    lt = []
    

    while t <= tmax:

        lx.append(x)
        ly.append(y)
        lVx.append(Vx)
        lVy.append(Vy)
        lt.append(t)

        x += Vx * delta
        y += Vy * delta
        
        Vx += BdF(x, y, Vx, Vy, t)[0] * delta
        Vy += BdF(x, y, Vx, Vy, t)[1] * delta

        t += delta
        #print(f"x = {x}, y = {y}\nVx = {Vx}, Vy = {Vy}")
    plt.subplot(221)
    plt.title("position")
    plt.plot(lx, ly, "-", color="red")
    plt.subplot(223)
    plt.title("Vitesse horizontal")
    plt.plot(lt, lVx, "-", color="blue")
    plt.subplot(224)
    plt.title("Vitesse vertical")
    plt.plot(lt, lVy, "-", color="blue")
    plt.show()


def forces(x:float, y:float, Vx:float, Vy:float, t:float) -> tuple:
    """
    liste des forces exercés sur le mobile étudié, en unité SI.
    Les forces peuvent dépendre de la position ou de la vitesse.
    renvoie un tuple d'accélérations (Ax, Ay)
    """
    G = 6.6743e-11
    M = 5.972e24
    R = 6400e3
    Ratm = 100e3
    m = 2

    Ax = 0
    Ay = 0


    norme_P = (G * M) / (x**2 + y**2)
    d = np.sqrt(x**2 + y**2)

    Ax += - x / d * norme_P
    Ay += - y / d * norme_P

    #print(x, y, Vx, Vy, ax, ay, t)
    return Ax, Ay


# exemple de simulation :
euler(x=6400e3+400e4, y=0, Vx=0, Vy=6e3, delta=0.1, BdF=forces, tmax=50_000)