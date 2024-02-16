"""Display the calculator user interface."""
from calculator_ui import CalculatorUI


if __name__ == '__main__':
    # create the UI.  There is no controller (yet), so nothing to inject.
    ui = CalculatorUI()
    ui.run()
