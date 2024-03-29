"""This is for creating Keypad Button"""
import tkinter as tk

FONT = {'font': ("Comic sans MS", 20, 'bold')}
OPTION = {'sticky': tk.NSEW, 'ipadx': 2, 'ipady': 2, 'padx': 2, 'pady': 2}


class Keypad(tk.Frame):
    def __init__(self, parent, keynames=[], columns=1, **kwargs):
        """Initialize the frame"""
        # keynames and columns
        super().__init__(parent, **kwargs)
        self.keynames = keynames

        self.init_components(columns)

    @property
    def frame(self):
        """To return the frame of the Keypad"""
        return super()

    def init_components(self, columns):
        """Create a keypad of keys using the keynames list.
        The first keyname is at the top left of the keypad and
        fills the available columns left-to-right, adding as many
        rows as needed.
        :param columns: number of columns to use
        """
        row_num = 0
        column_num = 0
        for value in self.keynames:
            button = tk.Button(self, text=value, **FONT)
            button.grid(row=row_num, column=column_num, **OPTION)
            column_num += 1
            if column_num >= columns:
                column_num = 0
                row_num += 1

        # use rowconfigure and columnconfigure to specify weights
        for i in range(row_num):
            self.rowconfigure(i, weight=1)
        for i in range(columns):
            self.columnconfigure(i, weight=1)

    def bind(self, sequence=None, func=None, add=None):
        """Bind an event handler to an event sequence."""
        for child in self.winfo_children():
            child.bind(sequence, func, add)

    def __setitem__(self, key, value) -> None:
        """Overrides __setitem__ to allow configuration of all buttons
        using dictionary syntax.

        Example: keypad['foreground'] = 'red'
        sets the font color on all buttons to red.
        """
        for child in self.winfo_children():
            child[key] = value

    def __getitem__(self, key):
        """Overrides __getitem__ to allow reading of configuration values
        from buttons.
        Example: keypad['foreground'] would return 'red' if the button
        foreground color is 'red'.
        """
        for child in self.winfo_children():
            return child[key]

    def configure(self, cnf=None, **kwargs):
        """Apply configuration settings to all buttons."""
        for child in self.winfo_children():
            child.configure(cnf, **kwargs)
