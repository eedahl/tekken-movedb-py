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
# TODO(edahl): Throw breaks for characters like King
# TODO(edahl): Improve the legend
# TODO(edahl): Add an in-game overlay


# #
# GLOBALS
# #

# Data and view
df = None
table = None

#
move_files = None
char_names = None

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

# TODO: Implement
#       NAME = 'Name'
#       NICKNAME = 'Pet name'
#       TOP15 = 'Top 15'

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

    with open(file_path, 'r') as data_file:
        data = json.load(data_file)

    return data


def char_names_from_filenames(filenames):
    def char_name(x):
        x = re.sub('.json', '', x)
        x = re.sub('_', ' ', x)
        return x.title()

    return [char_name(x) for x in filenames]


# TODO(edahl): Make the dump file logic
def save_movelist():
    # data = df.to_json(orient='records')
    for file, char in zip(move_files, char_names):
        data = df[df[CHAR] == char].to_dict(orient='records')
        with open('test_' + file, 'w') as outfile:
            json.dump(data, outfile, indent=4, separators=(',', ': '))


def filter_data():
    global df
    global table

    # df.drop('column_name', axis=1, inplace=True)
    # df.drop(df.columns[[0, 1, 3]], axis=1)
    # df.drop([Column Name or list],inplace=True,axis=1)

    def f(x: pandas.core.series.Series):
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

    tmp_widths = table.model.columnwidths
    table.model = TableModel(tf)
    table.model.columnwidths = tmp_widths
    table.redraw()


def clear_filters():
    command_filter.set('')
    hl_filter.set('')
    suf_filter.set('')
    bf_filter.set('')
    hf_filter.set('')
    chf_filter.set('')


def open_legend(root):
    window = Toplevel(root)

    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.realpath(__file__))

    file_path = os.path.join(script_dir, 'legend.txt')

    with open(file_path, 'r') as legend_file:
        legend = legend_file.read()

    Message(window, text=legend, font='Consolas', padx=10, pady=10).pack()


# TODO(edahl): Maybe put this into a class.
def make_column_filter_frame(root):
    column_filters = Frame(root)
    column_filters.pack(side=TOP, anchor='w')

    # TODO(edahl): Fix Return filter shortcut
    # column_filters.bind("<Return>", filter_data)

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

    clear_filters_button = Button(column_filters, text="Clear filters", underline=1, command=clear_filters)
    clear_filters_button.pack(side=TOP, anchor='w', fill=X, ipadx=30, padx=15, pady=2)

    # Filter button
    filter_button = Button(column_filters, text="Filter", underline=1, command=filter_data)
    filter_button.pack(side=TOP, anchor='w', fill=X, ipadx=30, padx=15, pady=2)


def make_table_frame(root):
    table_frame = Frame(root)
    table_frame.pack(fill=BOTH, expand=1)

    display_df = df

    global table
    table = Table(table_frame, fill=BOTH, expand=1, showstatusbar=True, dataframe=display_df)
    table.show()

    # NOTE(edahl): May cause trouble as we begin hiding columns
    table.model.columnwidths[CMD] = 200
    table.model.columnwidths[HL] = 70
    table.model.columnwidths[SUF] = 70
    table.model.columnwidths[BF] = 70
    table.model.columnwidths[HF] = 70
    table.model.columnwidths[CHF] = 70
    table.model.columnwidths[DMG] = 70
    table.model.columnwidths[NOTES] = 400


def main():
    # Load moves
    global move_files
    move_files = os.listdir('./data/')

    global char_names
    char_names = char_names_from_filenames(move_files)

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
    file_menu.add_command(label='Save', command=save_movelist)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=lambda: sys.exit(1))

    view_menu = Menu(menu)
    menu.add_cascade(label="View", menu=view_menu)

    for col in cols:
        view_menu.add_checkbutton(label='Hide ' + col, state=DISABLED)
    # add_command(label="Hide column")

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

    Button(character_filters, text='Clear all', underline=3, command=lambda: set_char_buttons(0)).pack(side=TOP, fill=X,
                                                                                                       pady=2,
                                                                                                       anchor='nw')
    Button(character_filters, text='Check all', underline=2, command=lambda: set_char_buttons(1)).pack(side=TOP, fill=X,
                                                                                                       pady=2,
                                                                                                       anchor='nw')

    make_column_filter_frame(root)
    make_table_frame(root)

    # Binds
    root.bind_all('<Alt-i>', lambda event=None: filter_data())
    root.bind_all('<Alt-l>', lambda event=None: clear_filters())
    root.bind_all('<Alt-i>', lambda event=None: filter_data())
    root.bind_all('<Return>', lambda event=None: filter_data())

    root.bind_all('<Alt-a>', lambda event=None: set_char_buttons(0))
    root.bind_all('<Alt-e>', lambda event=None: set_char_buttons(1))

    root.bind_all('<F1>', lambda event=None: open_legend(root))

    root.bind_all('<Control-s>', lambda event=None: save_movelist)

    root.mainloop()


if __name__ == '__main__':
    main()
