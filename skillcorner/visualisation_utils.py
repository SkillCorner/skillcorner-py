import json


def _get_json_list(response):
    data_bytes = response.content
    data_list = data_bytes.decode('utf-8').split("\n")
    data = []
    for line in data_list:
        if line:
            data.append(json.loads(line))
    return data


def _convert_response_to_df(data, df_parameterization):
    import pandas as pd
    df = pd.DataFrame(data)

    if not df_parameterization:
        return df

    elif df_parameterization=='positions_per_frame':
        arrays = [[], []]

        for frame in df.frame:
            if df.data[frame]:
                for i in range(len(df.data[frame])):
                    trackable_object = df.data[frame][i]['trackable_object']
                    if trackable_object not in arrays[0]:
                        arrays[0] += [trackable_object]*2
                        arrays[1] += ['x', 'y']

        positions = _preprepare_positions(len(df.frame), len(arrays[0]))

        for frame in df.frame:
            if df.data[frame]:
                for i in range(len(df.data[frame])):
                    trackable_object = df.data[frame][i]['trackable_object']
                    index = arrays[0].index(trackable_object)
                    positions[frame][index] = df.data[frame][i]['x']
                    positions[frame][index+1] = df.data[frame][i]['y']

        names = ['trackable_object', 'position']
        arrays_2 = [[], []]
        arrays_2[0] = df.frame
        arrays_2[1] = df.timestamp
        tuples_2 = list(zip(*arrays_2))
        names_2 = ['frame', 'timestamp']
        index = pd.MultiIndex.from_tuples(tuples_2, names=names_2)

        tuples = list(zip(*arrays))
        multi_index = pd.MultiIndex.from_tuples(tuples, names=names)
        data = pd.DataFrame(positions, columns=multi_index, index=index)

        return data


def _preprepare_positions(dim_1, dim_2):
    positions = []
    for i in range(dim_1):
        temp = []
        for j in range(dim_2):
            temp.append(0)
        positions.append(temp)
    return positions


def create_visualisation_per_frame(self, match, frame):
    """
    Function to plot extrapolated data visualisation at indicated frame.

    :param match: df of extrapolated tracking data or int id of match which should be presented
    :param frame: int indicating which frame visualisation to be presented
    """
    import matplotlib.pyplot as plt
    import pandas as pd

    if not isinstance(match, pd.DataFrame):
        tracking_data = self.get_match_tracking_data(match)
    else:
        tracking_data = match

    x = tracking_data.loc[frame, tracking_data.columns.get_level_values(1)=="x"]
    y = tracking_data.loc[frame, tracking_data.columns.get_level_values(1)=="y"]
    trackable_objects = tracking_data.columns.droplevel(1).unique()
    timestamp = tracking_data.index[frame][1]
    x[x==0] = float('nan')
    y[y==0] = float('nan')

    fig, ax = plt.subplots()
    fig.suptitle(f'Tracking visualisation of frame: {frame}')
    fig.canvas.set_window_title('Skillcorner')
    _plot_field(ax)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    text = fig.text(0.15, 0.05, f"Timestamp: {timestamp}")
    scatter = ax.scatter(x, y)
    plt.show()


def create_full_visualisation(self, match, valinit=100):
    """
    Function to plot extrapolated data visualisation for the full game. Uses matplot Slider widget.

    :param match: df of extrapolated tracking data or int id of match which should be presented
    :param valinit: int indicating frame of starting point for slider
    """
    from matplotlib.widgets import Slider
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    if not isinstance(match, pd.DataFrame):
        tracking_data = self.get_match_tracking_data(match)
    else:
        tracking_data = match

    x = tracking_data.loc[valinit, tracking_data.columns.get_level_values(1)=="x"]
    y = tracking_data.loc[valinit, tracking_data.columns.get_level_values(1)=="y"]
    x[x==0] = float('nan')
    y[y==0] = float('nan')
    timestamp = tracking_data.index[valinit][1]

    fig, ax = plt.subplots()
    fig.suptitle('Tracking visualisation')
    fig.canvas.set_window_title('Skillcorner')
    plt.subplots_adjust(bottom=0.25)
    _plot_field(ax)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
    ax_slider.get_xaxis().set_visible(False)
    ax_slider.get_yaxis().set_visible(False)
    text = fig.text(0.15, 0.05, f"Timestamp: {timestamp}")
    scatter = ax.scatter(x, y)
    slider = Slider(ax=ax_slider, label='Frames', valmin=0, valmax=len(tracking_data)-1, valinit=valinit, valstep=1)

    def update(frame):
        x = tracking_data.loc[frame, tracking_data.columns.get_level_values(1)=="x"]
        y = tracking_data.loc[frame, tracking_data.columns.get_level_values(1)=="y"]
        x[x==0] = float('nan')
        y[y==0] = float('nan')
        timestamp = tracking_data.index[frame][1]
        xx = np.vstack((x, y))
        scatter.set_offsets(xx.T)
        text.set_text(f"Timestamp: {timestamp}")

    slider.on_changed(update)

    plt.show()


def _plot_rectangle(x1, x2, y1, y2, ax):
    ax.plot([x1, x1], [y1, y2], color="white", zorder=8000)
    ax.plot([x2, x2], [y1, y2], color="white", zorder=8000)
    ax.plot([x1, x2], [y1, y1], color="white", zorder=8000)
    ax.plot([x1, x2], [y2, y2], color="white", zorder=8000)


def _plot_field(ax):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Arc
    # Pitch Outline & Centre Line
    origin_x1 = -52.5
    origin_x2 = 52.5
    origin_y1 = -34
    origin_y2 = 34

    d = 2
    rectangle = plt.Rectangle(
        (origin_x1 - 2 * d, origin_y1 - 2 * d),
        105 + 4 * d,
        68 + 4 * d,
        fc="green",
        alpha=0.4,
        zorder = -5000,
    )
    ax.add_patch(rectangle)
    _plot_rectangle(origin_x1, origin_x2, origin_y1, origin_y2, ax)
    ax.plot([0, 0], [origin_y1, origin_y2], color="white", zorder=8000)

    # Left Penalty Area
    penalty_box_length = 16.5
    penalty_box_width = 40.3

    x1 = origin_x1
    x2 = origin_x1 + penalty_box_length
    y1 = -penalty_box_width / 2
    y2 = penalty_box_width / 2
    _plot_rectangle(x1, x2, y1, y2, ax)

    # Right Penalty Area
    x1 = origin_x2 - penalty_box_length
    x2 = origin_x2
    y1 = -penalty_box_width / 2
    y2 = penalty_box_width / 2
    _plot_rectangle(x1, x2, y1, y2, ax)

    # Left 6-yard Box
    six_yard_box_length = 5.5
    six_yard_box_width = 18.3

    x1 = origin_x1
    x2 = origin_x1 + six_yard_box_length
    y1 = -six_yard_box_width / 2
    y2 = six_yard_box_width / 2
    _plot_rectangle(x1, x2, y1, y2, ax)

    # Right 6-yard Box
    x1 = origin_x2 - six_yard_box_length
    x2 = origin_x2
    y1 = -six_yard_box_width / 2
    y2 = six_yard_box_width / 2
    _plot_rectangle(x1, x2, y1, y2, ax)

    # Left Goal
    goal_width = 7.3
    goal_length = 2

    x1 = origin_x1 - goal_length
    x2 = origin_x1
    y1 = -goal_width / 2
    y2 = goal_width / 2
    _plot_rectangle(x1, x2, y1, y2, ax)

    # Right Goal
    x1 = origin_x2
    x2 = origin_x2 + goal_length
    y1 = -goal_width / 2
    y2 = goal_width / 2
    _plot_rectangle(x1, x2, y1, y2, ax)

    # Prepare Circles
    circle_radius = 9.15
    penalty_spot_distance = 11
    centreCircle = plt.Circle((0, 0), circle_radius, color="white", fill=False, zorder=8000)
    centreSpot = plt.Circle((0, 0), 0.4, color="white", zorder=8000)
    lx = origin_x1 + penalty_spot_distance
    leftPenSpot = plt.Circle((lx, 0), 0.4, color="white", zorder=8000)
    rx = origin_x2 - penalty_spot_distance
    rightPenSpot = plt.Circle((rx, 0), 0.4, color="white", zorder=8000)

    # Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)

    # Prepare Arcs
    r = circle_radius * 2
    leftArc = Arc(
        (lx, 0),
        height=r,
        width=r,
        angle=0,
        theta1=307,
        theta2=53,
        color="white",
        zorder=8000,
    )
    rightArc = Arc(
        (rx, 0),
        height=r,
        width=r,
        angle=0,
        theta1=127,
        theta2=233,
        color="white",
        zorder=8000,
    )
    # Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)
