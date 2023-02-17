def colors_setup():
    if not __import__("sys").stdout.isatty():
          for _ in dir():
              if isinstance(_, str) and _[0] != "_":
                  locals()[_] = ""
    else:
          if __import__("platform").system() == "Windows":
              kernel32 = __import__("ctypes").windll.kernel32
              kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
              del kernel32

underline = "\033[4m"
crossed = "\033[9m"
purple = "\033[1;35m"
orange = "\033[0;33m"
green = "\033[1;32m"
bold = "\033[1;37m"
blink = "\033[5m"
gray = "\033[1;30m"
blue = "\033[1;34m"
cyan = "\033[1;36m"
red = "\033[1;31m"
end = "\033[0m"