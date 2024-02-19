import tkinter as tk
from math import *
from pygame import mixer
from tkinter import ttk
from keypad import Keypad
from history import HistoryWindow

# Constants
OPTIONS = {'sticky': tk.NSEW, 'ipadx': 2, 'ipady': 2, 'padx': 2, 'pady': 2}
FONT = {'font': ("Comic sans MS", 20, 'bold')}
PACK = {'expand': True, 'fill': 'both'}
BUTTON_COLOR = {'bg': 'white', 'fg': '#B784B7'}
BG_COLOR = {'background': '#9290C3'}
LABEL_STYLE = {'bg': '#211951', 'fg': '#15F5BA', 'padx': 2, 'pady': 2}
BUTTON_NUMBERS = ["DEL", "CLR", "mod", "7", "8", "9", "4", "5", "6",
                  "1", "2", "3", '(', "0", ')', 'his', ".", 'hisCLR']
MAIN_OP = ['+', '-', '*', '/', "^", "="]
COMBOBOX_OP = ["sqrt", "EXP", 'log10', 'log2', 'ln']


class CalculatorUI(tk.Tk):

    def __init__(self):
        """Initialize the object"""
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

    def init_components(self):
        """Create a keypad of keys using the keynames list.
        The first keyname is at the top left of the keypad and
        fills the available columns left-to-right, adding as many
        rows as needed.
        """
        img = tk.PhotoImage(file="iconp.png")
        self.iconphoto(False, img)

        BUTTON_NUMBERS = ["DEL", "CLR", "mod", "7", "8", "9", "4", "5", "6",
                          "1", "2", "3", '(', "0", ')', 'his', ".", 'hisCLR']
        MAIN_OP = ['+', '-', '*', '/', "^", "="]
        COMBOBOX_OP = ["sqrt", "EXP", 'log10', 'log2', 'ln']

        keypad = Keypad(self, BUTTON_NUMBERS, 3)
        keypad.configure(width=5)
        keypad.bind('<Button-1>', self.key_pressed)

        main_operators = Keypad(self, MAIN_OP, 1)
        main_operators.configure(width=5)
        main_operators.bind('<Button-1>', self.key_pressed)

        combobox = ttk.Combobox(self, textvariable=self.current_fx)
        combobox['values'] = COMBOBOX_OP
        combobox.bind('<<ComboboxSelected>>', self.key_pressed)

        keypad.configure(**BUTTON_COLOR)
        main_operators.configure(**BUTTON_COLOR)
        combobox.configure(background='white', foreground='#B784B7')

        keypad.config(**BG_COLOR)
        main_operators.config(**BG_COLOR)
        combobox.config(**BG_COLOR)

        self.display_text.set("")
        self.display_label.pack(side=tk.TOP, **PACK)
        combobox.pack(side=tk.TOP, **PACK)
        keypad.pack(side=tk.LEFT, **PACK)
        main_operators.pack(side=tk.TOP, **PACK)

    def make_display(self) -> tk.Frame:
        """Make label that shows the number and calculated result"""
        frame = tk.Frame(self)
        frame.configure(highlightbackground='#9290C3', highlightthickness=2)

        # make label for display
        label = tk.Label(frame, textvariable=self.display_text, **FONT,
                         anchor=tk.E, height=2)
        label.config(**LABEL_STYLE)

        # pack
        label.pack(**PACK, side=tk.LEFT)
        return frame

    def key_pressed(self, event):
        """Binding function for widget button and combobox"""
        widget = event.widget
        mixer.Sound('press_sound.wav').play()
        if isinstance(widget, tk.Button):
            self.calculation(widget['text'])
        else:
            self.calculation(self.current_fx.get())

    def calculation(self, widget):
        """Check widget and use assign widget function"""
        operators = '+-*/^'
        if self.calculate_list and self.calculate_list[-1] in operators \
                and widget in operators and self.calculate_list[-1] != ')':
            self.calculate_list.pop()
        if widget == '=':
            self.evaluation()
        elif widget == 'hisCLR':
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
        """Calculate value using eval() but check
        and replace un calculate string"""
        try:
            # set normal color text
            self.children['!frame'].children['!label'].configure(**LABEL_STYLE)
            # make equation for calculation
            equation = ("".join(self.calculate_list).replace("mod", "%").
                        replace("^", "**").replace("ln", "log"))
            # calculate and set display
            result = eval(equation)
            self.display_text.set(f"{result:.5g}")
            self.calculate_list = [f"{result:.5g}"]
            # add to a history list
            self.history_list.append(f"{equation:<50}={result:<15.5g}")

        except (ValueError, ZeroDivisionError, SyntaxError):
            # set red text and sound
            mixer.Sound('error.wav').play()
            self.children['!frame'].children['!label']['fg'] = 'red'

    def handle_op_special(self, op):
        """Handle operators that can be used with math module"""
        try:
            last_index = self.calculate_list[-1]
            if last_index in MAIN_OP:
                self.calculate_list.append(f"{op}(")
            elif last_index == ')' or float(last_index):
                self.calculate_list.insert(0, f"{op}(")
                self.calculate_list.append(")")
            else:
                self.calculate_list.append(f"{op}(")
        except IndexError:
            self.current_fx.set('')

    def handle_ln(self):
        """For handling natural logarithm function"""
        try:
            last_index = self.calculate_list[-1]
            if last_index in MAIN_OP:
                self.calculate_list.append(f"ln(")
            elif float(last_index) or last_index == ')':
                self.calculate_list.insert(0, "ln(")
                self.calculate_list.append(")")
        except IndexError:
            self.current_fx.set('')

    def handle_expo(self):
        """For handling exponent function base 10"""
        try:
            if self.calculate_list[-1] != '*':
                self.calculate_list.append('*')
            self.calculate_list.append("(10**")
        except IndexError:
            self.current_fx.set("")

    def show_history(self):
        """Show valid calculated history"""
        history_window = HistoryWindow(self, self.history_list)
        history_window.run()

    def clear_display(self):
        """Clear the display Label and set the color to default colors"""
        # Set normal color text
        self.children['!frame'].children['!label'].configure(**LABEL_STYLE)
        self.calculate_list.clear()
        self.display_text.set('')

    def delete_last_index(self):
        """Deleted the lsat index of the calculation list"""
        try:
            self.calculate_list.pop()
            insert_string = "".join(self.calculate_list).replace("**", "^")
            self.display_text.set(insert_string)
        except IndexError:
            pass

    def run(self):
        """Make the window remain displaying"""
        self.mainloop()
