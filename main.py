"""Entry program for make.fun news-image-20261119 (Python 3.13, stdlib only).

Copies the bundled front-page image (entry.png, JPEG bytes) to the
grader's output path. The program runs with no network, twice, and both
runs must write the same bytes, so it does nothing but copy and verify:
magic bytes, the 1 MiB cap, the 1024 px cap, and a sha256 round-trip
check of what it wrote.
"""
import hashlib
import os
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024


def jpeg_size(data: bytes) -> tuple[int, int]:
    """Return (width, height) of a JPEG by scanning for its SOF marker."""
    if data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG: bad SOI marker")
    pos = 2
    while pos + 1 < len(data):
        if data[pos] != 0xFF:
            pos += 1
            continue
        marker = data[pos + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if pos + 4 > len(data):
            break
        length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
            return width, height
        pos += 2 + length
    raise ValueError("no SOF marker found in JPEG")


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_path = out_dir / "entry.png"
    data = SOURCE.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the {MAX_BYTES} cap")
    width, height = jpeg_size(data)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"entry.png is {width}x{height}, over the {MAX_SIDE} cap")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    written = out_path.read_bytes()
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(data).hexdigest():
        raise ValueError("written bytes do not match the bundled image")
    print(f"wrote {out_path} ({len(data)} bytes, {width}x{height})")


if __name__ == "__main__":
    main()
