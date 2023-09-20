# Simple python dialog maker

This module allows to create different dialog scenarios in terminal.

You can create:

- linear dialogs
- branching dialogs
- loop back branches

or combine them how you want

---

## HOW TO USE

(`< >` means attribute/parameter)

### Imports

    from dialog import Dialog, start_dialog

### Add dialog

Use `Dialog` class to create new dialog object.

    d = Dialog(<dialog-name>)

### Add options

Use `add_option` method to add options to dialog.

    d.add_option(<key-to-enter>, <option-name>, <function>, <function-arguments>, <next-dialog>)

\<`function`\> - can be regular function or lambda and also can take parameters.  
\<`function-arguments`\> (optional) - tuple of arguments.  
\<`next-dialog`\> (optional) - dialog, that will be called after current dialog ends.

### Begin dialog

Use `start_dialog` function to begin whole dialog

    start_dialog(<dialog-to-begin-from>)

\<`dialog-to-begin-from`\> - whole dialog begins from specified dialog.

---

_full exapmle in file `main.py`_
