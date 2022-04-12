import plotting

def create_plotting_with_trends(calc_df,pp,anomaly):
    if pp == "abs":
        plotting.fig_abs_trends_values(calc_df.time,
                                       calc_df.t, calc_df.tmin, calc_df.tmax,
                                       calc_df.trend_mean,calc_df.trend_min,calc_df.trend_max
                                       )
    if pp == "anom" and anomaly:
        plotting.fig_anom_trends_values(calc_df.time,
                                       calc_df.tanomaly,calc_df.trend_anomaly)
    if pp == "absanom" and anomaly:
        plotting.fig_abs_anom_trends_values(
            calc_df.time, 
            calc_df.t, calc_df.tmin, calc_df.tmax,
            calc_df.tanomaly,
            calc_df.trend_mean,calc_df.trend_min,calc_df.trend_max,calc_df.trend_anomaly
        )
    plotting.save_figure(f"output_plotting_trends_{pp}.png")
    
def create_plotting_without_trends(calc_df,pp,anomaly):
        if pp == "abs":
            plotting.fig_abs_values(calc_df.time,calc_df.t, calc_df.tmin, calc_df.tmax)
        if pp == "anom" and anomaly:
            plotting.fig_anom_values(calc_df.time,calc_df.tanomaly)
        if pp == "absanom" and anomaly:
            plotting.fig_abs_anom_values(calc_df.time,calc_df.t, calc_df.tmin, calc_df.tmax,calc_df.tanomaly)
        plotting.save_figure(f"output_plotting_{pp}.png")
    