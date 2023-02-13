import cx_Freeze
import sys
sys.setrecursionlimit(5000)

executables = [cx_Freeze.Executable("app.py", base = "Win32gui", icon="files\Classnap.ico")]

cx_Freeze.setup(
    name="Classnap",
    # options={"build_exe": {"excludes": ['pygame._camera_opencv_highgui', 'pandas', 'scipy.special.tests', 'scipy.special._precompute', 'scipy.special', 'pyqt5', 'pyside2'], "includes":["plyer.platforms.win.notification", "bitly_api", 'adhanpy', 'zoneinfo', 'tzdata']}}, # Those cause recursion errors (trying to import too much to get there).
    executables=executables,
    # Add torch as a package.
    packages=["torch"],
    author_email="shariefbahloul@gmail.com",
    description="Nap in class"
)