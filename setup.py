from cx_Freeze import setup, Executable
 
# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = ['matplotlib'], excludes = [])
 
import sys
base = 'Win32GUI' if sys.platform=='win32' else None
 
executables = [
    Executable('Runner.py', base=base)
]
 
setup(
    name='ET',
    version = '0.1',
    description = 'Optimal elimination trees generation',
    options = dict(build_exe = buildOptions),
    executables = executables
)
