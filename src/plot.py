import logging
from typing import Any, Tuple

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.ticker as ticker

from .series import Series


class Plot():
    __series: Series

    @staticmethod
    def init():
        matplotlib.use("GTK3Agg")
        style.use("seaborn-ticks")
        style.use("seaborn-whitegrid")
        style.use("seaborn-pastel")

    def __init__(self, series: Series):
        self.__series = series

    @staticmethod
    def show():
        plt.tight_layout()
        plt.show()

    @staticmethod
    def save():
        plt.savefig("plot.svg")

    def time(self, title: str) -> Any:
        subplot = Plot.__subplot(title)
        subplot.plot(self.__series.x, self.__series.y)
        return subplot

    def barh(self, title: str, count: int):
        subplot = Plot.__subplot(title)

        fmt = ticker.StrMethodFormatter("{x:.0f}")
        plt.gca().xaxis.set_major_formatter(fmt)

        logging.info("Limiting bar plot to %d items", count)
        max_xs = self.__series.x[-count:]
        max_ys = self.__series.y[-count:]

        ax = subplot.barh(max_xs, max_ys)
        for (y, b) in zip(max_ys, ax.patches):
            plt.text(b.get_width() + 0.05,
                     b.xy[1] + .3,
                     "%d (%.1f%%)" % (y, y / sum(self.__series.y) * 100.0),
                     fontsize=11)

    @staticmethod
    def __subplot(title: str) -> Any:
        fig = plt.figure(figsize=(10, 10))
        subplot = fig.add_subplot(111)
        plt.title(title)
        return subplot

    def annotate_chunked(self, ax: Any):
        for xy in self.__series.chunk(10):
            self.__annotate(xy[0], ax)

        # annotate the last element too
        Plot.__annotate(self.__series.zip()[-1], ax)

    @staticmethod
    def __annotate(xy: Tuple, ax: Any):
        ax.plot(xy[0], xy[1], "ro", ms=5, c="dimgrey")
        plt.annotate(
            "%s (%s)" % (
                xy[1],
                xy[0].strftime("%Y-%m-%d"),
            ),
            horizontalalignment="left",
            textcoords="offset points",
            verticalalignment="top",
            xy=xy,
            xytext=(5, 0),
        )