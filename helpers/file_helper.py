import re

import unicodedata


class FileHelper:

    @staticmethod
    def normalize_filename(title: str, prefix=None, ext=None) -> str:
        # Strip and normalize unicode
        title = title.strip().lower()
        title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")

        # Replace spaces and underscores with hyphens
        title = re.sub(r"[\s_]+", "-", title)

        # Remove any remaining invalid characters
        title = re.sub(r"[^a-z0-9\-]", "", title)

        # collapse multiple hyphens into one
        title = re.sub(r"-{2,}", "-", title)

        # Remove leading/trailing hyphens
        title = title.strip("-")

        # Combine with prefix and extension
        filename = f"{prefix}-{title}.{ext}"
        return filename
