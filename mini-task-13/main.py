import time
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

# Game of life initialisation
N = 256
M = 256
NUMBER_OF_STEPS = 128
np.random.seed(42)
NP_FIELD_NP_ID = np.random.randint(0, 2, size=(N, M))
NP_FIELD_PY_ID = NP_FIELD_NP_ID.copy()
PY_FIELD = NP_FIELD_NP_ID.tolist()

# Animation initialization
SHOW_ANIMATION = False

NP_FIGURE_NP_ID, NP_AXE_NP_ID = plt.subplots(figsize=(10, 10), num='Numpy with numpy indexation')
NP_FIGURE_NP_ID.tight_layout(pad=0)
NP_FIGURE_NP_ID.subplots_adjust(left=0, right=1, top=1, bottom=0)
NP_AXE_NP_ID.axis('off')
NP_FRAME_NP_ID = NP_AXE_NP_ID.imshow(NP_FIELD_NP_ID, cmap='binary')

NP_FIGURE_PY_ID, NP_AXE_PY_ID = plt.subplots(figsize=(10, 10), num='Numpy with python indexation')
NP_FIGURE_PY_ID.tight_layout(pad=0)
NP_FIGURE_PY_ID.subplots_adjust(left=0, right=1, top=1, bottom=0)
NP_AXE_PY_ID.axis('off')
NP_FRAME_PY_ID = NP_AXE_PY_ID.imshow(NP_FIELD_PY_ID, cmap='binary')

PY_FIGURE, PY_AXE = plt.subplots(figsize=(10, 10), num='Python')
PY_FIGURE.tight_layout(pad=0)
PY_FIGURE.subplots_adjust(left=0, right=1, top=1, bottom=0)
PY_AXE.axis('off')
PY_FRAME = PY_AXE.imshow(PY_FIELD, cmap='binary')


# Functions
def cnt_neighbours_np_id(field, i, j):
    result = -field[i, j]
    for i_shift in [-1, 0, 1]:
        for j_shift in [-1, 0, 1]:
            result += field[(i + i_shift + N) % N, (j + j_shift + M) % M]
    return result


def cnt_neighbours_py_id(field, i, j):
    result = -field[i][j]
    for i_shift in [-1, 0, 1]:
        for j_shift in [-1, 0, 1]:
            result += field[(i + i_shift + N) % N][(j + j_shift + M) % M]
    return result


def py_gol_step(field):
    next_field = copy.deepcopy(field)
    for i in range(N):
        for j in range(M):
            neighbours = cnt_neighbours_py_id(field, i, j)
            if ((not field[i][j]) and neighbours == 3) or (field[i][j] and (neighbours == 2 or neighbours == 3)):
                next_field[i][j] = 1
            else:
                next_field[i][j] = 0
    return next_field


def np_gol_step_np_id(field):
    next_field = field.copy()
    for i in range(N):
        for j in range(M):
            neighbours = cnt_neighbours_np_id(field, i, j)
            if ((not field[i, j]) and neighbours == 3) or (field[i, j] and (neighbours == 2 or neighbours == 3)):
                next_field[i, j] = 1
            else:
                next_field[i, j] = 0
    return next_field


def np_gol_step_py_id(field):
    next_field = field.copy()
    for i in range(N):
        for j in range(M):
            neighbours = cnt_neighbours_py_id(field, i, j)
            if ((not field[i][j]) and neighbours == 3) or (field[i][j] and (neighbours == 2 or neighbours == 3)):
                next_field[i][j] = 1
            else:
                next_field[i][j] = 0
    return next_field


def py_frame_update(frame):
    global PY_FIELD
    PY_FIELD = py_gol_step(PY_FIELD)
    PY_FRAME.set_data(PY_FIELD)
    return [PY_FRAME]


def np_frame_update_np_id(frame):
    global NP_FIELD_NP_ID
    NP_FIELD_NP_ID = np_gol_step_np_id(NP_FIELD_NP_ID)
    NP_FRAME_NP_ID.set_data(NP_FIELD_NP_ID)
    return [NP_FRAME_NP_ID]


def np_frame_update_py_id(frame):
    global NP_FIELD_PY_ID
    NP_FIELD_PY_ID = np_gol_step_py_id(NP_FIELD_PY_ID)
    NP_FRAME_PY_ID.set_data(NP_FIELD_PY_ID)
    return [NP_FRAME_PY_ID]


# Main
PY_ANIMATION = ani.FuncAnimation(PY_FIGURE, py_frame_update, frames=NUMBER_OF_STEPS, interval=0, repeat=False)
NP_ANIMATION_NP_ID = ani.FuncAnimation(NP_FIGURE_NP_ID, np_frame_update_np_id, frames=NUMBER_OF_STEPS, interval=0,
                                       repeat=False)
NP_ANIMATION_PY_ID = ani.FuncAnimation(NP_FIGURE_PY_ID, np_frame_update_py_id, frames=NUMBER_OF_STEPS, interval=0,
                                       repeat=False)

if SHOW_ANIMATION:
    plt.close(NP_FIGURE_NP_ID)
    plt.close(NP_FIGURE_PY_ID)
    plt.show()
else:
    TIMER_START = time.time()
    NP_ANIMATION_NP_ID.save('./NP_GOL_NP_ID.gif', writer='pillow', fps=5)
    print(f"Numpy with numpy indexation time: {(time.time() - TIMER_START):.4f}")

    TIMER_START = time.time()
    NP_ANIMATION_PY_ID.save('./NP_GOL_PY_ID.gif', writer='pillow', fps=5)
    print(f"Numpy with python indexation time: {(time.time() - TIMER_START):.4f}")

    TIMER_START = time.time()
    PY_ANIMATION.save('./PY_GOL.gif', writer='pillow', fps=5)
    print(f"Python time: {(time.time() - TIMER_START):.4f}")

plt.close('all')
