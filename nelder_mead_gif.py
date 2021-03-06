import matplotlib.pyplot as plt
import numpy as np
import gif


def rosen(p: list) -> int:
    x1, x2 = p
    a = 1
    b = 100
    y = (a - x1) ** 2 + b * (x2 - x1 ** 2) ** 2
    return y


def algo(points: list, func):
    u, v, w = points
    u, v, w = sorted([x for x in [u, v, w]], key=lambda k: func(k))
    c = [(v[x] + u[x]) / 2 for x in range(len(u))]  # centroid
    r = [c[x] + (c[x] - w[x]) for x in range(2)]  # reflect
    if func(u) <= func(r) < func(v):  # accept reflect
        w = r.copy()
    elif func(r) < func(u):
        e = [c[x] + 2 * (r[x] - c[x]) for x in range(2)]  # extend
        if func(e) < func(r):  # accept extend
            w = e.copy()
        else:  # accept reflect
            w = r.copy()
    else:
        if func(v) <= func(r) < func(w):  # contract outside
            contr = [c[x] + 0.5 * (r[x] - c[x]) for x in range(2)]
            if func(contr) <= func(r):
                w = contr.copy()
            else:  # shrink
                v = [u[x] + 0.5 * (v[x] - u[x]) for x in range(2)]
                w = [u[x] + 0.5 * (w[x] - u[x]) for x in range(2)]
        else:  # contract inside
            contr = [c[x] + 0.5 * (w[x] - c[x]) for x in range(2)]
            if func(contr) < func(w):
                w = contr.copy()
            else:  # shrink
                v = [u[x] + 0.5 * (v[x] - u[x]) for x in range(2)]
                w = [u[x] + 0.5 * (w[x] - u[x]) for x in range(2)]
    return [u, v, w]


@gif.frame
def anim(points: list):
    u, v, w = points
    x1 = np.arange(-5, 5, 0.1)
    x2 = np.arange(-5, 5, 0.1)
    x1, x2 = np.meshgrid(x1, x2)
    ax = plt.axes()
    return ax.imshow(rosen([x1, x2]), origin='lower', extent=[-5, 5, -5, 5], vmax=1000), \
           ax.plot([u[0], v[0]], [u[1], v[1]], color='black', linewidth=2), \
           ax.plot([v[0], w[0]], [v[1], w[1]], color='black', linewidth=2), \
           ax.plot([u[0], w[0]], [u[1], w[1]], color='black', linewidth=2)


frames = []
points_list = [[2, -2], [4, -2], [4, -4]]       # intial points
frame = anim(points_list)
frames.append(frame)
check = 1
while check == 1:
    points_list = algo(points_list, rosen)
    frame = anim(points_list)
    frames.append(frame)
    plt.pause(0.4)
    plt.clf()
    u, v, w = points_list
    if min([np.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[0]) ** 2) for x, y in zip([u, v, w], [w, u, v])]) < 0.05:
        check = 0  # size of simplex convergence

gif.save(frames, 'nelder_mead.gif', duration=8, unit='seconds', between="startend")
