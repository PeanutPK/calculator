import tkinter as tk
from math import *
from keypad import Keypad

OPTION = {'sticky': tk.NSEW, 'ipadx': 2, 'ipady': 2, 'padx': 2, 'pady': 2}
FONT = {'font': ("Comic sans MS", 20, 'bold')}
PACK = {'expand': True, 'fill': 'both'}
BUTTONCOLOR = {'bg': 'white', 'fg': '#B784B7'}
BGCOLOR = {'background': '#9290C3'}
LABEL = {'bg': '#211951', 'fg': '#15F5BA', 'padx': 2, 'pady': 2}


class CalculatorUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.attributes('-topmost', True)

        self.display_text = tk.StringVar()
        self.calculate_list = []

        self.history_list = []

        self.display_label = self.make_display()
        self.init_components()

    @property
    def frame(self):
        return super()

    def init_components(self) -> None:
        """Create a keypad of keys using the keynames list.
        The first keyname is at the top left of the keypad and
        fills the available columns left-to-right, adding as many
        rows as needed.
        """
        button_numbers = ["(", ")", "^", "7", "8", "9", "4", "5", "6", "1",
                          "2", "3", "0", ".", "="]
        main_operator = ['CLR', '*', '/', '+', '-']

        img = tk.PhotoImage(file="iconp.png")
        self.iconphoto(False, img)

        keypad = Keypad(self, button_numbers, 3)
        keypad.bind('<Button-1>', self.key_pressed)

        main_operator = Keypad(self, main_operator, 1)
        main_operator.bind('<Button-1>', self.key_pressed)

        keypad.configure(bg='white', fg='#B784B7')
        main_operator.configure(bg='white', fg='#B784B7')

        keypad.config(**BGCOLOR)
        main_operator.config(**BGCOLOR)

        self.display_text.set("")
        self.display_label.pack(side=tk.TOP, **PACK)
        keypad.pack(side=tk.LEFT, **PACK)
        main_operator.pack(side=tk.TOP, **PACK)

    def unused_upgraded_make_keypad(self, column, keys) -> tk.Frame:
        """Create a frame containing buttons for the numeric keys.
        This function is for making keypad without using a keypad object.
        Using this method can create both number
        and operation using column and keys.
        :param column: Number of columns requires for button.
        :param keys: List of values to put in the button.
        """
        frame = tk.Frame(self)
        row_num = 0
        column_num = 0
        for value in keys:
            button = tk.Button(frame, text=value, **FONT)
            button.grid(row=row_num, column=column_num, **OPTION)
            button.bind("<Button-1>", self.key_pressed)
            column_num += 1
            if column_num >= column:
                column_num = 0
                row_num += 1

        # use rowconfigure and columnconfigure to specify weights
        for i in range(row_num):
            frame.rowconfigure(i, weight=1)
        for i in range(column):
            frame.columnconfigure(i, weight=1)
        return frame

    def make_display(self) -> tk.Frame:
        frame = tk.Frame(self)
        frame.configure(highlightbackground='#9290C3', highlightthickness=2)

        # make label for display
        label = tk.Label(frame, textvariable=self.display_text, **FONT,
                         anchor=tk.E, height=2)
        label.config(**LABEL)

        # pack
        label.pack(**PACK, side=tk.LEFT)
        return frame

    def key_pressed(self, event):
        widget = event.widget
        self.calculation(widget['text'])

    def calculation(self, widget):
        if widget == '=':
            try:
                # make equation for calculation
                equation = "".join(self.calculate_list)
                self.children['!frame'].children['!label'].configure(**LABEL)
                self.display_text.set(f"{eval(equation):.5g}")
                self.calculate_list = [f"{eval(equation)}"]
                self.history_list.append([equation, f"= {eval(equation):.5g}"])

            except SyntaxError:
                # if error
                self.children['!frame'].children['!label']['fg'] = 'red'

        elif widget == 'CLR':
            self.children['!frame'].children['!label'].configure(**LABEL)
            self.calculate_list.clear()
            self.display_text.set('')

        elif widget == 'DEL':
            try:
                self.calculate_list.pop()
                insert_string = "".join(self.calculate_list).replace("**", "^")
                self.display_text.set(insert_string)
            except IndexError:
                pass

        else:
            new_string = self.display_text.get() + f"{widget}"
            self.display_text.set(new_string)

            if widget == '^':
                self.calculate_list.append("**")
            else:
                self.calculate_list.append(f"{widget}")

    def run(self):
        self.mainloop()
