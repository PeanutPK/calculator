import tkinter as tk
from math import *
from pygame import mixer
from tkinter import ttk
from keypad import Keypad
from history import HistoryWindow

OPTION = {'sticky': tk.NSEW, 'ipadx': 2, 'ipady': 2, 'padx': 2, 'pady': 2}
FONT = {'font': ("Comic sans MS", 20, 'bold')}
PACK = {'expand': True, 'fill': 'both'}
BUTTONCOLOR = {'bg': 'white', 'fg': '#B784B7'}
BGCOLOR = {'background': '#9290C3'}
LABEL = {'bg': '#211951', 'fg': '#15F5BA', 'padx': 2, 'pady': 2}


class CalculatorUI(tk.Tk):

    def __init__(self):
        super().__init__()
        mixer.init()
        self.title("Calculator")
        self.attributes('-topmost', True)

        self.current_fx = tk.StringVar()

        self.display_text = tk.StringVar()
        self.calculate_list = []

        self.history_list = []

        self.display_label = self.make_display()
        self.init_components()

    def init_components(self) -> None:
        """Create a keypad of keys using the keynames list.
        The first keyname is at the top left of the keypad and
        fills the available columns left-to-right, adding as many
        rows as needed.
        """
        img = tk.PhotoImage(file="iconp.png")
        self.iconphoto(False, img)

        BUTTON_NUMBERS = ["DEL", "CLR", "mod", "7", "8", "9", "4", "5", "6",
                          "1", "2", "3", '(', "0", ')', 'his', ".", 'AC']
        MAIN_OP = ['+', '-', '*', '/', "^", "="]
        COMBOBOX_OP = ["sqrt", "EXP", 'log10', 'log2', 'ln']

        keypad = Keypad(self, BUTTON_NUMBERS, 3)
        keypad.bind('<Button-1>', self.key_pressed)

        main_operators = Keypad(self, MAIN_OP, 1)
        main_operators.bind('<Button-1>', self.key_pressed)

        combobox = ttk.Combobox(self, textvariable=self.current_fx)
        combobox['values'] = COMBOBOX_OP
        combobox.bind('<<ComboboxSelected>>', self.key_pressed)

        keypad.configure(**BUTTONCOLOR)
        main_operators.configure(**BUTTONCOLOR)
        combobox.configure(background='white', foreground='#B784B7')

        keypad.config(**BGCOLOR)
        main_operators.config(**BGCOLOR)
        combobox.config(**BGCOLOR)

        self.display_text.set("")
        self.display_label.pack(side=tk.TOP, **PACK)
        combobox.pack(side=tk.TOP, **PACK)
        keypad.pack(side=tk.LEFT, **PACK)
        main_operators.pack(side=tk.TOP, **PACK)

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
        mixer.Sound('press_sound.wav').play()
        if isinstance(widget, tk.Button):
            self.calculation(widget['text'])
        else:
            self.calculation(self.current_fx.get())

    def calculation(self, widget):
        operators = '+-*/^'
        if self.calculate_list and self.calculate_list[-1] in operators \
                and widget in operators and self.calculate_list[-1] != ')':
            self.calculate_list.pop()
        if widget == '=':
            self.evaluation()
        elif widget == 'AC':
            self.clear_display()
            self.history_list.clear()
        elif widget == 'CLR':
            self.clear_display()
        elif widget == 'DEL':
            self.delete_last_index()
        elif widget == '^':
            self.calculate_list.append("^")
        elif widget == 'EXP':
            self.handle_expo()
        elif widget in ['sqrt', 'log2', 'log10']:
            self.handle_op_special(widget)
        elif widget == 'ln':
            self.handle_ln()
        elif widget == 'his':
            self.show_history()
        else:
            self.calculate_list.append(f"{widget}")

        new_string = "".join(self.calculate_list)
        self.display_text.set(new_string)

    def evaluation(self):
        try:
            # set normal color text
            self.children['!frame'].children['!label'].configure(**LABEL)
            # make equation for calculation
            equation = ("".join(self.calculate_list).replace("mod", "%").
                        replace("^", "**").replace("ln", "log"))
            # calculate and set display
            result = eval(equation)
            self.display_text.set(f"{result:.5g}")
            self.calculate_list = [f"{result:.5g}"]
            # add to history list
            self.history_list.append(f"{equation:<20}={result:<15.5g}")

        except (ValueError, ZeroDivisionError, SyntaxError):
            # set red text and sound
            mixer.Sound('error.wav').play()
            self.children['!frame'].children['!label']['fg'] = 'red'

    def handle_op_special(self, op):
        try:
            last_index = self.calculate_list[-1]
            if last_index.isnumeric() or last_index == ')':
                self.calculate_list.insert(0, f"{op}(")
                self.calculate_list.append(")")
            else:
                self.calculate_list.append(f"{op}(")
        except IndexError:
            self.current_fx.set('')

    def handle_ln(self):
        try:
            last_index = self.calculate_list[-1]
            if last_index.isnumeric() or last_index == ')':
                self.calculate_list.insert(0, "ln(")
                self.calculate_list.append(")")
            else:
                self.calculate_list.append(f"ln(")
        except IndexError:
            self.current_fx.set('')

    def handle_expo(self):
        try:
            if self.calculate_list[-1] != '*':
                self.calculate_list.append('*')
            self.calculate_list.append("(10**")
        except IndexError:
            self.current_fx.set("")

    def show_history(self):
        history_window = HistoryWindow(self, self.history_list)
        history_window.run()

    def clear_display(self):
        # Set normal color text
        self.children['!frame'].children['!label'].configure(**LABEL)
        self.calculate_list.clear()
        self.display_text.set('')

    def delete_last_index(self):
        try:
            self.calculate_list.pop()
            insert_string = "".join(self.calculate_list).replace("**", "^")
            self.display_text.set(insert_string)
        except IndexError:
            pass

    def run(self):
        self.mainloop()

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
