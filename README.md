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
1. Run `pyinstaller main.spec`
```

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
