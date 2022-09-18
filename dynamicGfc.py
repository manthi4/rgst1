from inspect import stack
import os
import sys

from gif_for_cli.execute import execute


f = open("some.txt" , "r+")
execute(os.environ,
    ["spiderlily.png"],
    f)
st = f.read()
print(st[0])
print(ascii(st))