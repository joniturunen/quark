from textwrap import wrap
import uuid
import os
import matplotlib.pyplot as plt


def draw_horizontal_barchart(totals, current_guild=None, bar_colors=['red', 'green', 'blue'], value_color='white', chart_text_color="#DAE4D0", time_unit='h', member=False):
    filename = './temp/'+str(uuid.uuid4())+'.png'
    totals = dict(
        sorted(totals.items(), key=lambda item: item[1], reverse=True))
    y_mins = list(totals.values())
    y_hours = [round((value / 60), 2) for value in y_mins]
    y = y_hours

    x = list(totals.keys())
    # last value is the sum of all values, comment the line if you wish to see the total bar
    y = y[1:21]
    x = x[1:21]

    # Following wraps long strings to several lines
    # x = ['\n'.join(wrap(l, 22)) for l in x]

    ax = plt.axes()
    ax.barh(x, y, align='center',
            color=bar_colors, edgecolor='darkgray')
    ax.xaxis.grid(color='#585c66', linestyle='dashed')
    ax.set_axisbelow(True)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(f"Played ({time_unit})", color='#ADBEC4')
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(8)

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
        ax.text(v - (v*0.15), i, str(v), color=value_color,
                fontweight='bold', fontsize=7)

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
