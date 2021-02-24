from textwrap import wrap
import uuid
import os
import matplotlib.pyplot as plt


def draw_horizontal_barchart(totals, current_guild=None, bar_colors=['red', 'green', 'blue'], value_color='white', chart_text_color="#DAE4D0", time_unit='min', member=False):
    filename = './temp/'+str(uuid.uuid4())+'.png'
    y = list(totals.values())
    x = list(totals.keys())
    # last value is the sum of all values, comment the line if you wish to see the total bar
    y = y[:-1]
    x = x[:-1]

    # Following wraps long strings to several lines
    x = ['\n'.join(wrap(l, 22)) for l in x]

    ax = plt.axes()
    # fig, ax = plt.subplots()
    # ax = plt.axes(box_aspect=9/21)
    ax.barh(x, y, align='center',
            color=bar_colors, edgecolor='darkgray')

    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(f"Played ({time_unit})", color='#ADBEC4')
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(6)

    if member:
        ax.set_title(
            f'Quarks intelligence survey of {member}', color=chart_text_color)
    else:
        ax.set_title(
            f'Quarks intelligence survey: {current_guild}', color=chart_text_color)

    ax.spines['bottom'].set_color('grey')
    ax.spines['top'].set_color('grey')
    ax.spines['left'].set_color('grey')
    ax.spines['right'].set_color('grey')
    ax.tick_params(color='#7289DA', labelcolor=chart_text_color)

    for i, v in enumerate(y):
        ax.text(v - (v*0.15), i, str(v), color=value_color, fontweight='bold', fontsize=7)

    plt.tight_layout()
    plt.savefig(filename, transparent=True, dpi=600)
    # print(f'Generated bar chart file: {filename}')
    plt.clf()
    return filename


def cleanup_file(filename):
    if os.path.exists(filename):
        # print(f'Deleting file {filename}')
        os.remove(filename)
        # print(f'File {filename} deleted..')
        return True
    else:
        print(f"The file {filename} does not exist..")
        return False
