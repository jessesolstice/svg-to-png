#!/usr/bin/env python3
"""Convert all SVG files in a directory to PNG format.

Requires: rsvg-convert (install via: brew install librsvg)
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


def check_rsvg_convert() -> Optional[str]:
    """Check if rsvg-convert is available and return its path."""
    path = shutil.which("rsvg-convert")
    if path:
        return path
    # Check common Homebrew location
    homebrew_path = "/opt/homebrew/bin/rsvg-convert"
    if Path(homebrew_path).exists():
        return homebrew_path
    return None


def convert_svg_to_png(
    rsvg_path: str,
    svg_path: Path,
    output_path: Path,
    dpi: int,
    scale: float
) -> bool:
    """Convert a single SVG file to PNG.

    Args:
        rsvg_path: Path to rsvg-convert executable
        svg_path: Path to the input SVG file
        output_path: Path for the output PNG file
        dpi: Output resolution in dots per inch
        scale: Scale multiplier for output size

    Returns:
        True if conversion succeeded, False otherwise
    """
    try:
        cmd = [
            rsvg_path,
            "--dpi-x", str(dpi),
            "--dpi-y", str(dpi),
        ]
        if scale != 1.0:
            cmd.extend(["--zoom", str(scale)])
        cmd.extend(["--output", str(output_path), str(svg_path)])

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  Error converting {svg_path.name}: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"  Error converting {svg_path.name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Convert SVG files to PNG format"
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory containing SVG files"
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=96,
        help="Output resolution in DPI (default: 96)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output directory (default: png_output subfolder)"
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Scale multiplier for output size (default: 1.0)"
    )

    args = parser.parse_args()

    # Check for rsvg-convert
    rsvg_path = check_rsvg_convert()
    if not rsvg_path:
        print("Error: rsvg-convert not found.")
        print("Install it with: brew install librsvg")
        sys.exit(1)

    # Validate input directory
    if not args.directory.is_dir():
        print(f"Error: '{args.directory}' is not a valid directory")
        sys.exit(1)

    # Find all SVG files
    svg_files = list(args.directory.glob("*.svg"))
    if not svg_files:
        print(f"No SVG files found in '{args.directory}'")
        sys.exit(0)

    # Create output directory
    output_dir = args.output if args.output else args.directory / "png_output"
    output_dir.mkdir(exist_ok=True)

    scale_info = f" at {args.scale}x scale" if args.scale != 1.0 else ""
    print(f"Converting {len(svg_files)} SVG file(s) at {args.dpi} DPI{scale_info}...")
    print(f"Output directory: {output_dir}")
    print()

    success_count = 0
    for svg_path in svg_files:
        png_path = output_dir / f"{svg_path.stem}.png"
        print(f"  {svg_path.name} -> {png_path.name}")

        if convert_svg_to_png(rsvg_path, svg_path, png_path, args.dpi, args.scale):
            success_count += 1

    print()
    print(f"Converted {success_count}/{len(svg_files)} files successfully")

    if success_count < len(svg_files):
        sys.exit(1)


if __name__ == "__main__":
    main()
