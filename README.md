# How to Build for Windows

Since this app uses Python, you can package it into a single `.exe` file that runs on any Windows machine without needing Python installed.

## Prerequisites
You need to be on a **Windows** computer to build the standard Windows executable.

## Steps

### 1. Install Python
If you haven't already, install Python from [python.org](https://www.python.org/downloads/).
- **Important**: Check the box **"Add Python to PATH"** during installation.

### 2. Open Command Prompt (cmd)
Open your terminal or command prompt and navigate to the folder with `main.py`.

### 3. Install Dependencies
Run the following command to install the necessary libraries:
```bash
pip install -r requirements.txt
```

### 4. Build the Executable
Run PyInstaller to create the standalone file:
```bash
pyinstaller --onefile --noconsole main.py
```
- `--onefile`: Bundles everything into a single .exe
- `--noconsole`: Hides the black terminal window when running the app

### 5. Locate your App
After the build finishes, check the **`dist`** folder.
- You will find `main.exe` there. This is your standalone application.
- You can rename it to `ZipcodeCleaner.exe` and move it anywhere.

## Troubleshooting
- If Windows Defender complains, it's a common false positive with PyInstaller. You may need to add an exclusion or sign the executable (advanced).
