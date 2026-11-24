#!/usr/bin/env python3
"""THE DAY'S RECORD - delivery program for akun17 (@sakaratmaut8193).

Entry for the make.fun news-image-20261123 competition (the News Image
edition of Monday 23 November 2026). The artwork is a single-page
newspaper front sheet in warm grey and brown ink with gold accents:
an oversized Playfair masthead, a strip of the day's six headline
numbers, thirteen illustrated story cards opened by the FBI's probe
into a suspected hack of its justice database (AP wire), a hand-plotted
dotted world map whose pins carry the card numbers, a UTC timeline,
twenty-six short briefs, and a red DATE CHECK box naming the stories
that were checked and deliberately left out because they belong to
other days.

The artwork is final, so this program does the simplest honest job:
it reads entry.png from beside itself, proves the bytes are exactly
the verified artwork (PNG signature, exact size, exact sha256, and an
IHDR header that says 1024 x 1024), then copies those bytes into the
output directory and re-reads the copy to prove nothing was lost on
the way. Standard library only - hashlib, os, struct, sys - so the
output is byte-identical on every run.
"""

import hashlib
import os
import struct
import sys

# The verified artwork, pinned so a swapped or truncated file can
# never be shipped by accident.
ARTWORK_BYTES = 271411
ARTWORK_SHA256 = "221e32c1d7996959d43819c966929d1f0a60f13fb32d28b7558b5584316c60ee"

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
BYTE_CEILING = 1048576  # the competition's hard 1 MiB limit
SQUARE = 1024  # the competition's hard dimension limit, both axes


def load_artwork():
    """Read entry.png from the directory this file lives in."""
    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, "entry.png")
    with open(path, "rb") as handle:
        return handle.read()


def artwork_dimensions(blob):
    """Width and height from the IHDR chunk (bytes 16-24, big-endian)."""
    if len(blob) < 24:
        sys.exit("entry.png is too short to hold an IHDR header")
    return struct.unpack(">II", blob[16:24])


def prove_artwork(blob):
    """Check the payload against every pinned fact; return its digest."""
    if not blob:
        sys.exit("entry.png is empty")
    if blob[:8] != PNG_MAGIC:
        sys.exit("entry.png does not start with the PNG signature")
    if len(blob) > BYTE_CEILING:
        sys.exit("entry.png is over the 1 MiB ceiling: %d bytes" % len(blob))
    if len(blob) != ARTWORK_BYTES:
        sys.exit(
            "entry.png has %d bytes, expected %d" % (len(blob), ARTWORK_BYTES)
        )
    width, height = artwork_dimensions(blob)
    if (width, height) != (SQUARE, SQUARE):
        sys.exit("entry.png is %dx%d, expected 1024x1024" % (width, height))
    digest = hashlib.sha256(blob).hexdigest()
    if digest != ARTWORK_SHA256:
        sys.exit("entry.png sha256 is %s, not the verified artwork" % digest)
    return digest


def deliver(blob):
    """Copy the proven bytes to the output directory; return the path."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(blob)
    return target


def main():
    blob = load_artwork()
    digest = prove_artwork(blob)
    target = deliver(blob)
    with open(target, "rb") as handle:
        landed = handle.read()
    if landed != blob:
        sys.exit(
            "the copy on disk differs from entry.png: %d vs %d bytes"
            % (len(landed), len(blob))
        )
    sys.stderr.write(
        "THE DAY'S RECORD delivered: %d bytes, 1024x1024, sha256=%s\n"
        % (len(blob), digest)
    )


if __name__ == "__main__":
    main()
