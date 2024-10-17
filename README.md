# YouTube-Downloader
Simple YouTube video downloader project

# Preview
<img width="1312" alt="Youtube-Downloader-preview" src="https://github.com/user-attachments/assets/8141b675-28da-4d96-ad1b-326b9598ce19">


# How to build for MacOS
1. Create a virtual environment using `python3 -m venv venv` from project root
1. Activate the virtual environment using `source venv/bin/activate`
1. Install required packages using `pip install -r requirements.txt`
1. Download external dependencies and resources using `python3 scripts/download_dependencies.py`
1. Install project package using `pip install -e .` at this point, you can run the application via `python src/main.py`
1. Run `pyinstaller main.spec` (There is an issue with `pyinstaller` that, it is not able to 
recognize proper venv's site package when pyinstaller is just installed to venv. To resolve
this issue, run `hash -r` or deactivate and re-activate the venv once. For more information see below)

## NOTES:
* In some cases, especially on Unix-like systems, if you install a package that provides a command-line tool (like `pyinstaller`), your shell might not recognize the new command immediately. This is because the shell's hash table of commands isn't updated until a new shell session starts. You can refresh this without deactivating your venv by running: `hash -r`

# How to run tests
1. Once you followed the steps above to set up the development environment (upto running `pip install -e .`), you can run test via `pytest` command from project root.

## TODOS:
[] resource manager
[] config loader
[] style
[] theme loader
[] font loader
[] locale loader
[] logger
[] settings dialog
[] splash screen
