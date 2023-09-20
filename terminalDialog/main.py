import sys

from dialog import Dialog, start_dialog


def say_hello():
    print('hello...')


def printer(word: str):
    print(f'function with parameter: word={word}')


def interactive_func():
    r = input('write anyting: ')
    print(f'you entered: {r}')


def main():

    d1 = Dialog('DIALOG 1')
    d2 = Dialog('DIALOG 2')
    d3 = Dialog('DIALOG 3')

    d1.add_option('1', 'regular function', say_hello)
    d1.add_option('2', 'function with parameter', printer, fargs=('qwe',))
    d1.add_option('3', 'loop back', interactive_func, next_dialog=d1)
    d1.add_option('4', 'lambda', lambda: print('this is lambda'))
    d1.add_option('5', 'empty filler', lambda: None)
    d1.add_option('6', 'dialog-2', lambda: print('go to dialog-2'), next_dialog=d2)
    d1.add_option('7', 'dialog-3', lambda: print('go to dialog-3'), next_dialog=d3)
    d1.add_option('x', 'exit', lambda: sys.exit())

    d2.add_option('1', 'dialog-1', lambda: print('go back to dialog-1'), next_dialog=d1)
    d2.add_option('x', 'exit', lambda: sys.exit())

    d3.add_option('1', 'back to dialog-1', lambda: print('go back to dialog-1'), next_dialog=d1)
    d3.add_option('x', 'exit', lambda: sys.exit())

    start_dialog(d1)


if __name__ == '__main__':
    main()
