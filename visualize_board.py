import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import enum

'''
The type of scale to plot the 2D plot.
'''
class ScaleType(enum.Enum):
    Linear = 1
    Log = 2

'''
Relative plot type normalizes over the sum of all values for each square.
Absolute plot type is for plotting the numbers directly.
'''
class PlotType(enum.Enum):
   Relative = 1
   Absolute = 2

def add_color(a, b):
    r = [0,0,0]
    r[0] = max(0, min(255, a[0] + b[0]))
    r[1] = max(0, min(255, a[1] + b[1]))
    r[2] = max(0, min(255, a[2] + b[2]))
    return r

def plot_board_3d(values, title='Chess', zname='Count'):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    bottom = np.zeros_like(values)
    width = depth = 1

    chessboard_color = []
    for col in range(8):
        for row in range(8):
            if (col+row)%2==0:
                color = (0xa4, 0x67, 0x38)  # Dark squares
            else:
                color = (0xe7, 0xcd, 0x83)  # Light squares

            extra = 0x33
            value = values[col*8 + row]
            if value > 0:
                color = add_color(color, (extra, extra, extra))
            elif value < 0:
                color = add_color(color, (-extra, -extra, -extra))
            r = "{:02x}".format(color[0])
            g = "{:02x}".format(color[1])
            b = "{:02x}".format(color[2])
            chessboard_color.append('#' + r + g + b)

    _x = np.arange(8)
    _y = np.arange(8)
    _xx, _yy = np.meshgrid(_x, _y)
    x, y = _xx.ravel(), _yy.ravel()

    for i,value in enumerate(values):
        if value < 0:
            values[i] *= -1

    ax.bar3d(x, y, bottom, width, depth, values, color=chessboard_color)
    ax.set_title(title)
    ax.set_xlabel('File')
    ax.set_ylabel('Rank')
    ax.set_zlabel(zname)
    ax.set_zlim(-0.001, max(values) * 2)
    ax.set_xticks([x+0.5 for x in range(8)])
    ax.set_yticks([x+0.5 for x in range(8)])
    ax.set_xticklabels(['A','B','C','D','E','F','G','H'])
    ax.set_yticklabels(['1','2','3','4','5','6','7','8'])

    plt.show()

def plot_board_2d(values, title='Chess', cmap='seismic', scale_type=ScaleType.Linear):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    image = np.array(values)
    image = image.reshape((8, 8))

    norm = colors.Normalize() if scale_type==ScaleType.Linear else colors.LogNorm()
    im = ax.matshow(image, origin='lower', cmap=cmap, norm=norm)
    ax.set_xlabel('File')
    ax.set_ylabel('Rank')
    ax.set_title(title)
    ax.set_xticks([x for x in range(8)])
    ax.set_yticks([x for x in range(8)])
    ax.set_xticklabels(['A','B','C','D','E','F','G','H'])
    ax.set_yticklabels(['1','2','3','4','5','6','7','8'])
    ax.tick_params(axis="x", bottom=True, top=False, labelbottom=True, labeltop=False)
    cax = fig.add_axes([0.85, 0.1, 0.075, 0.8])
    fig.colorbar(im, cax=cax, orientation='vertical')
    plt.show()




'''
Main entry point to plot both in 2D and 3d.
color_sum_per_square is an array of 64 values for squares corresponding to a1, b1, ..., h8
'''
def plot_color_sum_per_square(color_sum_per_square, title='Relative difference in player control',
                              cmap='seismic', zname='Diff', plot_type=PlotType.Relative, scale_type=ScaleType.Linear):
    board_color_sum = []
    total_sum = 0
    for i in range(64):
        board_color_sum.append(color_sum_per_square[i])
        total_sum += abs(color_sum_per_square[i])
    if plot_type == PlotType.Relative:
        for i in range(64):
            board_color_sum[i] /= total_sum

    plot_board_2d(board_color_sum, title=title, cmap=cmap, scale_type=scale_type)
    plot_board_3d(board_color_sum, title=title, zname=zname)