import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from keypad import Keypad


class HistoryWindow(tk.Toplevel):
    def __init__(self, parent, history_list: list):
        super().__init__(parent)
        self.title("History tabs")
        self.attributes('-topmost', True)

        # Set attribute for return to display
        self.equation = ''
        self.result = ''
        # Set and create Listbox widget
        self.selected_list = tk.Variable(value=history_list)
        self.listbox = tk.Listbox(self, listvariable=self.selected_list,
                                  selectmode=tk.SINGLE)

        self.init_components()

    def init_components(self):
        button = Keypad(self, ['equation', 'result'], 2)
        button.bind('<Button-1>', self.get_value)
        
        self.listbox.bind('<<ListboxSelect>>', self.set_equation)

        self.listbox.pack(side=tk.TOP, fill='both')
        button.pack(side=tk.TOP, expand=True, fill='both')

    def set_equation(self, event):
        try:
            # Get the index of the selected item
            selected_index = self.listbox.curselection()
            if selected_index:
                selected_item = self.listbox.get(selected_index)
                # Set the display to the selected equation or result
                equation, result = selected_item.split('=')
                parent = self.master  # Get the parent widget (CalculatorUI instance)
                parent.display_text.set(
                    result.strip())  # Set the display text to the
        except IndexError:
            pass

    def get_value(self, event):
        if event.widget['text'] == 'equation':
            return self.equation
        if event.widget['text'] == 'result':
            return self.result

    def run(self):
        self.mainloop()
