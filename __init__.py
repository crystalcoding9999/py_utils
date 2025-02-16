# only package that is always imported
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

# import warnings
__empty_terminal_os_IMPORT_WARNING = False
__color_print_colorama_IMPORT_WARNING = False

# utils
def clear_terminal():
    empty_terminal()
def empty_terminal():
    os = __try_os_import()
    global __empty_terminal_os_IMPORT_WARNING
    if os is None:
        if not __empty_terminal_os_IMPORT_WARNING:
            print("The function `empty_terminal()` requires the `os` module")
            print("Install the `os` module and try again")
            __empty_terminal_os_IMPORT_WARNING = True

        return

    os.system("cls" if os.name == "nt" else "clear")

def color_print(color, *args):
    colorama = __try_colorama_import()
    global __color_print_colorama_IMPORT_WARNING
    if colorama is None:
        if not __color_print_colorama_IMPORT_WARNING:
            print("The function `color_print()` requires the 'colorama` module")
            print("Install the `colorama` module and try again")
            __color_print_colorama_IMPORT_WARNING = True

        # functionality available without colorama
        s = "".join(map(str, args))
        print(s)

        return

    if color not in colorama.Fore or color is None:
        color = ""

    s = "".join(map(str, args))

    print(color + s + colorama.Fore.RESET)