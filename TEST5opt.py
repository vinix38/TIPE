import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
##parameters
G = 6.6743e-11
M = 5.972e24
m = 2

R = 6400e3
Ratm = R + 100e3

pos0 = np.array([0, R+400e4])       #R+400e3
v0 = np.array([6e3,0])           #7.70e3 pour iss

##outils
evoldt = []
def dtmd(rslt,K,dt):
    vx = rslt[1,0]
    vy = rslt[1,1]
    nrmv = np.sqrt(vx**2+vy**2)
    dtmd = dt*((2*K)/nrmv)
    evoldt.append(dtmd)
    return dtmd

def angle(rslt):
    x = rslt[0,0]
    y = rslt[0,1]
    if y == 0:
        return np.pi/2 if x > 0 else -np.pi/2
    else:
        angle = np.arctan(x/y)
        if y < 0:
            angle += np.pi
        return angle


def alt(resultsat):
    posx = resultsat[0,0]
    posy = resultsat[0,1]
    return np.sqrt(posx**2+posy**2)

alt0 = np.sqrt(pos0[0]**2+pos0[1]**2)
a0 = np.array([0, -(G*M)/(alt0**2)])
results = [np.array([pos0,v0,a0])]
##render

def increment(results,t,dtmd,dt):
    indx = t/dt
    indx = int(indx)

    pos = (results[indx])[0]
    v = (results[indx])[1]
    a = (results[indx])[2]

    posinc = v*dtmd + pos
    vinc = a*dtmd + v

    nrmP = (G*M*m)/(alt(results[indx])**2)
    Px = -(nrmP/m)*np.sin(angle(results[indx]))
    Py = -(nrmP/m)*np.cos(angle(results[indx]))  #ATTENTION nrmP/m seulement pour tester sans frottements
    ainc = np.array([Px,Py])

    return np.array([posinc,vinc,ainc])

def render(t,dt):
    global results
    results = [np.array([pos0,v0,a0])]
    nrmv0 = np.sqrt(v0[0]**2+v0[1]**2)

    for i in np.arange(0,t,dt):

        indx = int(i/dt)
        dti = dtmd(results[indx],nrmv0,dt)
        results.append(increment(results,i,dti,dt))



    narc = 100              #nb d'arc pour approx cercle
    arc = np.pi*2/narc

    Lcx = []
    Lcy = []
    for i in range(narc+1):
        Lcx.append(R*np.cos(i*arc))
        Lcy.append(R*np.sin(i*arc))
    b = plt.plot(Lcx,Lcy,'-',color='green')

    Lcx = []
    Lcy = []
    for i in range(narc+1):
        Lcx.append(Ratm*np.cos(i*arc))
        Lcy.append(Ratm*np.sin(i*arc))
    c = plt.plot(Lcx,Lcy,'-',color='blue')

    x = []
    y = []
    for i in range(len(results)):
        x.append(results[i][0,0])
    for j in range(len(results)):
        y.append(results[j][0,1])
    a = plt.plot(x,y,'-',color='red')

    plt.axis('equal')
    plt.show()



    #return results


render(50000,0.1)