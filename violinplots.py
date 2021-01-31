#! /usr/bin/env python3

# parse user arguments
from os.path import isfile
from sys import stdin
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input File Stream (JSON)")
parser.add_argument('-o', '--output', required=False, type=str, default=None, help="Output File")
parser.add_argument('-x', '--x', required=True, type=str, help="Key for X Values")
parser.add_argument('-y', '--y', required=True, type=str, help="Key for Y Values")
parser.add_argument('-in', '--inner', required=False, type=str, default=None, help="Violen interior")
parser.add_argument('-t', '--title', required=False, type=str, default=None, help="Figure Title")
parser.add_argument('-rx', '--rotate_xticks', action='store_true', help="Rotate X-Axis Ticks")
parser.add_argument('-xl', '--xlabel', required=False, type=str, default=None, help="X-Axis Label")
parser.add_argument('-yl', '--ylabel', required=False, type=str, default=None, help="Y-Axis Label")
parser.add_argument('-ymin', '--ymin', required=False, type=float, default=None, help="Y-Axis Minimum")
parser.add_argument('-ymax', '--ymax', required=False, type=float, default=None, help="Y-Axis Maximum")
parser.add_argument('-xlog', '--xlog', action='store_true', help="Log-Scaled X-Axis")
parser.add_argument('-ylog', '--ylog', action='store_true', help="Log-Scaled Y-Axis")
parser.add_argument('-fw', '--fig_width', required=False, type=float, default=6.4, help="Figure Width")
parser.add_argument('-fh', '--fig_height', required=False, type=float, default=4.8, help="Figure Height")
args = parser.parse_args()
if args.output is not None and isfile(args.output):
    print("Output file exists: %s" % args.output); exit(1)
if args.input == 'stdin':
    args.input = stdin
else:
    args.input = open(args.input)

# create figure+axes
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
df = pd.DataFrame(eval(args.input.read()))
fig, ax = plt.subplots()
fig.set_size_inches(args.fig_width, args.fig_height)

# plot the violin plots
sns.violinplot(data=df, x=args.x.strip(), y=args.y.strip(), inner=args.inner)

# set figure title and labels (if applicable)
if args.title is not None:
    plt.title(args.title)
if args.xlabel is not None:
    plt.xlabel(args.xlabel)
if args.ylabel is not None:
    plt.ylabel(args.ylabel)

# rotate x-axis ticks (if applicable)
if args.rotate_xticks:
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

# log-scale the axes (if applicable)
if args.xlog:
    ax.set_xscale('log')
if args.ylog:
    ax.set_yscale('log')

# set Y-axis range (if applicable)
if args.ymin is not None and args.ymax is not None:
    plt.ylim(args.ymin,args.ymax)
elif args.ymin is not None:
    plt.ylim(ymin=args.ymin)
elif args.ymax is not None:
    plt.ylim(ymax=args.ymax)

# clean up the figure and show
plt.tight_layout()
if args.output is None:
    plt.show()
else:
    fig.savefig(args.output, format=args.output.split('.')[-1], bbox_inches='tight')
