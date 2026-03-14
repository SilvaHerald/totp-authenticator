"""Helper to create a simple icon for the system tray when no file is provided."""

from PIL import Image, ImageDraw


def create_default_icon(width: int = 64, height: int = 64) -> Image.Image:
    """Generate a simple lock icon for the system tray."""
    # Create a dark blue background
    image = Image.new("RGBA", (width, height), (30, 30, 46, 255))
    dc = ImageDraw.Draw(image)

    # Draw a simple lock shape
    # Body
    body_y = height // 2
    body_h = height // 3
    margin = width // 4
    dc.rectangle(
        [margin, body_y, width - margin, body_y + body_h],
        fill=(137, 180, 250),  # Blue
        outline=(205, 214, 244),
        width=2,
    )

    # Shackle (U-shape on top)
    shackle_x0 = margin + width // 10
    shackle_x1 = width - margin - width // 10
    shackle_y0 = body_y - height // 4
    dc.arc(
        [shackle_x0, shackle_y0, shackle_x1, body_y * 2 - shackle_y0],
        start=180,
        end=360,
        fill=(205, 214, 244),
        width=4,
    )

    return image
