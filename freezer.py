from cx_Freeze import setup, Executable

setup(
    name="Photo annotator",
    version="0.1",
    description="Photo annotator",
    executables=[Executable("test_tkinter.py")]
)