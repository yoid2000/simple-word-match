# Simple Word Match (Kivy)

This is a Kivy-based version of the Simple Word Match app for Android. It does not require the Play Store and is for personal use only.

## Features
- Two columns: English and German words
- Tap to select an English word, then a German word to match
- Immediate feedback (color change)
- "Next" button to load new words


## How to Test Locally in VS Code (Before Building APK)

1. **Install Python 3** (if not already installed).
2. **Install Kivy:**
   - Open a terminal in the `kivy/` directory.
   - Run: `pip install kivy`
3. **Run the app:**
   - In the terminal, run: `python main.py`
   - The Kivy app window should open on your desktop.
4. **Test all features:**
   - Try matching words, double-clicking to mark as frequent, and using the "Next" button.

---

## How to Install on Android (No App Store)

### 1. Easiest: Run with Pydroid 3 (No APK Build Needed)
- Copy `main.py`, `word_manager.py`, and `translations.json` to your phone
- Install [Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3) from the Play Store
- Open Pydroid 3, open `main.py`, and run it

### 2. Build APK with Buildozer (Requires Ubuntu/Linux or WSL)

> **Note:** APK building with Buildozer must be done on Ubuntu/Linux, or on Windows using [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/) or a Linux virtual machine. You cannot build an APK natively on Windows.

#### **A. On Ubuntu/Linux/WSL:**

1. **Install dependencies:**
   - `sudo apt update && sudo apt install -y python3-pip git build-essential python3-setuptools python3-venv unzip openjdk-17-jdk`
   - `pip install --user buildozer`
   - `pip install kivy`
2. **Clone or copy this `kivy/` directory to your Ubuntu/WSL/Linux system.**
3. **Initialize Buildozer:**
   - `cd kivy`
   - `buildozer init`
   - Edit `buildozer.spec`:
     - Set `source.include_exts = py,json`
     - Set `requirements = python3,kivy`
     - Set `package.domain = org.yourname.simplewordmatch`
   - Make sure all files (`main.py`, `word_manager.py`, `translations.json`) are in this directory.
4. **Build the APK:**
   - `buildozer -v android debug`
   - The APK will be in the `bin/` directory.
5. **Sideload the APK to your phone:**
   - Enable "Install from unknown sources" on your phone
   - Transfer the APK to your phone and open it to install

#### **B. On Windows (for editing/running only):**
- You can edit and run the app locally with Python and Kivy (see above), but you cannot build an APK directly on Windows.
- To build an APK, use WSL (Windows Subsystem for Linux) or a Linux VM, and follow the Ubuntu/Linux instructions above.

---

For more help, see the [Kivy documentation](https://kivy.org/doc/stable/guide/packaging-android.html) and [Buildozer documentation](https://buildozer.readthedocs.io/en/latest/).
