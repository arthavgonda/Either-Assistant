# Installation Guide

Complete installation instructions for EitherAssistant on Windows, macOS, and Linux.

## 📥 Quick Download Links

<table>
<tr>
<td align="center" width="33%">

### 🪟 Windows
[![Download](https://img.shields.io/badge/Download-EitherAssistant.exe-blue?style=for-the-badge)](FinalApp/EitherAssistant.exe)

`EitherAssistant.exe`

</td>
<td align="center" width="33%">

### 🍎 macOS
[![Download](https://img.shields.io/badge/Download-EitherAssistant.app-purple?style=for-the-badge)](FinalApp/EitherAssistant.app)

`EitherAssistant.app`

</td>
<td align="center" width="33%">

### 🐧 Linux
[![Download](https://img.shields.io/badge/Download-Linux%20Package-orange?style=for-the-badge)](FinalApp/EitherAssistant-1.0.0-Linux.deb)

`EitherAssistant-1.0.0-Linux.deb`

</td>
</tr>
</table>

---

## 📦 Option 1: Pre-built Binaries (Recommended)

### Windows

#### Download

**Direct Download:**
- Download: [`EitherAssistant.exe`](FinalApp/EitherAssistant.exe)

**From Repository:**
1. Go to the repository `FinalApp/` directory
2. Click on `EitherAssistant.exe`
3. Click "Download" or "Download raw file"
4. Save the file to your desired location (e.g., `Downloads` folder)

#### Installation
1. Double-click `EitherAssistant.exe` to run
2. No installation required - runs directly
3. First launch will automatically start the Python backend

#### Requirements
- Windows 10 or later (64-bit)
- Microphone access permissions
- Administrator rights (for system operations)

---

### macOS

#### Download

**Direct Download:**
- Download: [`EitherAssistant.app`](FinalApp/EitherAssistant.app) (if available)

**From Repository:**
1. Go to the repository `FinalApp/` directory
2. Click on `EitherAssistant.app` or download the `.dmg` file
3. Click "Download" to save the application bundle
4. If downloading as `.zip`, extract the archive first

#### Installation
1. Open the downloaded `.app` file
2. If macOS blocks the app, go to System Preferences → Security & Privacy
3. Click "Open Anyway" to allow the application
4. Drag `EitherAssistant.app` to Applications folder (optional)

#### Requirements
- macOS 10.15 (Catalina) or later
- Intel or Apple Silicon (M1/M2) Mac
- Microphone access permissions

#### First Launch
1. Right-click the app and select "Open"
2. Confirm security prompt if shown
3. Application will start automatically

---

### Linux

#### Download Options

**Option A: Debian Package (.deb)**

**Direct Download:**
- Download: [`EitherAssistant-1.0.0-Linux.deb`](FinalApp/EitherAssistant-1.0.0-Linux.deb)

**From Repository:**
1. Go to the repository `FinalApp/` directory
2. Click on `EitherAssistant-1.0.0-Linux.deb`
3. Click "Download" to save the package file

**Option B: AppImage**

**Direct Download:**
- Download: [`EitherAssistant-1.0.0-x86_64.AppImage`](FinalApp/EitherAssistant-1.0.0-x86_64.AppImage) (if available)

**From Repository:**
1. Go to the repository `FinalApp/` directory
2. Click on `EitherAssistant-1.0.0-x86_64.AppImage`
3. Click "Download" to save the AppImage file

#### Installation - Debian Package

```bash
cd ~/Downloads
sudo dpkg -i EitherAssistant-1.0.0-Linux.deb
```

If dependencies are missing:
```bash
sudo apt-get install -f
```

Launch from applications menu or terminal:
```bash
EitherAssistant
```

#### Installation - AppImage

```bash
cd ~/Downloads
chmod +x EitherAssistant-1.0.0-x86_64.AppImage
./EitherAssistant-1.0.0-x86_64.AppImage
```

To make it available system-wide:
```bash
sudo mv EitherAssistant-1.0.0-x86_64.AppImage /usr/local/bin/EitherAssistant
sudo chmod +x /usr/local/bin/EitherAssistant
```

#### Requirements
- Ubuntu 20.04+ or equivalent Linux distribution
- 64-bit architecture
- Microphone access permissions
- PortAudio library (usually pre-installed)

#### Install PortAudio (if needed)
```bash
sudo apt update
sudo apt install portaudio19-dev python3-dev
```

---

## 🔧 Option 2: Build from Source

### Prerequisites

#### Windows

**Install .NET 8.0 SDK:**
1. Download from [Microsoft .NET website](https://dotnet.microsoft.com/download)
2. Run the installer
3. Verify installation:
```powershell
dotnet --version
```

**Install Python 3.8+:**
1. Download from [Python website](https://www.python.org/downloads/)
2. Check "Add Python to PATH" during installation
3. Verify installation:
```powershell
python --version
```

**Install Visual C++ Build Tools:**
- Required for some Python packages
- Download from [Microsoft Visual Studio](https://visualstudio.microsoft.com/downloads/)

#### macOS

**Install .NET 8.0 SDK:**
```bash
brew install --cask dotnet-sdk
```

**Install Python 3.8+:**
```bash
brew install python@3.8
```

**Install PortAudio:**
```bash
brew install portaudio
```

#### Linux

**Install .NET 8.0 SDK:**
```bash
wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y dotnet-sdk-8.0
```

**Install Python 3.8+:**
```bash
sudo apt update
sudo apt install python3.8 python3.8-venv python3.8-pip
```

**Install PortAudio:**
```bash
sudo apt install portaudio19-dev python3-dev
```

---

### Frontend Build Instructions

#### Windows
```powershell
cd EitherAssistant
dotnet restore
dotnet build
dotnet publish -c Release -r win-x64 --self-contained true
```

Output location: `EitherAssistant/bin/Release/net8.0/win-x64/publish/`

#### macOS
```bash
cd EitherAssistant
dotnet restore
dotnet build
dotnet publish -c Release -r osx-x64 --self-contained true
```

For Apple Silicon (M1/M2):
```bash
dotnet publish -c Release -r osx-arm64 --self-contained true
```

Output location: `EitherAssistant/bin/Release/net8.0/osx-x64/publish/`

#### Linux
```bash
cd EitherAssistant
dotnet restore
dotnet build
dotnet publish -c Release -r linux-x64 --self-contained true
```

Output location: `EitherAssistant/bin/Release/net8.0/linux-x64/publish/`

---

### Backend Setup Instructions

#### All Operating Systems

**Step 1: Navigate to Python directory**
```bash
cd Python
```

**Step 2: Create virtual environment**

Windows:
```powershell
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install torch
```

**Step 4: Download Vosk Model (Offline STT)**

1. Visit [Vosk Models](https://alphacephei.com/vosk/models)
2. Download `vosk-model-en-us-0.22` (or preferred language model)
3. Extract to `Python/STT/vosk-model-en-us-0.22/`

**Step 5: Start the backend server**
```bash
python api_server.py
```

Server will start on `http://localhost:8000`

---

## 🚀 Running the Application

### First Time Setup

1. **Start Backend Server**
   - Navigate to `Python/` directory
   - Activate virtual environment
   - Run `python api_server.py`
   - Wait for "System initialization complete" message

2. **Start Frontend Application**

   **Pre-built:**
   - Windows: Double-click `EitherAssistant.exe`
   - macOS: Open `EitherAssistant.app`
   - Linux: Run `EitherAssistant` or AppImage

   **From Source:**
   ```bash
   cd EitherAssistant
   dotnet run
   ```

3. **Initial Calibration**
   - Backend will prompt for noise calibration
   - Remain silent for 3 seconds
   - System will learn background noise levels

4. **Browser Setup (Optional)**
   - Choose whether to enable browser automation
   - System works without browser for file/system operations

---

## ✅ Verification

### Check Backend Status
Open browser and visit: `http://localhost:8000/status`

Expected response:
```json
{
  "status": "online",
  "voice_listening": false,
  "browser_enabled": false,
  "system_controller": true
}
```

### Check API Documentation
Visit: `http://localhost:8000/docs`

### Test Voice Recognition
1. Click microphone button in frontend
2. Speak a command
3. Check if transcription appears in the UI

---

## 🔧 Configuration

### Backend Configuration

Create `.env` file in `Python/` directory:
```bash
API_HOST=0.0.0.0
API_PORT=8000
STT_METHOD=vosk
BROWSER_HEADLESS=false
```

### Frontend Configuration

Settings are stored in user application data:
- Windows: `%APPDATA%\EitherAssistant\`
- macOS: `~/Library/Application Support/EitherAssistant/`
- Linux: `~/.config/EitherAssistant/`

---

## 🐛 Troubleshooting Installation

### Windows Issues

**"Python not found"**
- Add Python to PATH during installation
- Restart terminal after installation

**"dotnet command not found"**
- Restart terminal after .NET SDK installation
- Verify with `dotnet --version`

**Permission errors**
- Run terminal as Administrator
- Check antivirus isn't blocking execution

### macOS Issues

**"App is damaged"**
- Remove quarantine: `xattr -cr EitherAssistant.app`
- Or: System Preferences → Security → Allow app

**"Command not found: python3"**
- Install via Homebrew: `brew install python@3.8`
- Use `python3` instead of `python`

### Linux Issues

**"PortAudio not found"**
```bash
sudo apt install portaudio19-dev
```

**"Permission denied" (AppImage)**
```bash
chmod +x EitherAssistant-1.0.0-x86_64.AppImage
```

**"Dependencies missing" (.deb)**
```bash
sudo apt-get install -f
```

**Browser not detected**
```bash
sudo apt install chromium-browser firefox
```

---


