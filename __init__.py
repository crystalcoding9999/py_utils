from utils.colors import Colors

import sys
import importlib

# import attempts
def __try_os_import():
    try:
        return importlib.import_module("os")
    except ModuleNotFoundError:
        return None

__colorama_initialized = False
def __try_colorama_import():
    global __colorama_initialized
    try:
        colorama = importlib.import_module("colorama")
        if colorama is None:
            return None
        if not __colorama_initialized:
            colorama.init(autoreset=True)
            __colorama_initialized = True
        return colorama
    except ModuleNotFoundError:
        return None


def __ansi_supported():
    if sys.platform != "win32":
        return True
    os = __try_os_import()
    if os is None:
        return False
    return "ANSICON" in os.environ or "WT_SESSION" in os.environ or os.environ.get("TERM_PROGRAM") == "vscode"

# import warnings
__empty_terminal_os_IMPORT_WARNING = False
__empty_terminal_NO_TERM_WARNING = False
__color_print_colorama_IMPORT_WARNING = False

# terminal utils
def clear_terminal():
    empty_terminal()
def empty_terminal():
    os = __try_os_import()
    global __empty_terminal_os_IMPORT_WARNING, __empty_terminal_NO_TERM_WARNING
    if os is None:
        if not __empty_terminal_os_IMPORT_WARNING:
            print("")
            print("The function `empty_terminal()` requires the `os` module")
            print("Install the `os` module and try again")
            print("")
            __empty_terminal_os_IMPORT_WARNING = True

        return

    if "TERM" not in os.environ:
        if not __empty_terminal_NO_TERM_WARNING:
            print("")
            print("The function `empty_terminal()` does not work in this terminal environment!")
            print("This is usually caused by running in a IDE terminal")
            print("Try running the script directly from the terminal to resolve this issue.")
            print("")
            __empty_terminal_NO_TERM_WARNING = True

        return

    os.system("cls" if os.name == "nt" else "clear")

def color_print(color, *args):
    if color in Colors.__dict__.values() and __ansi_supported():
        s = " ".join(map(str, args))

        print(color + s)
        return

    colorama = __try_colorama_import()
    global __color_print_colorama_IMPORT_WARNING
    if colorama is None:
        if not __color_print_colorama_IMPORT_WARNING:
            print("")
            print("The function `color_print()` requires the 'colorama` module")
            print("Install the `colorama` module and try again")
            print("")
            __color_print_colorama_IMPORT_WARNING = True

        # functionality available without colorama
        s = " ".join(map(str, args))
        print(s)

        return

    if color not in colorama.Fore or color is None:
        color = ""

    s = " ".join(map(str, args))

    print(color + s + colorama.Fore.RESET)

def print_at(x, y, *args, color:Colors=Colors.RESET):
    # no library requirements
    if __ansi_supported():
        print("\033[{0};{1}H{3}{2}".format(y, x, " ".join(map(str, args)), color))
    else:
        print("\033[{0};{1}H{2}".format(y, x, " ".join(map(str, args))))

# check utils
def is_str(e: any) -> bool:
    if e is None:
        return False
    try:
        str(e)
        return True
    except ValueError:
        return False

def is_int(e: any) -> bool:
    if e is None:
        return False
    try:
        int(e)
        return True
    except ValueError:
        return False

def is_float(e: any) -> bool:
    if e is None:
        return False
    try:
        float(e)
        return True
    except ValueError:
        return False

# input utils

def str_input(
        *args,
        force_input=True,
        show_error=True,
        error_message="You cannot enter an empty value!",
        validate_inputs=False,
        validations=None,
        validation_error="That is not an option"
) -> str | None:
    if validations is None:
        validations = []
    res:str|None = None

    prompt = " ".join(map(str, args))

    while res is None and force_input:
        inp = input(prompt)

        if is_str(inp) and inp != "" and inp is not None:
            res = str(inp)
            if validate_inputs:
                if res not in validations:
                    res = None
                    print(validation_error)
        else:
            if show_error:
                print(error_message)

    return res

def int_input(
        *args,
        force_input=True,
        show_error=True,
        error_message="That is not a number",
        validate_inputs=False,
        validations=None,
        validation_error="That is not an option"
) -> int | None:
    if validations is None:
        validations = []
    res:int|None = None

    prompt = " ".join(map(str, args))

    while res is None and force_input:
        inp = input(prompt)

        if is_int(inp):
            res = int(inp)
            if validate_inputs:
                if res not in validations:
                    res = None
                    print(validation_error)
        else:
            if show_error:
                print(error_message)

    return res

def float_input(
        *args,
        force_input=True,
        show_error=True,
        error_message="That is not a number",
        validate_inputs=False,
        validations=None,
        validation_error="That is not an option"
) -> float | None:
    if validations is None:
        validations = []
    res:float|None = None

    prompt = " ".join(map(str, args))

    while res is None and force_input:
        inp = input(prompt)

        if is_float(inp):
            res = float(inp)
            if validate_inputs:
                if res not in validations:
                    res = None
                    print(validation_error)
        else:
            if show_error:
                print(error_message)

    return res