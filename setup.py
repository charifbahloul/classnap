import cx_Freeze
import sys
sys.setrecursionlimit(5000)

executables = [cx_Freeze.Executable("app.py")]

# Torch isn't included because it makes it too big.

cx_Freeze.setup(
    name="ClassNap",
    version= "1.42",
    options={"build_exe": {"excludes": ["torch"], "includes": ['jinja2' , 'jinja2.ext'], "include_files": ['templates/index.html']}},
    executables=executables,
    author="Charif Bahloul",
    author_email="shariefbahloul@gmail.com",
    description="Nap in class",
)

# To run, put the following in the terminal: python setup.py build