# before executing this script, execute the following command, replacing /path/to/your/project/ with the absolute path to the src folder:
# - mac/linux: export PYTHONPATH="${PYTHONPATH}:/path/to/your/project/"
# - windows: set PYTHONPATH=%PYTHONPATH%;C:\path\to\your\project\

from config import paths


print("Your root path is:", paths.ROOT)
