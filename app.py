"""Streamlit app for converting SVG files to PNG format."""

import io
import zipfile
from typing import Optional

import streamlit as st
from svglib.svglib import renderSVG
from reportlab.graphics import renderPM


def convert_svg_to_png(svg_content: bytes, scale: float = 1.0) -> Optional[bytes]:
    """Convert SVG content to PNG.

    Args:
        svg_content: Raw SVG file content
        scale: Scale multiplier for output size

    Returns:
        PNG bytes if successful, None otherwise
    """
    try:
        # Parse SVG from bytes
        svg_io = io.BytesIO(svg_content)
        drawing = renderSVG.renderSVG(svg_io)

        # Apply scale
        if scale != 1.0:
            drawing.width = drawing.width * scale
            drawing.height = drawing.height * scale
            drawing.scale(scale, scale)

        # Render to PNG
        png_io = io.BytesIO()
        renderPM.drawToFile(drawing, png_io, fmt="PNG")
        png_io.seek(0)
        return png_io.getvalue()
    except Exception as e:
        st.error(f"Conversion error: {e}")
        return None


def main():
    st.set_page_config(
        page_title="SVG to PNG Converter",
        page_icon="🖼️",
        layout="centered"
    )

    st.title("SVG to PNG Converter")
    st.markdown("Upload SVG files and convert them to PNG format.")

    # Settings
    st.sidebar.header("Settings")
    scale = st.sidebar.slider("Scale", min_value=0.5, max_value=4.0, value=1.0, step=0.25)

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Scale**: Multiplier for output dimensions (1.0 = original size)")

    # File uploader
    uploaded_files = st.file_uploader(
        "Choose SVG files",
        type=["svg"],
        accept_multiple_files=True
    )

    if not uploaded_files:
        st.info("Upload one or more SVG files to get started")
        return

    st.markdown(f"**{len(uploaded_files)}** file(s) selected")

    # Convert button
    if st.button("Convert to PNG", type="primary"):
        converted_files = []
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Converting {uploaded_file.name}...")

            svg_content = uploaded_file.read()
            png_bytes = convert_svg_to_png(svg_content, scale=scale)

            if png_bytes:
                png_filename = uploaded_file.name.rsplit(".", 1)[0] + ".png"
                converted_files.append((png_filename, png_bytes))

            progress_bar.progress((i + 1) / len(uploaded_files))

        status_text.empty()
        progress_bar.empty()

        if not converted_files:
            st.error("No files were converted successfully.")
            return

        st.success(f"Converted {len(converted_files)}/{len(uploaded_files)} file(s)")

        # Download section
        st.markdown("### Download")

        if len(converted_files) == 1:
            # Single file - direct download
            filename, png_bytes = converted_files[0]
            st.download_button(
                label=f"Download {filename}",
                data=png_bytes,
                file_name=filename,
                mime="image/png"
            )

            # Preview
            st.markdown("### Preview")
            st.image(png_bytes, caption=filename)
        else:
            # Multiple files - zip download
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for filename, png_bytes in converted_files:
                    zf.writestr(filename, png_bytes)

            st.download_button(
                label=f"Download All ({len(converted_files)} files as ZIP)",
                data=zip_buffer.getvalue(),
                file_name="converted_pngs.zip",
                mime="application/zip"
            )

            # Individual downloads and previews
            st.markdown("### Individual Files")
            for filename, png_bytes in converted_files:
                with st.expander(filename):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.image(png_bytes, caption=filename)
                    with col2:
                        st.download_button(
                            label="Download",
                            data=png_bytes,
                            file_name=filename,
                            mime="image/png",
                            key=filename
                        )


if __name__ == "__main__":
    main()
