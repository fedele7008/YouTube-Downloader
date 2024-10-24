# YouTube-Downloader
YouTube Video Downloading GUI Application

### Supported Platforms
| Platform | Status |
| --- | --- |
| MacOS Apple Silicon | Tested |
| MacOS Intel | Planned to support but Not tested yet |
| Windows ARM64 | Tested |
| Windows x64 | Planned to support but Not tested yet |
| Windows x32/x86 | Not planned to support |
| Linux | Not planned to support |

## How to setup development environment (MacOS: Apple Silicon / Intel)
1. Make sure you are using python3.12 version as some dependencies are not compatible with 3.13 yet (10/21/2024)
1. Open terminal and go to project root `cd /path/to/project/root`
1. Install `virtualenv` using `python3 -m pip install virtualenv`
1. Create a virtual environment using `python3 -m venv venv`
1. Activate the virtual environment using `source venv/bin/activate`
1. Install required packages using `pip install -r requirements.txt`
1. Download external dependencies and resources using `python3 scripts/download_dependencies.py`
1. Install project package using `pip install -e .`
1. Now you can run the application via `python3 src/main.py`

Important Notes:
* You may find config folder for youtube-downloader in `/Users/<YourUsername>/Library/Application Support`.
The config folder is named `youtube_downloader`.

## How to setup development environment (Windows: ARM64)
1. Install `python3.12` from Microsoft Store (Recommended)
1. Open PowerShell and go to project root `cd /path/to/project/root`
1. Install `virtualenv` using `python3 -m pip install virtualenv`
1. Create a virtual environment using `python3 -m venv venv`
1. Activate the virtual environment using `.\venv\Scripts\activate`
1. Install required packages using `pip install -r requirements.txt`
1. Download external dependencies and resources using `python3 .\scripts\download_dependencies.py`
1. Install project package using `pip install -e .`
1. Now you can run the application via `python3 .\src\main.py`

Important Notes:
* Using python installed from Microsoft Store is recommended because there are some pip install issue
with `pycryptodome` package in local ARM64 environment.
* If you are using python installed from Microsoft Store, you might not be able to find config folder for
youtube-downloader in your normal %APPDATA% directory. This is because this python version is using
isolated environment. To go to config folder follow these steps:
    1. Open PowerShell and run `Get-AppxPackage | Where-Object { $_.Name -like "*Python*" }`
    1. In `PackageFamilyName` row, you will see something like `PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0`
    1. Copy this string and go to `C:\Users\<YourUsername>\AppData\Local\Packages\`
    1. Find the folder that matches the `PackageFamilyName` string and go into it.
    1. Inside, you will see `LocalCache` folder. go into it.
    1. Inside, you will see `Roaming` folder. go into it.
    1. This is where configuration folder for youtube-downloader (`youtube_downloader`) will be located. (when you run through `python3 .\src\main.py`)
* If you are running the application through distributed executable, config folder will located in the
normal %APPDATA% directory of the user. 

## How to setup development environment (Windows: x64)
> TODO: Not tested yet

## How to distribute application (MacOS / Windows)
1. If you are on MacOS, run `hash -r` or deactivate and re-activate the venv once. (Do this only once after pip installing requirements packages)
1. Run `pyinstaller main.spec` from project root.
1. You will find the distributable in `dist` folder.

Important Notes:
* In some cases, especially on Unix-like systems, if you install a package that provides a command-line tool (like `pyinstaller`), your shell might not recognize the new command immediately. This is because the shell's hash table of commands isn't updated until a new shell session starts. You can refresh this without deactivating your venv by running: `hash -r`

# How to run tests
1. Once you followed the steps above to set up the development environment (upto running `pip install -e .`), you can run test via `pytest` command from project root.

## TODOS:
- [ ] style
- [ ] settings dialog
