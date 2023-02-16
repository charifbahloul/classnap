import cx_Freeze
import sys
sys.setrecursionlimit(5000)

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Classnap",
    version= "0.1",
    options={},
    executables=executables,
    author_email="shariefbahloul@gmail.com",
    description="Nap in class",
)