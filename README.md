# 📋 Task Manager (PyQt6)

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-brightgreen.svg)
![OS](https://img.shields.io/badge/OS-Linux-orange.svg)

A clean, modern system monitor and process manager built with Python and PyQt6. Easily monitor live CPU, RAM, disk, and network stats, inspect active processes, and manage system resources—all in a lightweight, standalone desktop application.

---

## ✨ Features

* 📊 **Real-Time System Monitoring:** Track live **CPU**, **RAM**, **Disk**, and **Network** usage statistics at a glance.
* ⚙️ **Active Process Inspection:** View all running system processes along with detailed resource consumption (CPU & Memory usage per process).
* 🛑 **Process Manager:** Terminate or kill any unresponsive or resource-heavy process directly from the app.
* 🎨 **Modern PyQt6 Interface:** Clean, fast, and lightweight desktop GUI built for Linux.
* ⚡ **Zero Setup Required:** Download and run—no local Python or dependencies setup needed for end-users!

<img width="1190" height="740" alt="image" src="https://github.com/user-attachments/assets/4a5b7dcf-dac2-4479-a647-0d9bcdd498ff" />


---

## 📥 Download & Installation (Linux)

You don't need Python installed to run this application! Follow the steps below to download and run the pre-built binary.

### Option 1: Quick Setup (Recommended)

1. Go to the **[Releases](../../releases)** page on this repository.
2. Under **Assets**, download **`task_manager-v1.0.0-linux.tar.gz`**.
3. Open your terminal in your `Downloads` folder and run:

```bash
# Navigate to Downloads
cd ~/Downloads

# Extract the archive
tar -xvf main-v1.0.0-linux.tar.gz

# Grant execution permissions
chmod +x main

# Launch the application
./main
