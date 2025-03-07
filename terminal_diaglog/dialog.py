import os

from typing import Dict


class Option:
    def __init__(self, name: str, func: object, fargs: tuple = None, next_dialog: object = None) -> None:
        self._name: str = name
        self._func: object = func
        self._fargs: tuple = fargs
        self._next_dialog: object = next_dialog

    @property
    def name(self) -> str:
        return self._name

    @property
    def next_dialog(self) -> str:
        return self._next_dialog

    @next_dialog.setter
    def next_dialog(self, next_dialog) -> None:
        self._next_dialog = next_dialog

    @property
    def func(self) -> str:
        return (self._func, self._fargs)

    @func.setter
    def func(self, func: object, fargs=None) -> None:
        self._func = func
        self._fargs = fargs

    def execute(self) -> None:
        if self._fargs:
            self._func(*self._fargs)
        else:
            self._func()
        return self._next_dialog


class Dialog:
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._options: Dict[str, Option] = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def options(self) -> Dict[str, Option]:
        return self._options

    def add_option(self, symbol: str, name: str, func: object, fargs: tuple = None, next_dialog: object = None) -> None:
        self._options.update({symbol: Option(name, func, fargs, next_dialog)})

    def dialog(self) -> object:
        print_dialog(self)

        opt = input('> ')
        while opt not in self._options.keys():
            os.system('clear')
            print('<error: wrong option>')
            print_dialog(self)
            opt = input('> ')

        os.system('clear')
        return self._options.get(opt).execute()


def start_dialog(dialog: Dialog) -> None:
    curr = dialog
    while curr:
        os.system('clear')
        curr = curr.dialog()


def print_dialog(dialog: Dialog):
    print(dialog.name)
    for k in dialog.options:
        print(
            f"[{k}] {dialog.options[k].name}")
