import subprocess

try:
    import passlib
except ImportError:
    subprocess.call(['python', '-m', 'pip', 'install', 'passlib'])