import re
import unicodedata


def normalize_arabic(text: str) -> str:
    """Normalize Arabic text: remove diacritics, normalize alef variants."""
    text = unicodedata.normalize("NFC", text)
    # Remove Arabic diacritics (tashkeel)
    text = re.sub(r"[ً-ٰٟ]", "", text)
    # Normalize alef variants → bare alef
    text = re.sub(r"[إأآا]", "ا", text)
    # Normalize teh marbuta → heh
    text = re.sub(r"ة", "ه", text)
    return text.strip()


def is_arabic(text: str) -> bool:
    arabic_chars = sum(1 for c in text if "؀" <= c <= "ۿ")
    return arabic_chars > len(text) * 0.3
