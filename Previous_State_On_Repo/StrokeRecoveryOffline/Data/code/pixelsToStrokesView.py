import random, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

def add_arrow_to_line2D(
    axes, line, arrow_locs=[0.2, 0.4, 0.6, 0.8],
    arrowstyle='-|>', arrowsize=1, transform=None):
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
    if (not(isinstance(line, list)) or not(isinstance(line[0], 
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


def arrowview(strokepath):
	strokefile = open(strokepath, "r")

	fig, ax = plt.subplots(1, 1)

	first = ["r", "g", "b"]
	second = ["^", "--", "s", "o"]

	x = []
	y = []
	for line in strokefile.readlines():
		line = line.strip()
		if line == ".PEN_DOWN" or line == ".PEN_UP":
			#change colour
			rand = random.random()%12

			last = first[ int(rand/4) ] + second[ int(rand)%4 ]
			jumppoints = 20
			if len(x) > 1:
				if len(x)>jumppoints:
					x = [x[index] for index in range(0, len(x), jumppoints) ]
					y = [y[index] for index in range(0, len(y), jumppoints) ] 
				line = ax.plot(x, y, 'k-')
				add_arrow_to_line2D(ax, line, arrow_locs=np.linspace(0., 1., 200), arrowstyle='->')

			x = []
			y = []

			continue
		else:
			coor = line.split()
			x.append( int(coor[0]) )
			y.append( int(coor[1]) )

	temp = ""
	for term in strokepath:
		if term != "/":
			temp+= term

	plt.savefig( "images/" + temp.strip(".txt") + "_arrow")
	strokefile.close()

def mainview(strokepath):

	arrowview(strokepath)

	strokefile = open(strokepath, "r")

	fig, ax = plt.subplots(1, 1)

	first = ["r", "g", "b"]
	second = ["^", "--", "s", "o"]

	x = []
	y = []
	for line in strokefile.readlines():
		line = line.strip()
		if line == ".PEN_DOWN" or line == ".PEN_UP":
			rand = int( (random.random() * 100 )%3)
			last = first[ rand ] + second[ 1 ]

			if len(x) > 1:
				plt.plot(x,y,last)
			x = []
			y = []

			continue
		else:
			coor = line.split()
			x.append( int(coor[0]) )
			y.append( int(coor[1]) )
	temp = ""
	for term in strokepath:
		if term != "/":
			temp+= term

	plt.savefig( "images/" + temp.strip(".txt") + "_")

# for i in range(1,50):
# 	i = i*2
# 	mainview("file_0_" + str(i) + ".txt")