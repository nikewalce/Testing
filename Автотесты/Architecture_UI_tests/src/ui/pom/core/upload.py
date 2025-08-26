import re
import shutil
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import fitz
import psutil


class FileUpload:
    """Класс для обработки скаченных файлов."""

    def __init__(self, path: Path = None):
        """
        :param path: Путь к директории, где находятся файлы.
        """
        self._path = path

    @property
    def base_path(self) -> Path:
        return Path("upload") if self._path is None else self._path

    def find_file_by_extension(self, extension: str) -> Path:
        """
        Находит файл с указанным расширением.

        :param extension: Расширение файла (например, "pdf", "zip", "xml").
        """
        file_path = next(self.base_path.glob(f"*.{extension}"), None)
        if not file_path:
            raise FileNotFoundError(
                f"Файл с расширением '{extension}' не найден в директории {self.base_path}"
            )
        return file_path

    def parse_file(self, extension: str) -> str:
        """
        Парсит содержимое файла с указанным расширением.

        :param extension: Расширение файла.
        """
        parsers = {
            "pdf": self._parse_pdf,
            "xml": self._parse_xml,
        }

        if extension not in parsers:
            raise ValueError(
                f"Поддерживаемые форматы для парсинга: {list(parsers.keys())}"
            )

        return parsers[extension]()

    def _parse_pdf(self) -> str:
        """Парсинг текста из PDF файла."""
        file_path = self.find_file_by_extension("pdf")
        with fitz.open(file_path) as pdf_document:
            pdf_text = " ".join(page.get_text("text") for page in pdf_document)
        pdf_text = re.sub(r"(?<!\n)\n(?!\n)|\s{2,}", " ", pdf_text)
        return pdf_text

    def _parse_xml(self) -> str:
        """Парсинг текста из XML файла."""
        file_path = self.find_file_by_extension("xml")
        tree = ET.parse(file_path)
        root = tree.getroot()
        xml_text = " ".join(element.text or "" for element in root.iter())
        xml_text = re.sub(r"\s{2,}", " ", xml_text).strip()
        return xml_text

    def _terminate_process_using_file(self, file_path: Path):
        """
        Завершает процесс, который использует указанный файл.
        :param file_path: Путь к файлу.
        """
        proc = next(
            (
                proc
                for proc in psutil.process_iter(["pid", "open_files"])
                if any(
                    open_file.path == str(file_path)
                    for open_file in (proc.info["open_files"] or [])
                )
            ),
            None,
        )
        if proc:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except psutil.TimeoutExpired:
                raise RuntimeError(
                    f"Не удалось завершить процесс, использующий файл: {file_path}"
                )

    def delete_upload_directory(self) -> None:
        """Очистка директории upload после теста."""
        crdownload_file = next(self.base_path.glob("*.crdownload"), None)
        if crdownload_file:
            self._terminate_process_using_file(crdownload_file)
            crdownload_file.unlink(missing_ok=True)
        shutil.rmtree(self.base_path, ignore_errors=True)

    def unpack_zip_archive(self):
        """
        Распаковка zip-архива.
        """
        zip_path = self.find_file_by_extension("zip")
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(self.base_path)
        except zipfile.BadZipFile:
            raise ValueError("Архив поврежден.")
