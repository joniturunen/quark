from textwrap import wrap
import uuid
import os
import matplotlib.pyplot as plt


def draw_horizontal_barchart(totals, time_unit='min', member=False):

    values = list(totals.values())
    filename = './temp/'+str(uuid.uuid4())+'.png'
    keys = list(totals.keys())
    keys = ['\n'.join(wrap(l, 22)) for l in keys]

    # fig, ax = plt.subplots()
    ax = plt.axes(box_aspect=0.5625)

    ax.barh(keys, values, align='center',
            color='white', edgecolor='darkgray')

    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(f"Played ({time_unit})", color='grey')
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(8)

    if member:
        ax.set_title(f'Quarks intelligence survey for {member}', color='grey')
    else:
        ax.set_title('Quarks intelligence survey', color='grey')

    ax.spines['bottom'].set_color('grey')
    ax.spines['top'].set_color('grey')
    ax.spines['left'].set_color('grey')
    ax.spines['right'].set_color('grey')
    ax.tick_params(color='grey', labelcolor='grey')

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
