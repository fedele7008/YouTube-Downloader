"""
Install necessary dependencies for the project.

Install list:
- FFmpeg
- Fonts

Supported OS: MacOS, Windows(Not supported yet, but is planned)

Run this script in virtual environment that installed all necessary python 
    packages in requirements.txt.
"""

import os, subprocess, zipfile, uuid, shutil, gdown

# Determine the operating system
current_os: str = os.uname().sysname

# Find project root
project_root: str = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

ffmpeg_output: str = "ffmpeg.zip"
ffmpeg_executable: str = "ffmpeg"
ffmpeg_download_id: str | None = None

font_dir_download_id: str = "1UqKze7zTopihuWZsVyliUleJrbiRtKzU"
font_dir_destination: str = os.path.join(project_root, "resources", "fonts")

tmp_dir: str = os.path.join(project_root, f"install_dependency_tmp_{uuid.uuid4()}")

# Supported OS: MacOS, Windows
match current_os:
    case "Darwin":
        print("Detected MacOS environment")
        ffmpeg_download_id = "1QVBsLc-eijb8L2vfZ3Fmiez_5Xxj-Zsn"
    case "Windows":
        print("Detected Windows environment (Not supported yet)")
        exit(1)
    case _:
        print("Unsupported operating system")
        exit(1)

# Assert ffmpeg_download_id is not None
if ffmpeg_download_id is None:
    print("FFmpeg download ID is not set")
    exit(1)

# Check if ffmpeg is already installed ({project_root}/external/ffmpeg/bin/)
ffmpeg_dir: str = os.path.join(project_root, "external", "ffmpeg", "bin")
if not os.path.isfile(os.path.join(ffmpeg_dir, ffmpeg_executable)):
    print(f"FFmpeg not found at {ffmpeg_dir}, downloading...")

    # Create ffmpeg directory
    os.makedirs(ffmpeg_dir, exist_ok=True)

    gdown.download(id=ffmpeg_download_id, output=os.path.join(ffmpeg_dir, ffmpeg_output), quiet=False)
    print(f"FFmpeg downloaded to {ffmpeg_dir}")

    # Unzip ffmpeg
    with zipfile.ZipFile(os.path.join(ffmpeg_dir, ffmpeg_output), "r") as zip_ref:
        zip_ref.extractall(ffmpeg_dir)
    print(f"FFmpeg unzipped to {ffmpeg_dir}")

    # Remove the zip file
    os.remove(os.path.join(ffmpeg_dir, ffmpeg_output))
    print(f"FFmpeg zip file removed")

    # Make ffmpeg executable
    print(f"Making FFmpeg executable")
    os.chmod(os.path.join(ffmpeg_dir, ffmpeg_executable), 0o755)
else:
    print(f"FFmpeg already installed at {ffmpeg_dir}")

    # Check if ffmpeg is executable
    if not os.access(os.path.join(ffmpeg_dir, ffmpeg_executable), os.X_OK):
        print(f"FFmpeg executable is not executable, making it executable")
        os.chmod(os.path.join(ffmpeg_dir, ffmpeg_executable), 0o755)

# Check if ffmpeg is working
result = subprocess.run([os.path.join(ffmpeg_dir, ffmpeg_executable), "-version"], capture_output=True, text=True)
if result.returncode != 0:
    print(f"FFmpeg executable is not working: {result.returncode}")
    match current_os:
        case "Darwin":
            # Remove quarantine attribute
            print(f"Removing quarantine attribute")
            subprocess.run(["xattr", "-d", "com.apple.quarantine", os.path.join(ffmpeg_dir, ffmpeg_executable)])

            # Re-check if ffmpeg is working
            result = subprocess.run([os.path.join(ffmpeg_dir, ffmpeg_executable), "-version"], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"FFmpeg executable is still not working, please check your installation")
                exit(1)

            print(f"FFmpeg installed version: {result.stdout}")
        case "Windows":
            print("Windows is not supported yet")
            exit(1)
        case _:
            print("Unsupported operating system")
            exit(1)

# Parse ffmpeg version
ffmpeg_version: str = result.stdout.split("\n")[0].split(" ")[2]
print(f"FFmpeg installed version: {ffmpeg_version}")

# Download fonts from Google Drive
os.makedirs(tmp_dir, exist_ok=True)
print(f"Downloading fonts to {tmp_dir}")
gdown.download_folder(id=font_dir_download_id, output=tmp_dir, quiet=False)

# Unzip fonts
for font_zip in os.listdir(tmp_dir):
    print(f"Unzipping {font_zip}")
    with zipfile.ZipFile(os.path.join(tmp_dir, font_zip), "r") as zip_ref:
        zip_ref.extractall(font_dir_destination)
    print(f"Unzipped {font_zip}")

# Remove __MACOSX directory
if os.path.exists(os.path.join(font_dir_destination, "__MACOSX")):
    shutil.rmtree(os.path.join(font_dir_destination, "__MACOSX"))
    print(f"Removed __MACOSX directory")

print(f"All fonts downloaded to {font_dir_destination}")

# Remove tmp_dir
shutil.rmtree(tmp_dir)
print(f"Temporary directory removed: {tmp_dir}")
