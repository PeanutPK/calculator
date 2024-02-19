"""This is for the History windows display in the CalculatorUI"""
import tkinter as tk
from keypad import Keypad


class HistoryWindow(tk.Toplevel):
    """Tkinter class for displaying a separated window
    from the parent window"""
    def __init__(self, parent, history_list: list):
        """
        Initialize the program and receive value from the parent.
        :param parent: Parent object to set value to.
        :param history_list: List from a parent object.
        """
        super().__init__(parent)
        self.title("History reopen to refresh")
        self.attributes('-topmost', True)
        self.parent = parent

        # Set attribute for return to display
        self.equation = ''
        self.result = ''

        # Set and create Listbox widget
        self.selected_list = tk.Variable(value=history_list)
        self.listbox = tk.Listbox(self, listvariable=self.selected_list,
                                  selectmode=tk.SINGLE)

        self.init_components()

    def init_components(self):
        """Initialize all the component use in this object window"""
        button = Keypad(self, ['equation', 'result'], 2)
        button.bind('<Button-1>', self.get_value)

        self.listbox.bind('<<ListboxSelect>>', self.set_equation)

        self.listbox.pack(side=tk.TOP, expand=True, fill='both')
        button.pack(side=tk.TOP, expand=True, fill='both')

    def set_equation(self, event):
        """Set the equation and result value to be ready to return"""
        try:
            # Get the index of the selected item
            selected_index = self.listbox.curselection()
            if selected_index and '=' in self.listbox.get(selected_index):
                selected_item = self.listbox.get(selected_index)
                # Set the display to the selected equation or result
                self.equation, self.result = selected_item.split('=')
        except IndexError:
            pass

    def get_value(self, event):
        """Set value of the parent display to equation or value
        depends on the selected button"""
        if event.widget['text'] == 'equation':
            self.parent.display_text.set(self.equation.strip())
            self.parent.calculate_list = [self.equation.strip()]
        if event.widget['text'] == 'result':
            self.parent.display_text.set(self.result.strip())
            self.parent.calculate_list = [self.result.strip()]

    def run(self):
        self.mainloop()
