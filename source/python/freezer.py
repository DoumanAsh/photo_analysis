from cx_Freeze import setup, Executable

setup(
    name="Photo project manager",
    version="0.1",
    description="Photo project manager",
    executables=[Executable("main.py")]
)