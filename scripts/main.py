import os

from bokeh.plotting import figure
from bokeh.io import output_file, save
from bokeh.layouts import column
import pandas as pd

REPLOT = False
a_keys = ['Ax', 'Ay', 'Az']
a_cols = ['red', 'blue', 'green']
a_jump_th = 0.02
start_time = 1
end_time = 1


def process_logs(path):
    dfs = {}
    for f in os.listdir(path):
        scenario, ext = os.path.splitext(f)
        df = pd.read_csv(os.path.join(path, f))
        dfs[scenario] = df
    return dfs


def calculate_stat(scenario: str, df: pd.DataFrame):
    start = df[(df['Time'] - df['Time'][0]) < start_time]
    end = df[df['Time'] > df['Time'].iloc[-1] - end_time]
    starts = []
    ends = []
    for a in a_keys:
        a_avg_start = abs(start[a].mean())
        df_over_from_start = df[df[a].abs() > a_avg_start + a_jump_th]
        motion_start_from_start = df_over_from_start['Time'].iloc[0]
        motion_end_from_start = df_over_from_start['Time'].iloc[-1]

        a_avg_end = abs(end[a].mean())
        df_over_from_end = df[df[a].abs() > a_avg_end + a_jump_th]
        motion_start_from_end = df_over_from_end['Time'].iloc[0]
        motion_end_from_end = df_over_from_end['Time'].iloc[-1]

        if abs(motion_start_from_start - motion_start_from_end) > 1:
            print(f'Error in {scenario}, {a} start: {motion_start_from_start} vs {motion_start_from_end}')
            continue
        if abs(motion_end_from_start - motion_end_from_end) > 1:
            print(f'Error in {scenario}, {a} end: {motion_end_from_start} vs {motion_end_from_end}')
            continue

        if motion_start_from_start is not None and motion_start_from_start > 0.0:
            starts.append(motion_start_from_start)
        if motion_end_from_start is not None and motion_end_from_start > 0.0:
            ends.append(motion_end_from_start)

        if motion_start_from_end is not None and motion_start_from_end > 0.0:
            starts.append(motion_start_from_end)
        if motion_end_from_end is not None and motion_end_from_end > 0.0:
            ends.append(motion_end_from_end)

    start_mean = round(sum(starts) / len(starts), 3)
    end_mean = round(sum(ends) / len(ends), 3)
    print(f'{scenario}: starts: {start_mean} ({starts}), ends: {end_mean} ({ends})')
    print(f'{scenario}: {round(end_mean - start_mean, 3)} s')


def calculate_stats(dfs: dict):
    for scenario, df in dfs.items():
        calculate_stat(scenario, df)


def plot_single(figures, scenario, df):
    f = figure(title=scenario, height=1200, width=2200)
    for a, col in zip(a_keys, a_cols):
        f.line(df['Time'], df[a], color=col, legend_label=a.lower())
    figures.append(f)


def plot(dfs: dict):
    figures = []
    for scenario, df in dfs.items():
        plot_single(figures, scenario, df)
    output_file('shutter_scenarios.html')
    save(column(figures))


def main():
    dfs = process_logs('data')
    calculate_stats(dfs)
    if REPLOT:
        plot()


if __name__ == '__main__':
    main()
