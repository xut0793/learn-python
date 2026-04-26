import os
import sys

program = "python"
arguments = ["process_called.py"]

print("Process calling")

os.execvp(program, (program,) + tuple(arguments))
print("Good Bye!!")