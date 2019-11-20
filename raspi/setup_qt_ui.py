from PyQt5 import uic

with open('gui_ui.py', 'w') as fd:
    uic.compileUi('gui.ui', fd)
