
"""Tests for the Module 7 QR Code Generator."""

import main as qr_app
import logging
import sys
from pathlib import Path

import pytest

from main import (
    create_directory,
    generate_qr_code,
    is_valid_url,
    main,
)


def test_valid_url():
    """A valid HTTPS URL should pass validation."""
    assert is_valid_url("https://www.google.com") is True


def test_invalid_url():
    """Invalid text should fail URL validation."""
    assert is_valid_url("not-a-valid-url") is False


def test_create_directory(tmp_path):
    """The application should create missing directories."""
    directory = tmp_path / "new_folder"

    create_directory(directory)

    assert directory.exists()
    assert directory.is_dir()


def test_generate_qr_code(tmp_path):
    """A valid URL should generate a PNG file."""
    output_file = tmp_path / "test_qr.png"

    generate_qr_code(
        "https://www.google.com",
        output_file,
        fill_color="red",
        back_color="white",
    )

    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_invalid_url_does_not_generate_file(tmp_path):
    """An invalid URL should not create a QR code."""
    output_file = tmp_path / "invalid_qr.png"

    generate_qr_code(
        "invalid-url",
        output_file,
    )

    assert not output_file.exists()


def test_generate_qr_code_custom_colors(tmp_path):
    """QR generation should accept custom colors."""
    output_file = tmp_path / "custom_qr.png"

    generate_qr_code(
        "https://www.python.org",
        output_file,
        fill_color="blue",
        back_color="yellow",
    )

    assert output_file.exists()


def test_generate_qr_code_save_error(tmp_path, caplog):
    """A file-writing error should be logged."""
    output_file = tmp_path / "missing_folder" / "qr.png"

    with caplog.at_level(logging.ERROR):
        generate_qr_code(
            "https://www.google.com",
            output_file,
        )

    assert not output_file.exists()
    assert "An error occurred" in caplog.text


def test_create_directory_error(tmp_path, monkeypatch):
    """A directory creation error should exit the program."""
    file_path = tmp_path / "existing_file"
    file_path.write_text("This is a file.")

    with pytest.raises(SystemExit) as error:
        create_directory(file_path / "new_folder")

    assert error.value.code == 1


def test_main_generates_qr_code(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(qr_app, "QR_DIRECTORY", "qr_codes")
    monkeypatch.setattr(
        sys,
        "argv",
        ["main.py", "--url", "https://www.google.com"],
    )

    qr_app.main()

    generated_files = list(
        (tmp_path / "qr_codes").glob("QRCode_*.png")
    )

    assert len(generated_files) == 1
    assert generated_files[0].stat().st_size > 0