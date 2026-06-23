import logging
from pathlib import Path
import sys
import os


os.environ["TERM"] = "xterm-256color"
os.environ["NO_COLOR"] = ""

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

def color_from_hex(hex_code, bold=False, italic=False, underline=False, strike=False, invert=False):
    hex_code = hex_code.lstrip('#')
    r, g, b = tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))
    codes = []
    if bold:      codes.append("1")
    if italic:    codes.append("3")
    if underline: codes.append("4")
    if invert:    codes.append("7")
    if strike:    codes.append("9")
    codes.append(f"38;2;{r};{g};{b}")
    return f"\033[{';'.join(codes)}m"

MODULE_COLORS = {
    r"cogs\lifecycle": GREEN,
    r"cogs\dart": color_from_hex("#f04c4b"),
}


class RelativePathFilter(logging.Filter):
    def filter(self, record):
        try:
            rel_path = Path(record.pathname).resolve().relative_to(Path.cwd())
            record.rel_module = str(rel_path).removesuffix(".py")
        except ValueError:
            record.rel_module = Path(record.pathname).stem
        return True


class CustomFormatter(logging.Formatter):
    def format(self, record):
        rel_module = getattr(record, 'rel_module', Path(record.pathname).stem)
        msg = record.getMessage()

        bold_module = f"{BOLD}{rel_module}{RESET}"

        if record.levelno >= logging.ERROR:
            return f"{RED}[{record.levelname}] {bold_module}:{record.lineno}{RESET}\n{msg}"

        elif record.levelno >= logging.WARNING:
            return f"{YELLOW}[{record.levelname}] {bold_module}:{record.lineno} - {msg}{RESET}"

        else:  # INFO / DEBUG etc.
            color = MODULE_COLORS.get(rel_module, "")
            if color:
                return f"{color}{BOLD}[{rel_module}]{RESET} {msg}"
            else:
                return f"[{bold_module}] {msg}"


logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

# Clear old handlers
for h in logger.handlers[:]:
    logger.removeHandler(h)

# Use sys.stdout explicitly
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(CustomFormatter())
handler.addFilter(RelativePathFilter())

logger.addHandler(handler)
logger.propagate = False