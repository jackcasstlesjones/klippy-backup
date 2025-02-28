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

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/klippy.git

# Make the script executable
chmod +x klippy

# Optional: Install Rich for enhanced UI
pip install rich
```

### Installing as a CLI Tool

Method 1: Using ~/.local/bin

```bash
# Clone the repository into ~/.local/bin/klippy
git clone https://github.com/yourusername/klippy.git ~/.local/bin/klippy

# Navigate to the directory
cd ~/.local/bin/klippy

# Ensure the main script is executable
chmod +x klippy

# Add the directory to your PATH by appending this line to your shell config file
echo 'export PATH="$HOME/.local/bin/klippy:$PATH"' >> ~/.zshrc
# Or for bash users:
# echo 'export PATH="$HOME/.local/bin/klippy:$PATH"' >> ~/.bashrc

# Apply changes to current session
source ~/.zshrc
# Or for bash users:
# source ~/.bashrc
```

Method 2: Using a symlink

```bash
# Clone the repository
git clone https://github.com/yourusername/klippy.git ~/.local/bin/klippy

# Make the script executable
chmod +x ~/.local/bin/klippy/klippy

# Create a symlink to make klippy available system-wide
ln -s ~/.local/bin/klippy/klippy /usr/local/bin/klippy
```

## Usage

```bash
# Configure Klippy settings
./klippy --config

# Process clippings without deleting the source file
./klippy --add

# Process clippings and delete the source file
./klippy --sync

# Delete clippings file without processing
./klippy --delete
```

## How It Works

1. Connect your Kindle device to your computer
2. Run Klippy with your preferred command
3. Klippy extracts highlights from "My Clippings.txt"
4. Highlights are organized by book into separate Markdown files
5. A Map of Content (MOC) file links all your books together

## License

This project is available under the MIT License.
