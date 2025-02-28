#!/usr/bin/env python3

import re
import os
import json
import argparse
import shutil
import time
from datetime import datetime
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("For a better experience, install rich: pip install rich")

# Initialize rich console if available
console = Console() if RICH_AVAILABLE else None

# Define default paths and settings
CONFIG_DIR = os.path.expanduser('~/.config/klippy')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')
OLD_CONFIG_FILE = os.path.expanduser('~/.klippy_config.json')
print(f"Config file path: {CONFIG_FILE}")
DEFAULT_CONFIG = {
    'device_name': 'Kindle',
    'dest_dir': os.path.expanduser('~/obsidian/jacks-vault/clippings'),
    'create_moc': True,
    'moc_filename': 'moc-clippings'  # Without .md extension for consistency with link format
}

# Load configuration
def load_config():
    if RICH_AVAILABLE:
        with console.status("[bold green]Loading configuration...", spinner="dots"):
            time.sleep(0.5)  # Small delay for visual effect
            return _load_config()
    else:
        return _load_config()

def _load_config():
    print(f"Loading config from: {CONFIG_FILE}")
    
    # Check if we need to migrate from old location
    if not os.path.exists(CONFIG_FILE) and os.path.exists(OLD_CONFIG_FILE):
        try:
            if RICH_AVAILABLE:
                console.print(f"[yellow]Migrating config from old location:[/yellow] {OLD_CONFIG_FILE}")
            else:
                print(f"Migrating config from old location: {OLD_CONFIG_FILE}")
                
            # Ensure the config directory exists
            os.makedirs(CONFIG_DIR, exist_ok=True)
            
            # Read old config
            with open(OLD_CONFIG_FILE, 'r') as old_f:
                old_config = json.load(old_f)
            
            # Write to new location
            with open(CONFIG_FILE, 'w') as new_f:
                json.dump(old_config, new_f, indent=4, sort_keys=True)
            
            if RICH_AVAILABLE:
                console.print(f"[green]Successfully migrated config to:[/green] {CONFIG_FILE}")
            else:
                print(f"Successfully migrated config to: {CONFIG_FILE}")
        except Exception as e:
            if RICH_AVAILABLE:
                console.print(f"[bold red]Error migrating config:[/bold red] {str(e)}")
            else:
                print(f"Error migrating config: {str(e)}")
    
    # Now load from the new location
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                user_config = json.load(f)
                if RICH_AVAILABLE:
                    console.print("[green]Configuration loaded successfully[/green]")
                else:
                    print(f"Loaded config: {user_config}")
                return user_config
        except json.JSONDecodeError:
            if RICH_AVAILABLE:
                console.print("[bold red]Error reading config file. Using empty configuration.[/bold red]")
            else:
                print(f"Error reading config file. Using empty configuration.")
            return {}
    else:
        if RICH_AVAILABLE:
            console.print("[yellow]Config file does not exist yet. Will be created when saving.[/yellow]")
        else:
            print(f"Config file does not exist yet. Will be created when saving.")
    return {}

# Save configuration
def save_config(config):
    # Ensure we're only saving valid config keys
    valid_config = {k: config[k] for k in DEFAULT_CONFIG.keys() if k in config}
    
    if RICH_AVAILABLE:
        with console.status("[bold green]Saving configuration...", spinner="dots"):
            time.sleep(0.5)  # Small delay for visual effect
            result = _save_config(valid_config)
            if result:
                console.print("[bold green]✓[/bold green] Configuration saved successfully")
            else:
                console.print("[bold red]✗[/bold red] Failed to save configuration")
            return result
    else:
        return _save_config(valid_config)

def _save_config(valid_config):
    print(f"Saving configuration: {valid_config}")
    print(f"Writing to file: {CONFIG_FILE}")
    
    # Ensure the config directory exists
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    # Debug: Check if file exists and is writable
    if os.path.exists(CONFIG_FILE):
        print(f"File exists. Current permissions: {oct(os.stat(CONFIG_FILE).st_mode)}")
    
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(valid_config, f, indent=4, sort_keys=True)
            f.flush()
            os.fsync(f.fileno())  # Force write to disk
        print(f"Configuration saved to {CONFIG_FILE}")
        
        # Verify the file was actually written
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                saved_config = json.load(f)
            print(f"Verification - File contains: {saved_config}")
            return True
        else:
            print(f"ERROR: File does not exist after save!")
            return False
    except Exception as e:
        print(f"ERROR saving configuration: {str(e)}")
        return False

# Setup configuration interactively
def setup_config():
    config = load_config()
    
    if RICH_AVAILABLE:
        console.print(Panel.fit(
            "[bold blue]Klippy Configuration Setup[/bold blue]",
            border_style="blue"
        ))
        
        # Only show the current config values in the prompt, no defaults
        device_name = Prompt.ask(
            "Enter device name", 
            default=config.get('device_name', ''),
            show_default=True
        )
        config['device_name'] = device_name
        
        # Keep asking for a valid destination directory
        valid_dest_dir = False
        while not valid_dest_dir:
            dest_dir = Prompt.ask(
                "Enter destination directory, using a full filepath e.g ~/obsidian/my-vault/clippings", 
                default=config.get('dest_dir', ''),
                show_default=True
            )
            if dest_dir:
                # Validate that the path contains at least one directory separator
                if '/' not in dest_dir and '\\' not in dest_dir and not dest_dir.startswith('~'):
                    console.print("[bold red]Error:[/bold red] Please enter a full path with at least one directory separator (/ or \\).")
                    print(f"Examples: ~/Documents/clippings, /Users/username/Documents, C:\\Users\\username\\Documents")
                    continue
                
                # If the path is relative (doesn't start with / or ~), make it absolute
                if not dest_dir.startswith('/') and not dest_dir.startswith('~'):
                    dest_dir = os.path.abspath(dest_dir)
                
                expanded_path = os.path.expanduser(dest_dir)
                
                # Check if the directory exists or can be created
                try:
                    # Try to create the directory if it doesn't exist
                    os.makedirs(expanded_path, exist_ok=True)
                    config['dest_dir'] = expanded_path
                    valid_dest_dir = True
                except (OSError, PermissionError) as e:
                    console.print(f"[bold red]Error:[/bold red] Invalid directory path: {e}")
                    console.print("Please enter a valid directory path.")
            else:
                # If they didn't enter anything, use the existing value if it exists
                if config.get('dest_dir'):
                    valid_dest_dir = True
                else:
                    console.print("[bold red]Error:[/bold red] You must enter a valid destination directory.")
        
        create_moc = Confirm.ask(
            "Do you want to create a Map of Content (MOC) file for your clippings?",
            default=config.get('create_moc', True)
        )
        config['create_moc'] = create_moc
        
        if create_moc:
            moc_filename = Prompt.ask(
                "Enter MOC filename (without extension)", 
                default=config.get('moc_filename', ''),
                show_default=True
            )
            config['moc_filename'] = moc_filename
    else:
        print("Klippy Configuration Setup")
        print("=========================")
        
        # Only show the current config values in the prompt, no defaults
        device_name = input(f"Enter device name [{config.get('device_name', '')}]: ")
        # Always update the config, even if the user just pressed Enter (use the current value)
        config['device_name'] = device_name if device_name else config.get('device_name', '')
        
        # Keep asking for a valid destination directory
        valid_dest_dir = False
        while not valid_dest_dir:
            dest_dir = input(f"Enter destination directory [{config.get('dest_dir', '')}]: ")
            if dest_dir:
                # Validate that the path contains at least one directory separator
                if '/' not in dest_dir and '\\' not in dest_dir and not dest_dir.startswith('~'):
                    print("Error: Please enter a full path with at least one directory separator (/ or \\).")
                    print("Examples: ~/Documents/clippings, /Users/username/Documents, C:\\Users\\username\\Documents")
                    continue
                
                # If the path is relative (doesn't start with / or ~), make it absolute
                if not dest_dir.startswith('/') and not dest_dir.startswith('~'):
                    dest_dir = os.path.abspath(dest_dir)
                
                expanded_path = os.path.expanduser(dest_dir)
                
                # Check if the directory exists or can be created
                try:
                    # Try to create the directory if it doesn't exist
                    os.makedirs(expanded_path, exist_ok=True)
                    config['dest_dir'] = expanded_path
                    valid_dest_dir = True
                except (OSError, PermissionError) as e:
                    print(f"Error: Invalid directory path: {e}")
                    print("Please enter a valid directory path.")
            else:
                # If they didn't enter anything, use the existing value if it exists
                if config.get('dest_dir'):
                    valid_dest_dir = True
                else:
                    print("Error: You must enter a valid destination directory.")
        
        create_moc_input = input(f"Do you want to create a Map of Content (MOC) file for your clippings? (y/n) [{config.get('create_moc', True) and 'y' or 'n'}]: ").lower()
        create_moc = create_moc_input.startswith('y') if create_moc_input else config.get('create_moc', True)
        config['create_moc'] = create_moc
        
        if create_moc:
            moc_filename = input(f"Enter MOC filename (without extension) [{config.get('moc_filename', '')}]: ")
            # Always update the config, even if the user just pressed Enter (use the current value)
            config['moc_filename'] = moc_filename if moc_filename else config.get('moc_filename', '')
    
    save_config(config)
    return config

# Get clippings file path based on device name
def get_clippings_file_path(device_name):
    return os.path.expanduser(f'~/../../Volumes/{device_name}/documents/My Clippings.txt')

# Ensure destination directory exists
def ensure_dest_dir(dest_dir):
    os.makedirs(dest_dir, exist_ok=True)

# Read the content of the clippings.txt file
def read_clippings(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()

# Parse the clippings into a structured format
def parse_clippings(content):
    clippings = {}
    entries = content.split('==========')
    
    total_entries = len(entries)
    processed_entries = 0
    
    if RICH_AVAILABLE:
        console.print(f"[green]Parsing [bold]{total_entries}[/bold] entries...[/green]")
        
        for entry in entries:
            processed_entries += 1
            if processed_entries % 100 == 0:  # Show progress every 100 entries
                console.print(f"[green]Processed [bold]{processed_entries}/{total_entries}[/bold] entries...[/green]")
            
            entry = entry.strip()
            if not entry:
                continue

            lines = entry.split('\n')
            if len(lines) < 3:
                continue

            book_line = lines[0].strip().lstrip("\ufeff")  # Strip BOM if present
            location_line = lines[1].strip() if len(lines) > 1 else ""
            quote = '\n'.join(lines[2:]).strip() if len(lines) > 2 else ""

            # Extract book title and author
            book_match = re.search(r'^(.*?)(?:\((.*?)\))?$', book_line)
            if book_match:
                book_title = book_match.group(1).strip()
                page_number = ""

                # Extract page or location number
                page_match = re.search(r'page (\d+)', location_line)
                if page_match:
                    page_number = page_match.group(1)
                else:
                    loc_match = re.search(r'location (\d+)', location_line)
                    if loc_match:
                        page_number = f"loc {loc_match.group(1)}"

                # Skip entries with title "Your Clippings" as these are metadata
                if book_title and quote and book_title.strip() != "Your Clippings":
                    # Ensure each book has a unique set of quotes
                    if book_title not in clippings:
                        clippings[book_title] = set()

                    clippings[book_title].add((page_number, quote))
    else:
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue

            lines = entry.split('\n')
            if len(lines) < 3:
                continue

            book_line = lines[0].strip().lstrip("\ufeff")  # Strip BOM if present
            location_line = lines[1].strip() if len(lines) > 1 else ""
            quote = '\n'.join(lines[2:]).strip() if len(lines) > 2 else ""

            # Extract book title and author
            book_match = re.search(r'^(.*?)(?:\((.*?)\))?$', book_line)
            if book_match:
                book_title = book_match.group(1).strip()
                page_number = ""

                # Extract page or location number
                page_match = re.search(r'page (\d+)', location_line)
                if page_match:
                    page_number = page_match.group(1)
                else:
                    loc_match = re.search(r'location (\d+)', location_line)
                    if loc_match:
                        page_number = f"loc {loc_match.group(1)}"

                # Skip entries with title "Your Clippings" as these are metadata
                if book_title and quote and book_title.strip() != "Your Clippings":
                    # Ensure each book has a unique set of quotes
                    if book_title not in clippings:
                        clippings[book_title] = set()

                    clippings[book_title].add((page_number, quote))

    total_clippings = sum(len(qs) for qs in clippings.values())
    if RICH_AVAILABLE:
        console.print(f"[green]Found [bold]{total_clippings}[/bold] unique clippings across [bold]{len(clippings)}[/bold] books.[/green]")
    else:
        print(f"Found {total_clippings} unique clippings across {len(clippings)} books.")
    return clippings

# Create markdown file for each book
def create_markdown_files(clippings, dest_dir, create_moc=True, moc_filename=""):
    filenames = {}

    if RICH_AVAILABLE:
        console.print(f"[bold]Creating markdown files for [green]{len(clippings)}[/green] books[/bold]")
        
        total_books = len(clippings)
        for i, (book, quotes) in enumerate(clippings.items()):
            console.print(f"[cyan]Writing book {i+1}/{total_books}: {book}...[/cyan]")
            
            clean_book_name = re.sub(r'[:\\/?*"><|]', '', book).strip()
            filename = f"{clean_book_name}.md"
            filepath = os.path.join(dest_dir, filename)
            filenames[book] = clean_book_name

            # Sort quotes by page/location number (if available)
            sorted_quotes = sorted(quotes, key=lambda q: q[0] if q[0] else "")
            
            with open(filepath, 'w', encoding='utf-8') as md_file:  # 'w' mode overwrites existing files
                if create_moc and moc_filename:
                    md_file.write(f"[[{moc_filename}]]\n\n")
                md_file.write(f"# {book}\n\n")

                for page, quote in sorted_quotes:
                    if page:
                        md_file.write(f"**Page {page}**\n\n")
                    else:
                        md_file.write("**Unknown location**\n\n")
                    md_file.write(f"> {quote}\n\n")
    else:
        print(f"Creating markdown files for {len(clippings)} books")
        for book, quotes in clippings.items():
            clean_book_name = re.sub(r'[:\\/?*"><|]', '', book).strip()
            filename = f"{clean_book_name}.md"
            filepath = os.path.join(dest_dir, filename)
            filenames[book] = clean_book_name

            # Sort quotes by page/location number (if available)
            sorted_quotes = sorted(quotes, key=lambda q: q[0] if q[0] else "")

            print(f"Writing {len(sorted_quotes)} unique clippings to {repr(filepath)}")
            with open(filepath, 'w', encoding='utf-8') as md_file:  # 'w' mode overwrites existing files
                if create_moc and moc_filename:
                    md_file.write(f"[[{moc_filename}]]\n\n")
                md_file.write(f"# {book}\n\n")

                for page, quote in sorted_quotes:
                    if page:
                        md_file.write(f"**Page {page}**\n\n")
                    else:
                        md_file.write("**Unknown location**\n\n")
                    md_file.write(f"> {quote}\n\n")

    if create_moc and moc_filename:
        create_moc_file(filenames, dest_dir, moc_filename)
    return filenames

# Create a Map of Content (MOC) file
def create_moc_file(filenames, dest_dir, moc_filename):
    moc_filepath = os.path.join(dest_dir, f"{moc_filename}.md")

    if RICH_AVAILABLE:
        console.print(f"[bold]Creating MOC file at[/bold] {repr(moc_filepath)}")
    else:
        print(f"Creating MOC file at {repr(moc_filepath)}")
        
    with open(moc_filepath, 'w', encoding='utf-8') as moc_file:
        moc_file.write("[[home]]\n\n")
        current_date = datetime.now().strftime("%Y-%m-%d")
        moc_file.write(f"*Last updated: {current_date}*\n\n")

        sorted_books = sorted(filenames.keys())
        moc_file.write("## Book Highlights\n\n")
        for book in sorted_books:
            clean_name = filenames[book]
            moc_file.write(f"[[{clean_name}]]\n")
            
    if RICH_AVAILABLE:
        console.print(f"[green]✓[/green] MOC file created with [bold]{len(filenames)}[/bold] book links")

# Process clippings
def process_clippings(config, delete_source=False):
    device_name = config.get('device_name', '')
    dest_dir = os.path.expanduser(config.get('dest_dir', ''))
    create_moc = config.get('create_moc', True)
    moc_filename = config.get('moc_filename', '') if create_moc else ''
    
    clippings_file_path = get_clippings_file_path(device_name)
    
    if RICH_AVAILABLE:
        console.print(f"[bold]Looking for clippings at:[/bold]", clippings_file_path)
        console.print(f"[bold]Will save markdown files to:[/bold]", dest_dir)
    else:
        print(f"Looking for clippings at: {clippings_file_path}")
        print(f"Will save markdown files to: {dest_dir}")
    
    if not os.path.exists(clippings_file_path):
        if RICH_AVAILABLE:
            console.print(f"[bold red]ERROR:[/bold red] Clippings file not found at {clippings_file_path}")
        else:
            print(f"ERROR: Clippings file not found at {clippings_file_path}")
        return False
    
    ensure_dest_dir(dest_dir)
    
    if RICH_AVAILABLE:
        with console.status("[bold green]Reading clippings file...", spinner="dots"):
            content = read_clippings(clippings_file_path)
        
        with console.status("[bold green]Parsing clippings...", spinner="dots"):
            clippings = parse_clippings(content)
    else:
        content = read_clippings(clippings_file_path)
        clippings = parse_clippings(content)
    
    if clippings:
        if RICH_AVAILABLE:
            with console.status("[bold green]Creating markdown files...", spinner="dots"):
                create_markdown_files(clippings, dest_dir, create_moc, moc_filename)
        else:
            create_markdown_files(clippings, dest_dir, create_moc, moc_filename)
        
        if delete_source:
            try:
                if RICH_AVAILABLE:
                    with console.status("[bold yellow]Deleting source file...", spinner="dots"):
                        os.remove(clippings_file_path)
                    console.print(f"[green]Deleted source file:[/green] {clippings_file_path}")
                else:
                    # Delete the original file
                    os.remove(clippings_file_path)
                    print(f"Deleted source file: {clippings_file_path}")
            except Exception as e:
                if RICH_AVAILABLE:
                    console.print(f"[bold red]Error while trying to delete source file:[/bold red] {e}")
                else:
                    print(f"Error while trying to delete source file: {e}")
        
        if RICH_AVAILABLE:
            console.print("[bold green]✓ Done![/bold green] Markdown files and MOC created successfully.")
        else:
            print("Done! Markdown files and MOC created successfully.")
        return True
    else:
        if RICH_AVAILABLE:
            console.print("[yellow]No clippings found to process.[/yellow]")
        else:
            print("No clippings found to process.")
        return False

# Main function
# Delete clippings file without processing
def delete_clippings_file(config):
    device_name = config.get('device_name', '')
    clippings_file_path = get_clippings_file_path(device_name)
    
    if RICH_AVAILABLE:
        console.print(f"[bold]Looking for clippings at:[/bold]", clippings_file_path)
    else:
        print(f"Looking for clippings at: {clippings_file_path}")
    
    if not os.path.exists(clippings_file_path):
        if RICH_AVAILABLE:
            console.print(f"[bold red]ERROR:[/bold red] Clippings file not found at {clippings_file_path}")
        else:
            print(f"ERROR: Clippings file not found at {clippings_file_path}")
        return False
    
    try:
        if RICH_AVAILABLE:
            with console.status("[bold yellow]Deleting source file...", spinner="dots"):
                os.remove(clippings_file_path)
            console.print(f"[green]✓[/green] Deleted source file: {clippings_file_path}")
        else:
            # Delete the original file
            os.remove(clippings_file_path)
            print(f"Deleted source file: {clippings_file_path}")
        return True
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[bold red]Error while trying to delete source file:[/bold red] {e}")
        else:
            print(f"Error while trying to delete source file: {e}")
        return False

def display_welcome():
    if not RICH_AVAILABLE:
        return
        
    console.print(Panel.fit(
        "[bold blue]Klippy[/bold blue] - [cyan]Kindle Clippings to Markdown Converter[/cyan]",
        border_style="blue"
    ))
    
    # Create a table for commands
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Command", style="dim")
    table.add_column("Description")
    
    table.add_row("--config", "Configure Klippy settings")
    table.add_row("--add", "Process clippings without deleting source file")
    table.add_row("--sync", "Process clippings and delete source file")
    table.add_row("--delete", "Delete clippings file without processing")
    
    console.print(table)
    console.print()

def main():
    if RICH_AVAILABLE:
        display_welcome()
    
    parser = argparse.ArgumentParser(description='Kindle clippings to Markdown converter for Obsidian')
    parser.add_argument('--config', action='store_true', help='Configure Klippy settings')
    parser.add_argument('--add', action='store_true', help='Process clippings without deleting source file')
    parser.add_argument('--sync', action='store_true', help='Process clippings and delete source file')
    parser.add_argument('--delete', action='store_true', help='Delete clippings file without processing')
    
    args = parser.parse_args()
    
    if args.config:
        setup_config()
        return
    
    config = load_config()
    
    # Handle delete operation
    if args.delete:
        delete_clippings_file(config)
        return
    
    # If no action flags are provided, show help
    if not (args.add or args.sync):
        if not RICH_AVAILABLE:  # Only show standard help if rich is not available
            parser.print_help()
        return
    
    # --sync takes precedence over --add if both are specified
    process_clippings(config, delete_source=args.sync)

if __name__ == "__main__":
    main()
