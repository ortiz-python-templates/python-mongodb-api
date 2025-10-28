from os.path import splitext


class FileExtensions:
    """
    Defines common file extension groups used for file upload validation
    """

    # Common image formats (used in photo uploads and previews)
    Images = [".jpg", ".jpeg", ".png", ".gif"]

    # Common document formats (used in text, presentations, and spreadsheets)
    Documents = [".txt", ".pdf", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"]

    # Text-based file formats, often used for data export/import
    CsvTxts = [".csv", ".txt"]

    # Compressed archive formats
    Archives = [".zip", ".rar", ".7z", ".tar", ".gz"]


    @staticmethod
    def is_valid_extension(filename: str, allowed_extensions: list[str]) -> bool:
        """Checks whether a file has an allowed extension."""
        return FileExtensions.get_extension(filename) in allowed_extensions


    @staticmethod
    def get_extension(filename: str) -> str:
        return splitext(filename)[1].lower()

