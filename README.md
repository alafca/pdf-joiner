# PDF Joiner

A small Windows desktop app for merging PDFs. Add files, put them in order, and save them as a single PDF.

## Features

- Add PDFs with drag and drop or a file picker
- Reorder with **Move up** / **Move down**, remove single files, or clear the list
- Skips duplicates and files that aren't PDFs
- Offers to open the merged file when it's done

## Requirements

- Windows
- Python 3.9+ from [python.org](https://www.python.org/downloads/). Anaconda's tkinter layout breaks PyInstaller's bundling.

## Run from source

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python pdf_joiner.py
```

Drag and drop needs `tkinterdnd2`. If it isn't installed, the app falls back to the file picker.

## Build a standalone .exe

```bat
build.bat
```

This creates `.venv` if it doesn't exist, installs the dependencies, and writes `dist\PDF Joiner.exe`, a single-file windowed executable.

## License

[MIT](LICENSE)
