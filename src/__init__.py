import os
import sys

from dotenv import load_dotenv

load_dotenv(override=True)

if os.path.isdir("./src"):
    os.chdir("./src")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
