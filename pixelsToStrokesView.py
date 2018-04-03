# This file is only python 3 compatible

import glob
import os
import random

import matplotlib
matplotlib.use('Agg')
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from os.path import join

import global_constants


def add_arrow_to_line2D(
        axes, line, arrow_locs=[0.3, 0.7],
        arrowstyle='-|>', arrowsize=3, transform=None):
    """
    Add arrows to a matplotlib.lines.Line2D at selected locations.

    Parameters:
    -----------
    axes: 
    line: list of 1 Line2D obbject as returned by plot command
    arrow_locs: list of locations where to insert arrows, % of total length
    arrowstyle: style of the arrow
    arrowsize: size of the arrow
    transform: a matplotlib transform instance, default to data coordinates

    Returns:
    --------
    arrows: list of arrows
    """
    if (not (isinstance(line, list)) or not (isinstance(line[0],
                                                        mlines.Line2D))):
        raise ValueError("expected a matplotlib.lines.Line2D object")
    x, y = line[0].get_xdata(), line[0].get_ydata()

    arrow_kw = dict(arrowstyle=arrowstyle, mutation_scale=10 * arrowsize)

    color = line[0].get_color()
    use_multicolor_lines = isinstance(color, np.ndarray)
    if use_multicolor_lines:
        raise NotImplementedError("multicolor lines not supported")
    else:
        arrow_kw['color'] = color

    linewidth = line[0].get_linewidth()
    if isinstance(linewidth, np.ndarray):
        raise NotImplementedError("multiwidth lines not supported")
    else:
        arrow_kw['linewidth'] = linewidth

    if transform is None:
        transform = axes.transData

    arrows = []
    for loc in arrow_locs:
        s = np.cumsum(np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2))
        n = np.searchsorted(s, s[-1] * loc)
        arrow_tail = (x[n], y[n])
        arrow_head = (np.mean(x[n:n + 2]), np.mean(y[n:n + 2]))
        p = mpatches.FancyArrowPatch(
            arrow_tail, arrow_head, transform=transform,
            **arrow_kw)
        axes.add_patch(p)
        arrows.append(p)
    return arrows


def arrow_view(strokepath, jump_points, arrow_size, output_path):
    strokefile = open(strokepath, "r")

    first = ["r", "g", "b"]
    second = ["^", "--", "s", "o"]

    x = []
    y = []

    fig, ax = plt.subplots(1, 1)

    for line in strokefile.readlines():
        line = line.strip()
        if line == ".PEN_DOWN" or line == ".PEN_UP":
            # change colour
            rand = random.random() % 12

            last = first[int(rand / 4)] + second[int(rand) % 4]
            jumppoints = jump_points
            if len(x) > 1:
                if len(x) > jumppoints:
                    x = [x[index] for index in range(0, len(x), jumppoints)]
                    y = [y[index] for index in range(0, len(y), jumppoints)]
                line = ax.plot(x, y, 'k-')
                add_arrow_to_line2D(ax, line, arrow_locs=np.linspace(0., 1., 200), arrowstyle='->', arrowsize=arrow_size)

            x = []
            y = []

            continue
        else:
            coor = line.split()
            x.append(int(coor[0]))
            y.append(int(coor[1]))

    export_to_image(strokepath, "_arrow_" + str(jump_points) + "_" + str(arrow_size), fig, output_path)


def color_view(stroke_path, output_path):
    stroke_data = open(stroke_path, "r").readlines()

    first = ["r", "g", "b", "c", "k"]
    second = ["^", "--", "s", "o", "+", "*", "d"]

    for index, line_style in enumerate(second):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        x = []
        y = []
        for line in stroke_data:
            line = line.strip()
            if line == ".PEN_DOWN" or line == ".PEN_UP":
                rand = int((random.random() * 100) % len(first))
                last = first[rand] + line_style

                if len(x) > 1:
                    ax.plot(x, y, last)
                x = []
                y = []

                continue
            else:
                coor = line.split()
                x.append(int(coor[0]))
                y.append(int(coor[1]))

        export_to_image(stroke_path, "_variation_" + str(index), fig, output_path)


def normal_view(stroke_path, output_path):
    stroke_data = open(stroke_path, "r").readlines()

    x = []
    y = []

    min_distance, min_x, min_y, selection_folder = 10e10, -1, -1, "correct"

    for line in stroke_data:
        line = line.strip()
        if line == ".PEN_DOWN" or line == ".PEN_UP":

            if len(x) > 1:
                plt.plot(x, y, "b-")

                if x[0] * x[0] + y[0] * y[0] < min_distance:
                    min_distance, min_x, min_y, selection_folder = x[0] * x[0] + y[0] * y[0], x[0], y[0], "correct"

                if len(x) > 2 and x[-1] * x[-1] + y[-1] * y[-1] < min_distance:
                    min_distance, min_x, min_y, selection_folder = x[-1] * x[-1] + y[-1] * y[-1], x[-1], y[-1], "wrong"

            x = []
            y = []

            continue
        else:
            coor = line.split()
            x.append(int(float(coor[0])))
            y.append(int(float(coor[1])))

    export_to_image(stroke_path, "_variation_normal", plt, join(output_path, selection_folder))
    plt.clf()



def export_to_image(stroke_path, tag, fig, output_path):
    # Split by whatever is the system path delimiter
    directory, file_name = os.path.split(stroke_path)

    fig.savefig(join(output_path, file_name.rstrip(".tif.txt") + tag + ".png"))


if __name__ == '__main__':

    output_path = "revision_data/stroke_to_images/"

    # image_path_list = [{"path" : global_constants.offline_word_ban_data_set, "filter" : "Image1."}]
    # image_path_list.append({"path" : global_constants.offline_word_eng_data_set, "filter" : "file8_24_3."})
    # image_path_list.append({"path" : global_constants.offline_word_hin_data_set, "filter" : "file0_0_110."})

    image_path_list = [{"path" : global_constants.online_char_hin_data, "filter": "file", "output": "char_hin"},
                       {"path" : global_constants.online_char_eng_data, "filter": "img", "output": "char_eng"}]

    number_to_output = 1000

    for image_dictionary in image_path_list:
        image_files = glob.glob(join(image_dictionary["path"], "**", "*" + image_dictionary["filter"] + "*"), recursive=True)
        if len(image_files) != 0:
            os.makedirs(join(output_path, image_dictionary['output'], "correct"), exist_ok=True)
            os.makedirs(join(output_path, image_dictionary['output'], "wrong"), exist_ok=True)

        sorted_image_files = sorted(image_files)
        random.seed(0)
        random.shuffle(sorted_image_files)

        for index, input_image in enumerate(sorted_image_files):
            if index%100 ==0:
                print(image_dictionary["output"], index, number_to_output)
            normal_view(input_image, join(output_path, image_dictionary['output']))

            # arrow_view(input_image, jump_points=5, arrow_size=2, output_path)
            # color_view(input_image, output_path)

            if index >= number_to_output:
                break
