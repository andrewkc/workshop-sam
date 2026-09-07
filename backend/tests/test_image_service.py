import io
from PIL import Image
from app.image_service import cutout, prompt_for, select_primary
from app.providers import MaskCandidate


def test_prompt_comes_from_listing():
    product = type("Product", (), {"category": "silla", "name": "Roble Clara"})()
    assert prompt_for(product) == "silla roble clara"


def test_selects_score_then_largest_area():
    small = Image.new("L", (10, 10)); small.paste(255, (0, 0, 2, 2))
    large = Image.new("L", (10, 10)); large.paste(255, (0, 0, 8, 8))
    assert select_primary([MaskCandidate(small, .8), MaskCandidate(large, .8)]).mask is large


def test_cutout_has_transparent_background_and_crops():
    source = Image.new("RGB", (8, 8), "red"); source_bytes = io.BytesIO(); source.save(source_bytes, "PNG")
    mask = Image.new("L", (8, 8)); mask.paste(255, (2, 1, 6, 7)); mask.paste(0, (3, 2, 4, 3))
    png, width, height = cutout(source_bytes.getvalue(), mask)
    image = Image.open(io.BytesIO(png))
    assert (width, height) == (4, 6)
    assert image.getchannel("A").getextrema() == (0, 255)
