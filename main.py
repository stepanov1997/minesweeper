from tkinter import *
from tkinter import messagebox
import random
from itertools import product


def loadProps(param):
    from jproperties import Properties
    configs = Properties()
    with open('config.properties', 'rb') as config_file:
        configs.load(config_file)
    return int(configs.get(param).data)


matrica = []
HEIGHT = loadProps('HEIGHT')
WIDTH = loadProps('WIDTH')
NUMBER_OF_MINES = loadProps('NUMBER_OF_MINES')


def fieldClick(button):
    info = button.grid_info()
    x = info["column"]
    y = info["row"]
    print(x, y)
    counted = matrica[x][y][4]
    isMine = matrica[x][y][3]
    if not isMine:
        button.configure(text=counted, background="lightgreen", foreground="black")
        if not any(e for e in [item for sublist in matrica for item in sublist] if e[0].cget('bg') == 'whitesmoke'):
            messagebox.showinfo("You win", "You are a challenger!")
        else:
            perm = list(product([-1, 0, 1], repeat=2))
            perm.remove((0, 0))
            for (a, b) in perm:
                if x + a < 0 or y + b < 0 or x + a >= HEIGHT or y + b >= WIDTH: continue
                field = matrica[x + a][y + b];
                color = field[0].cget('bg');
                if matrica[x][y][4]==0 and not (color=='lightgreen' or color=='orange'):
                    fieldClick(matrica[x + a][y + b][0])
    else:
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if matrica[i][j][3]:
                    matrica[i][j][0].configure(background="red", text="✳", foreground="black")
        messagebox.showinfo("Game over", "You are a feeder!")
        for i in range(WIDTH):
            for j in range(HEIGHT):
                matrica[i][j][0].bind('<Button-1>', lambda event: messagebox.showinfo("Game over", "You are a feeder!"))


def fieldClickEvent(event):
    button = event.widget
    fieldClick(button)


def numOfNeighbourMines(matrica, i, j):
    perm = list(product([-1, 0, 1], repeat=2))
    perm.remove((0, 0))
    counter = 0
    for (x, y) in perm:
        if i + x < 0 or j + y < 0 or i + x >= WIDTH or j + y >= HEIGHT: continue
        if matrica[i + x][j + y][3]:
            counter += 1
    tuple = matrica[i][j]
    matrica[i][j] = (tuple[0], tuple[1], tuple[2], tuple[3], counter)
    return counter


def changeColor(event):
    button = event.widget;
    oldColor = button.cget('bg');
    if oldColor == 'whitesmoke':
        button.configure(background='orange', foreground='black')
    elif oldColor == 'orange':
        button.configure(background='whitesmoke')


root = Tk()
root.title("Мајнсвипер - ✳")
# root.geometry('400x350')
root.configure(background='white')

temp_arr = []
counter = NUMBER_OF_MINES

while counter > 0:
    x = random.randint(0, WIDTH - 1)
    y = random.randint(0, HEIGHT - 1)
    if (x, y) in temp_arr:
        continue
    else:
        temp_arr.append((x, y))
        counter -= 1

print(temp_arr)
for i in range(WIDTH):
    array = []
    for j in range(HEIGHT):
        btn = Button(root, text="😮", foreground="whitesmoke", activeforeground="whitesmoke", background="whitesmoke",
                     borderwidth=2, pady=10, padx=10,
                     relief="groove")

        mineExists = (i, j) in temp_arr
        # if mineExists:
        #     btn.configure(background="red", text="✳", foreground="black")
        btn.grid(column=i, row=j)
        btn.bind('<Button-1>', fieldClickEvent)
        btn.bind('<Button-3>', changeColor)
        array.append((btn, i, j, mineExists, 0))
    matrica.append(array)

for i in range(WIDTH):
    for j in range(HEIGHT):
        numOfNeighbourMines(matrica, i, j)

print(matrica)

root.mainloop()
