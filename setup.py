import cx_Freeze
import sys
sys.setrecursionlimit(5000)

executables = [cx_Freeze.Executable("app.py", icon="files\Classnap.ico")]

cx_Freeze.setup(
    name="Classnap",
    version= "0.1",
    options={"build_exe": {"includes": ['torch', 'jinja2' , 'jinja2.ext'], "include_files": ['templates/index.html'], "excludes": ['Tkinter']}}, # Those cause recursion errors (trying to import too much to get there).
    executables=executables,
    author_email="shariefbahloul@gmail.com",
    description="Nap in class",
)