# Python Environment Setup (Windows)

Follow these steps to provision a compatible Python 3.11 environment before working on the project.

## 1. Install Python 3.11

Use the Microsoft Store or winget to install Python 3.11:

```powershell
winget install --exact --id Python.Python.3.11
```

Alternatively download the installer from https://www.python.org/downloads/ and ensure you enable "Add Python to PATH" during setup.

## 2. Create a Virtual Environment

From the project root:

```powershell
py -3.11 -m venv .venv
```

## 3. Activate the Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If execution policy blocks activation, run PowerShell as Administrator and execute `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` once.

## 4. Install Requirements

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

Optional Kaggle support for dataset downloads:

```powershell
pip install kaggle
```

## 5. Persist Environment Selection (VS Code)

Open the command palette (`Ctrl+Shift+P`), choose "Python: Select Interpreter", and point to `.venv`.

The project tools and scripts now run against the intended Python 3.11 runtime, avoiding incompatible wheel builds on Python 3.12+.
