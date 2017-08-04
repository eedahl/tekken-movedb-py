# tekken-movedb-py
A Tekken 7 move database. Likely to become a web app when more fully fleshed out.

## Requirements and how to
You need a Python distribution installed. I use the Anaconda distribution, adding to path when installing.

You can get Anaconda from the following link: https://www.continuum.io/downloads

You need two packages: pandas and pandastable.

To install them, write `pip install pandas` and `pip install pandastable` in a command line.

To run the program, open a command line in the filter containing it (e.g. `shift+right click` inside the folder to get an option in the drop down).

Run from the command line with `python tekken-movedb.py`.

## Suggested features
* Hide/show columns cascade
* Improve SUF, HF, BF, CHF filters
* Highlight safe moves
* Hint for unparryable lows
* Move names
* Move pet names
* Indicate moves that are not in the in-game movelist
* Add a character size category, to sort the list accordingly, with regard to character (size) specific combos etc. E.g., Gigas is max size, Ling is smallest, Kuma has short legs that fuck up certain combos etc
* Add active frames
* Add recovery frames
* Look into links for selected moves SUF < 10+frame (dis)advantage
* Move tracking info, i.e. which direction it tracks
* Throw breaks for characters like King
* A gif of the move
* A quiz mode, where you see a gif of the move and you have to input the correct frame (dis)advantage
* Show the most commonly used strings/moves and how fast of a punisher is needed to bop it.

## Acknowledgements
Moves are from RBNorway.org.

JSON-files adapted from the Tekken discord bot Combot.

Legend is from Catlord's guide, https://www.gamefaqs.com/ps4/814542-tekken-7/faqs/72021
