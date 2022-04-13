"""
Title: Exercise 03
Autor: Florian Ennemoser
Date: 21.01.2022
Course: 411.062 Data Handling in Atmospheric and Climate Physics
"""
import plotting


def create_plotting_with_trends(calc_df, pp, anomaly):
    if pp == "abs":
        plotting.fig_abs_trends_values(
            calc_df.time,
            calc_df.t,
            calc_df.tmin,
            calc_df.tmax,
            calc_df.trend_mean,
            calc_df.trend_min,
            calc_df.trend_max,
        )
    if pp == "anom" and anomaly:
        plotting.fig_anom_trends_values(
            calc_df.time, calc_df.tanomaly, calc_df.trend_anomaly
        )
    if pp == "absanom" and anomaly:
        plotting.fig_abs_anom_trends_values(
            calc_df.time,
            calc_df.t,
            calc_df.tmin,
            calc_df.tmax,
            calc_df.tanomaly,
            calc_df.trend_mean,
            calc_df.trend_min,
            calc_df.trend_max,
            calc_df.trend_anomaly,
        )
    else:
        print("HINT: if pictures are empty/white, add --anomaly and --trend flag.")
    plotting.save_figure(f"output_plotting_trends_{pp}.png")
    print(f"Plot saved as: output_plotting_trends_{pp}.png")


def create_plotting_without_trends(calc_df, pp, anomaly):
    if pp == "abs":
        plotting.fig_abs_values(calc_df.time, calc_df.t, calc_df.tmin, calc_df.tmax)
    if pp == "anom" and anomaly:
        plotting.fig_anom_values(calc_df.time, calc_df.tanomaly)
    if pp == "absanom" and anomaly:
        plotting.fig_abs_anom_values(
            calc_df.time, calc_df.t, calc_df.tmin, calc_df.tmax, calc_df.tanomaly
        )
    plotting.save_figure(f"output_plotting_{pp}.png")
    print(f"Plot saved as: output_plotting_{pp}.png")
