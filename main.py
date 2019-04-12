import glob
import utils

from os.path import getsize
from datetime import datetime
from collections import defaultdict
from bokeh.plotting import figure
from bokeh.io import export_svgs
from multiprocessing import Pool


def date_to_month(d):
    return datetime(d.year, d.month, 1)


base_dir = "/home/visgean/Dropbox/**/*"

picture_extensions = ['.jpg', '.jpeg', '.png']
pictures = list(filter(
    lambda f: utils.get_extension(f) in picture_extensions,
    glob.iglob(base_dir, recursive=True)
))

with Pool(12) as p:
    exif_data = p.map(utils.get_exif, pictures)
    dates = p.map(utils.parse_date, exif_data)


filesize_counter = defaultdict(int)
image_counter = defaultdict(int)
for filename, date in dates:
    if not date:
        continue

    month = date_to_month(date)
    image_counter[month] += 1
    filesize_counter[month] += getsize(filename) / 1024 ** 2

months_sorted = sorted(image_counter.keys())
size_vals = [filesize_counter[k] for k in months_sorted]
count_vals = [image_counter[k] for k in months_sorted]


count_graph = figure(
    title="Pics per month",
    background_fill_color="#E8DDCB",
    y_axis_label='# of pics',
    x_axis_label='Time',
    x_axis_type="datetime",
    output_backend="svg"
)

count_graph.vbar(x=months_sorted, top=count_vals, width=0.1)
export_svgs(count_graph, filename="count.svg")


size_graph = figure(
    title="MB of Pics per month",
    background_fill_color="#E8DDCB",
    y_axis_label='Total size in MB',
    x_axis_label='Time',
    x_axis_type="datetime",
    output_backend="svg"
)

size_graph.vbar(x=months_sorted, top=size_vals, width=0.1)
export_svgs(size_graph, filename="size.svg")
