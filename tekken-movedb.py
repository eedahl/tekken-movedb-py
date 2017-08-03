import json
import os
from tkinter import *

import pandas
from pandastable import Table, TableModel

# TODO(edahl): Hide/show columns cascade
# TODO(edahl): Improve SUF, HF, BF, CHF filters
# TODO(edahl): Highlight safe moves
# TODO(edahl): Hint for unparryable lows
# TODO(edahl): Names
# TODO(edahl): Pet names
# TODO(edahl): Indicate moves that are not in the in-game movelist
# TODO(edahl): Add a character size category, to sort the list accordingly,
# TODO         with regard to character (size) specific combos etc.
# TODO         E.g., Gigas is max size, Ling is smallest,
# TODO         Kuma has short legs that fuck up certain combos etc
# TODO(edahl): Add active frames
# TODO(edahl): Add recovery frames
# TODO(edahl): A gif of the move
# TODO(edahl): A quiz mode, where you see a gif of the move and you have to input the correct frame (dis)advantage
# TODO(edahl): Show the most commonly used strings/moves and how fast of a punisher is needed to bop it.
# TODO(edahl): Look into links. SUF < 10+frame (dis)advantage
# TODO(edahl): Move tracking info, i.e. which direction it tracks
# TODO(edahl): Clear all filters
# TODO(edahl): Throw breaks for characters like King


# #
# GLOBALS
# #

# Data and view
df = None
table = None

# Column names
CHAR = 'Character'
CMD = 'Command'
HL = 'Hit level'
SUF = 'SUF'
BF = 'BF'
HF = 'HF'
CHF = 'CHF'
DMG = 'Damage'
NOTES = 'Notes'

# Filters
active_characters = dict()

command_filter = None
hl_filter = None
suf_filter = None
bf_filter = None
hf_filter = None
chf_filter = None


def load_moves_by_filename(filename):
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.realpath(__file__))
    rel_path = './data/' + filename
    file_path = os.path.join(script_dir, rel_path)

    data_file = open(file_path)
    data = json.load(data_file)
    data_file.close()

    return data


def char_names_from_filenames(filenames):
    def char_name(x):
        x = re.sub('.json', '', x)
        x = re.sub('_', ' ', x)
        return x.title()

    return [char_name(x) for x in filenames]


def filter_characters():
    global df
    global table
    table.updateModel(TableModel(df[df[SUF] == '12']))
    table.redraw()


# NOTE(edahl): May cause trouble as we begin hiding columns
def set_column_widths():
    global table
    table.model.columnwidths[CMD] = 200
    table.model.columnwidths[HL] = 70
    table.model.columnwidths[SUF] = 70
    table.model.columnwidths[BF] = 70
    table.model.columnwidths[HF] = 70
    table.model.columnwidths[CHF] = 70
    table.model.columnwidths[DMG] = 70
    table.model.columnwidths[NOTES] = 400


def filter_data():
    global df
    global table

    # df.drop('column_name', axis=1, inplace=True)
    # df.drop(df.columns[[0, 1, 3]], axis=1)
    # df.drop([Column Name or list],inplace=True,axis=1)

    def f(x):
        suf = '(?={0})[^0-9]*'.format(re.escape(suf_filter.get()))
        bf = '(?={0})[^0-9]*'.format(re.escape(bf_filter.get()))
        hf = '(?={0})[^0-9]*'.format(re.escape(hf_filter.get()))
        chf = '(?={0})[^0-9]+'.format(re.escape(chf_filter.get()))

        b = ((active_characters[x[CHAR]].get() == 1) and
             (command_filter.get() == '' or x[CMD] == command_filter.get()) and
             (hl_filter.get() == '' or re.match(hl_filter.get(), x[HL]) is not None) and
             (suf_filter.get() == '' or re.match(suf, x[SUF]) is not None) and
             (bf_filter.get() == '' or re.search(bf, x[BF]) is not None) and
             (hf_filter.get() == '' or re.search(hf, x[HF]) is not None) and
             (chf_filter.get() == '' or re.search(chf, x[CHF]) is not None))

        return b

    tf = df[df[[CHAR, CMD, HL, SUF, BF, HF, CHF]].apply(f, axis=1)]

    temp = table.model.columnwidths
    table.model = TableModel(tf)
    table.model.columnwidths = temp
    table.redraw()


def open_legend(root):
    window = Toplevel(root)


def main():
    # Load moves
    move_files = os.listdir('./data/')

    data = [load_moves_by_filename(x) for x in move_files]
    dfs = [pandas.DataFrame(x) for x in data]

    # Arrange data
    global df
    df = pandas.concat(dfs)
    cols = [CHAR, CMD, HL, SUF, BF, HF, CHF, DMG, NOTES]
    df = df[cols]

    # Root GUI
    root = Tk()
    # root.iconbitmap('jin.ico')
    root.title('Tekken Move Database')
    root.geometry('1400x1050+20+20')

    # Menu GUI
    menu = Menu(root)
    root.config(menu=menu)
    file_menu = Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=lambda: sys.exit(1))

    view_menu = Menu(menu)
    menu.add_cascade(label="View", menu=view_menu)

    for col in cols:
        view_menu.add_checkbutton(label='Hide '+col)
    #add_command(label="Hide column")

    help_menu = Menu(menu)
    menu.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Legend", command=lambda: open_legend(root))

    # Character filter GUI
    character_filters = Frame(root)
    character_filters.pack(side=LEFT, anchor='nw', padx=10, pady=20)
    char_names = char_names_from_filenames(move_files)

    global active_characters
    char_cbs = []
    for x in char_names:
        y = IntVar()
        y.set(1)
        active_characters.update({x: y})
        cb = Checkbutton(character_filters, text=x, variable=active_characters[x])
        cb.pack(side=TOP, anchor='nw')
        char_cbs.append(cb)

    def set_char_buttons(val):
        for x in active_characters.values():
            x.set(val)

    Button(character_filters, text='Clear all', command=lambda: set_char_buttons(0)).pack(side=TOP, fill=X,
                                                                                          pady=5, anchor='nw')
    Button(character_filters, text='Check all', command=lambda: set_char_buttons(1)).pack(side=TOP, fill=X,
                                                                                          pady=5, anchor='nw')

    # Column filter GUI
    column_filters = Frame(root)
    column_filters.pack(side=TOP, anchor='w')

    global command_filter
    command_filter = StringVar()

    command_label = Label(column_filters, text="Command")
    command_label.pack(side=LEFT)
    command_entry = Entry(column_filters, textvariable=command_filter)
    command_entry.pack(side=LEFT)

    global hl_filter
    hl_filter = StringVar()

    hl_label = Label(column_filters, text="Hit levels")
    hl_label.pack(side=LEFT)
    hl_entry = Entry(column_filters, textvariable=hl_filter)
    hl_entry.pack(side=LEFT)

    global suf_filter
    suf_filter = StringVar()

    suf_label = Label(column_filters, text="Start up frames")
    suf_label.pack(side=LEFT)
    suf_entry = Entry(column_filters, textvariable=suf_filter)
    suf_entry.pack(side=LEFT)

    global bf_filter
    bf_filter = StringVar()

    bf_label = Label(column_filters, text="Block frames")
    bf_label.pack(side=LEFT)
    bf_entry = Entry(column_filters, textvariable=bf_filter)
    bf_entry.pack(side=LEFT)

    global hf_filter
    hf_filter = StringVar()

    hf_label = Label(column_filters, text="Hit frames")
    hf_label.pack(side=LEFT)
    hf_field = Entry(column_filters, textvariable=hf_filter)
    hf_field.pack(side=LEFT)

    global chf_filter
    chf_filter = StringVar()

    chf_label = Label(column_filters, text="CH frames")
    chf_label.pack(side=LEFT)
    chf_entry = Entry(column_filters, textvariable=chf_filter)
    chf_entry.pack(side=LEFT)

    # Filter button
    filter_button = Button(column_filters, text="Filter", command=filter_data)
    filter_button.pack(side=TOP, anchor='w', ipadx=30, padx=15)

    # Table GUI
    table_frame = Frame(root)
    table_frame.pack(fill=BOTH, expand=1)

    display_df = df

    global table

    table = Table(table_frame, fill=BOTH, expand=1, showstatusbar=True, dataframe=display_df)

    table.show()

    # Default column widths
    set_column_widths()

    root.mainloop()


if __name__ == '__main__':
    main()
