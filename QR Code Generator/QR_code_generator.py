"""
===================================================
QR Code Generator Script with Center Image, Corner Image, and Text Overlay
===================================================

HOW IT WORKS:
-------------
1. Install Dependencies:
   - pip install qrcode Pillow

2. This script generates a QR code from any text or URL
   with the following features:
   - Customizable error correction levels (L, M, Q, H).
   - Auto-size fitting (the version is determined automatically
     to fit your data).
   - Custom box size, border, and colors (foreground and background).
   - The ability to overlay a smaller image (logo) in the center
     of the QR code for branding or decoration.

3. Error Correction Levels:
   - qrcode.constants.ERROR_CORRECT_L: About 7% or less errors can be corrected.
   - qrcode.constants.ERROR_CORRECT_M: About 15% or less errors can be corrected.
   - qrcode.constants.ERROR_CORRECT_Q: About 25% or less errors can be corrected.
   - qrcode.constants.ERROR_CORRECT_H: About 30% or less errors can be corrected.

4. Output:
   - By default, the script saves the QR code image to 'qrcode.png' in the
     current directory.
   - You can specify a different directory and filename if you wish.

Dependencies:
-------------
- qrcode (pip install qrcode)
- Pillow (pip install Pillow)

"""


import os
import qrcode
from PIL import Image, ImageDraw, ImageFont


def generate_qr_code(
    data,
    save_directory='.',
    filename='qrcode.png',
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
    fill_color="black",
    back_color="white",
    logo_path=None,
    corner_logo_path=None,
    text=None,
    text_font_path=None,
    text_size=20,
    text_color="black"
):
    """
    Generates a QR code with customization options.

    :param data: Text or URL to encode in the QR code.
    :param save_directory: Directory path where the QR code will be saved.
    :param filename: Name of the output image file.
    :param error_correction: Error correction level from qrcode.constants.
    :param box_size: Pixel size of each 'box' in the QR code.
    :param border: Thickness of the border (in boxes).
    :param fill_color: Color of the QR code (default "black").
    :param back_color: Background color for the QR code (default "white").
    :param logo_path: (Optional) Path to a center logo image.
    :param corner_logo_path: (Optional) Path to a small image in the bottom-right corner.
    :param text: (Optional) Text to overlay on the QR code.
    :param text_font_path: (Optional) Path to a .ttf font file for the text.
    :param text_size: Font size for the overlay text.
    :param text_color: Color of the overlay text.
    """

    # Initialize the QRCode object
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Generate the QR code image
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

    # Add the center logo, if provided
    if logo_path and os.path.isfile(logo_path):
        logo = Image.open(logo_path)
        qr_width, qr_height = img.size
        logo_size = int(qr_width * 0.25)
        logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)

        # Center the logo
        logo_x = (qr_width - logo.width) // 2
        logo_y = (qr_height - logo.height) // 2
        img.paste(logo, (logo_x, logo_y), mask=logo if logo.mode == "RGBA" else None)

    # Add the corner logo, if provided
    if corner_logo_path and os.path.isfile(corner_logo_path):
        corner_logo = Image.open(corner_logo_path)
        qr_width, qr_height = img.size
        corner_logo_size = int(qr_width * 0.15)
        corner_logo.thumbnail((corner_logo_size, corner_logo_size), Image.Resampling.LANCZOS)

        # Position the corner logo at the bottom-right
        corner_x = qr_width - corner_logo.width - 10
        corner_y = qr_height - corner_logo.height - 10
        img.paste(corner_logo, (corner_x, corner_y), mask=corner_logo if corner_logo.mode == "RGBA" else None)

    # Add text overlay, if provided
    if text:
        draw = ImageDraw.Draw(img)

        # Use default font if no font path is provided
        if text_font_path and os.path.isfile(text_font_path):
            font = ImageFont.truetype(text_font_path, text_size)
        else:
            font = ImageFont.load_default()

        # Calculate text position
        qr_width, qr_height = img.size
        text_bbox = draw.textbbox((0, 0), text, font=font)  # Get text bounding box
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (qr_width - text_width) // 2
        text_y = qr_height - text_height - 20  # Place above the bottom edge

        # Draw the text
        draw.text((text_x, text_y), text, fill=text_color, font=font)

    # Ensure the save directory exists
    os.makedirs(save_directory, exist_ok=True)
    full_path = os.path.join(save_directory, filename)

    # Save the final image
    img.save(full_path)
    print(f"QR code saved as: {full_path}")


if __name__ == "__main__":
    # Example usage
    generate_qr_code(   
        data="https://example.com",
        save_directory=r"C:\Documents\GitHub\Miscellaneous-Projects\QR Code Generator",
        filename="android_qrcode.png",
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
        fill_color="black",
        back_color="white",
        logo_path=r"C:\Documents\GitHub\Miscellaneous-Projects\QR Code Generator\primary-logo.png",
        corner_logo_path=r"C:\Documents\GitHub\Miscellaneous-Projects\QR Code Generator\secondary_logo.png",
        text=None,  # Set to None if you don't want text
        text_font_path=r"C:\Windows\Fonts\arial.ttf",  # Update with your font path
        text_size=20,
        text_color="blue"
    )
