import cx_Freeze
import sys
sys.setrecursionlimit(5000)

executables = [cx_Freeze.Executable("app.py")]

# Torch isn't included because it makes it too big.

cx_Freeze.setup(
    name="Classnap",
    version= "0.2",
    options={"build_exe": {"excludes": ["torch"], "includes": ['jinja2' , 'jinja2.ext'], "include_files": ['templates/index.html']}},
    executables=executables,
    author_email="shariefbahloul@gmail.com",
    description="Nap in class",
)