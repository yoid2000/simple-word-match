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
   - The following assumes that a venv has been setup and activated
   - `sudo apt update && sudo apt install -y python3-pip git build-essential python3-setuptools python3-venv unzip openjdk-17-jdk`
   - `pip install buildozer`
   - `pip install kivy`
   - `pip install cython`
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
   - **Enable "Install from unknown sources":**
     - On your Android device, go to **Settings > Security** (or **Settings > Apps & notifications > Special app access > Install unknown apps** on newer Android versions).
     - Find your file manager or browser app (the one you'll use to open the APK) and enable "Allow from this source" or "Install unknown apps".
   - **Transfer the APK to your phone:**
     - The APK file will be in the `bin/` directory (e.g., `bin/simplewordmatch-0.1-debug.apk`).
     - You can transfer it via:
       - **USB cable:** Connect your phone to your PC, set it to "File Transfer" mode, and copy the APK to your Downloads folder.
       - **Email:** Email the APK to yourself and download it on your phone.
       - **Cloud storage:** Upload the APK to Google Drive, Dropbox, etc., and download it on your phone.
   - **Open and install the APK:**
     - Use your phone's file manager or the "Files" app to navigate to the folder where you saved the APK (usually "Downloads").
     - Tap the APK file. You may see a warning; confirm you want to install.
     - The app will install and appear in your app drawer.

#### **B. On Windows (for editing/running only):**
- You can edit and run the app locally with Python and Kivy (see above), but you cannot build an APK directly on Windows.
- To build an APK, use WSL (Windows Subsystem for Linux) or a Linux VM, and follow the Ubuntu/Linux instructions above.

---

## How to Generate a New APK After Updating the App

If you make changes to the app code (for example, edit `main.py`, `word_manager.py`, or other files), you need to generate a new APK to install the updated version on your phone:

1. **On your Ubuntu/Linux/WSL machine, open a terminal and navigate to the `kivy/` directory:**
   ```sh
   cd /path/to/your/simple-word-match/kivy
   ```
2. **Build a new APK:**
   ```sh
   buildozer -v android debug
   ```
   - This will rebuild the APK with your latest changes. The new APK will appear in the `bin/` directory.
3. **Sideload and install the new APK on your phone:**
   - Follow the instructions in the "How to Update the App on Your Phone" section below.

---

## How to Update the App on Your Phone

If you make changes to the app and build a new APK, follow these steps to update it on your Android device:

1. **(Recommended) Uninstall the old version first:**
   - Go to **Settings > Apps** (or **Apps & notifications**), find **Simple Word Match**, and tap **Uninstall**.
   - This helps avoid conflicts with debug/test builds.
2. **Transfer the new APK to your phone:**
   - Use USB, email, or cloud storage as described above.
3. **Install the new APK:**
   - Open your file manager or "Files" app.
   - Navigate to the folder where you saved the new APK (usually "Downloads").
   - Tap the APK file and confirm installation.
   - If prompted, allow installation from unknown sources.
   - The new version will replace the old one and appear in your app drawer.

---

For more help, see the [Kivy documentation](https://kivy.org/doc/stable/guide/packaging-android.html) and [Buildozer documentation](https://buildozer.readthedocs.io/en/latest/).
