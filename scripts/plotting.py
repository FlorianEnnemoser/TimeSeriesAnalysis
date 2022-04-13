"""
Title: Exercise 03
Autor: Florian Ennemoser
Date: 21.01.2022
Course: 411.062 Data Handling in Atmospheric and Climate Physics
"""

import matplotlib.pyplot as plt

degree_sign = "\N{DEGREE SIGN}"


def create_subplot(fig, data, position, label, c, ylabel):
    ax = fig.add_subplot(position)
    ax.title.set_text(ylabel)
    for i, pair in enumerate(data):
        x, y = pair
        ax.plot(x, y, c=c[i], label=label[i])
    ax.set_xlabel("Time")
    ax.set_ylabel(r"Temp. ($\degree$C)")
    ax.grid()


def fig_abs_values(x, mean, minimum, maximum):
    fig = plt.figure(figsize=(6, 10))
    create_subplot(
        fig,
        [[x, mean]],
        311,
        "daily temp.",
        "grey",
        f"mean Temperature ({degree_sign}C)",
    )
    create_subplot(
        fig,
        [[x, minimum]],
        312,
        "min temp.",
        "blue",
        f"min. Temperature ({degree_sign}C)",
    )
    create_subplot(
        fig, [[x, maximum]], 313, "max temp.", "r", f"max. Temperature ({degree_sign}C)"
    )
    plt.tight_layout()


def fig_abs_anom_values(x, mean, minimum, maximum, anomaly):
    fig = plt.figure(figsize=(6, 10))
    create_subplot(
        fig,
        [[x, mean]],
        411,
        "daily temp.",
        "grey",
        f"mean Temperature ({degree_sign}C)",
    )
    create_subplot(
        fig,
        [[x, minimum]],
        412,
        "min temp.",
        "blue",
        f"min. Temperature ({degree_sign}C)",
    )
    create_subplot(
        fig, [[x, maximum]], 413, "max temp.", "r", f"max. Temperature ({degree_sign}C)"
    )
    create_subplot(
        fig,
        [[x, anomaly]],
        414,
        "anomaly temp.",
        "g",
        f"anomaly Temperature ({degree_sign}C)",
    )
    plt.tight_layout()


def fig_anom_values(x, anomaly):
    fig = plt.figure(figsize=(7, 5))
    create_subplot(
        fig,
        [[x, anomaly]],
        111,
        "anomaly temp.",
        "g",
        f"anomaly Temperature ({degree_sign}C)",
    )
    plt.tight_layout()


def fig_abs_trends_values(x, mean, minimum, maximum, tr_mean, tr_min, tr_max):
    fig = plt.figure(figsize=(6, 10))
    create_subplot(
        fig,
        [[x, mean], [x, tr_mean]],
        311,
        ["daily temp.", "trend"],
        ["grey", "k"],
        f"mean Temperature ({degree_sign}C)",
    )
    create_subplot(
        fig,
        [[x, minimum], [x, tr_min]],
        312,
        ["min temp.", "trend"],
        ["blue", "k"],
        f"min. Temperature ({degree_sign}C)",
    )
    create_subplot(
        fig,
        [[x, maximum], [x, tr_max]],
        313,
        ["max temp.", "trend"],
        ["r", "k"],
        f"max. Temperature ({degree_sign}C)",
    )
    plt.tight_layout()


def fig_abs_anom_trends_values(
    x, mean, minimum, maximum, anomaly, tr_mean, tr_min, tr_max, tr_anom
):
    fig = plt.figure(figsize=(6, 10))
    create_subplot(
        fig,
        [[x, mean], [x, tr_mean]],
        411,
        ["daily temp.", "trend"],
        ["grey", "k"],
        f"mean Temperature ({degree_sign}C)",
    )
    create_subplot(
        fig,
        [[x, minimum], [x, tr_min]],
        412,
        ["min temp.", "trend"],
        ["blue", "k"],
        f"min. Temperature ({degree_sign}C)",
    )
    create_subplot(
        fig,
        [[x, maximum], [x, tr_max]],
        413,
        ["max temp.", "trend"],
        ["r", "k"],
        f"max. Temperature ({degree_sign}C)",
    )
    create_subplot(
        fig,
        [[x, anomaly], [x, tr_anom]],
        414,
        ["anomaly temp.", "trend"],
        ["g", "k"],
        f"anomaly Temperature ({degree_sign}C)",
    )
    plt.tight_layout()


def fig_anom_trends_values(x_anom, anomaly, tr_anom):
    fig = plt.figure(figsize=(7, 5))
    create_subplot(
        fig,
        [[x_anom, anomaly], [x_anom, tr_anom]],
        111,
        ["anomaly temp.", "trend"],
        ["g", "k"],
        f"anomaly Temperature ({degree_sign}C)",
    )
    plt.tight_layout()


def save_figure(title):
    plt.tight_layout()
    plt.savefig(title, dpi=600)
