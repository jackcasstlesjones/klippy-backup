# Klippy

A sleek, efficient tool for converting Kindle highlights to Markdown files for Obsidian.

## Overview

Klippy extracts your Kindle highlights and notes, organizing them into neatly formatted Markdown files that integrate seamlessly with Obsidian or other Markdown-based note-taking systems.

## Features

- **Automatic Extraction**: Reads directly from your Kindle device
- **Markdown Conversion**: Transforms highlights into formatted Markdown
- **Obsidian Integration**: Creates backlinks and a Map of Content (MOC)
- **Rich UI**: Enhanced experience with progress indicators and colorful output (when Rich is installed)
- **Flexible Configuration**: Customizable output directory and formatting options

## Installation

> **NOTE:** Backup your existing configuration (if any exists)

### Install Klippy

#### Recommended Step

Fork this repo so that you have your own copy that you can modify, then install by cloning the fork to your machine using one of the commands below.

> **NOTE:** Your fork's URL will be something like this: `https://github.com/<your_github_username>/klippy.git`

#### Clone Klippy Repository

**Linux and Mac**

```bash
# Clone the repository
git clone https://github.com/yourusername/klippy.git ~/.config/klippy

# Make the script executable
chmod +x ~/.config/klippy/klippy

# Optional: Install Rich for enhanced UI
pip install rich
```

### Make Klippy Available System-wide

**Method 1: Add to PATH (Linux/Mac)**

```bash
# Add the directory to your PATH by appending this line to your shell config file
echo 'export PATH="$HOME/.config/klippy:$PATH"' >> ~/.zshrc
# Or for bash users:
# echo 'export PATH="$HOME/.config/klippy:$PATH"' >> ~/.bashrc

# Apply changes to current session
source ~/.zshrc
# Or for bash users:
# source ~/.bashrc
```

**Method 2: Create a Symlink (Linux/Mac)**

```bash
# Create a symlink to make klippy available system-wide
sudo ln -s ~/.config/klippy/klippy /usr/local/bin/klippy
```

## Usage

Start Klippy with one of the following commands:

```bash
# Configure Klippy settings
klippy --config

# Process clippings without deleting the source file
klippy --add

# Process clippings and delete the source file
klippy --sync

# Delete clippings file without processing
klippy --delete
```

## How It Works

1. Connect your Kindle device to your computer
2. Run Klippy with your preferred command
3. Klippy extracts highlights from "My Clippings.txt"
4. Highlights are organized by book into separate Markdown files
5. A Map of Content (MOC) file links all your books together

## License

This project is available under the MIT License.
