import cx_Freeze
import sys
sys.setrecursionlimit(5000)

executables = [cx_Freeze.Executable("app.py")]

cx_Freeze.setup(
    name="ClassNap",
    version="1.42",
    executables=executables,
    author="Charif Bahloul",
    author_email="shariefbahloul@gmail.com",
    description="Nap in class",
    options={
        "build_exe": {
            "include_files": ['templates/index.html'],
            "bin_includes": [
                ("C:/Users/shari/anaconda3/envs/ClassnapEnvironment/Lib/site-packages/curl_cffi.libs/libcurl-cbb416caa1dd01638554eab3f38d682d.dll"),
            ],
            "includes": ["curl_cffi"]
        }
    }
)

# To run, put the following in the terminal: python setup.py build
# Make sure to copy over libcurl-cbb416caa1dd01638554eab3f38d682d.dll into lib folder. For some reason, g4f doesn't work without it.