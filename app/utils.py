import sys
import time
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


class TerminalPrinter:
    """Write message to the console"""
    def write(self, message: str):
        sys.stderr.write(f"{message}\n")


class FilePrinter:
    """Write message to the file"""
    def write(self, message: str):
        with open("log.txt", "a+", encoding="UTF8") as file:
            file.write(f"{message}\n")


class Logger:
    """Custom logger"""
    def __init__(self):
        self.prefix = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def log(self, message: str, notifier):
        notifier().write(f"{self.prefix} {message}")
