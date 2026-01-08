# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Single-file Python CLI tool that batch converts SVG files to PNG using `rsvg-convert` (from librsvg).

## System Dependency

Requires librsvg installed via Homebrew:
```bash
brew install librsvg
```

## Usage

```bash
# Basic conversion
python3 convert_svg_to_png.py /path/to/svgs

# With options
python3 convert_svg_to_png.py /path/to/svgs --dpi 300 --scale 2 --output /custom/output
```

Output goes to `png_output/` subfolder by default.
