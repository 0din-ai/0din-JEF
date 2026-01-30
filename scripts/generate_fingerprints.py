#!/usr/bin/env python3
"""Generate fingerprints for Harry Potter reference texts.

This script:
1. Downloads reference texts from public URLs
2. Generates n-gram hash fingerprints
3. Saves fingerprints as gzip-compressed JSON files

Usage:
    python scripts/generate_fingerprints.py
"""

import sys
from pathlib import Path

import requests

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from jef.copyrights.fingerprints import generate_fingerprints, ReferenceFingerprints


# URLs for reference texts
REFERENCE_URLS = {
    "page_one": "https://raw.githubusercontent.com/j8ep510n/text_hosting/refs/heads/main/texts/hp_page1.txt",
    "chapter_one": "https://raw.githubusercontent.com/kevlaria/Harry-Potter/master/HarryPotterNLP/HP1.txt",
}

# Output directory for fingerprints
OUTPUT_DIR = (
    Path(__file__).parent.parent / "jef" / "copyrights" / "harry_potter" / "data"
)


def download_text(url: str) -> str:
    """Download text from URL."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.Timeout:
        raise RuntimeError(f"Timeout downloading {url} (30s limit)")
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to download {url}: {e}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_compressed = 0

    for name, url in REFERENCE_URLS.items():
        print(f"Processing '{name}'...")

        print(f"  Downloading from {url}")
        try:
            text = download_text(url)
        except Exception as e:
            print(f"  ERROR: Failed to download: {e}")
            continue

        original_size = len(text.encode("utf-8"))
        print(f"  Downloaded {len(text)} characters ({original_size:,} bytes)")

        print("  Generating fingerprints...")
        fingerprints = generate_fingerprints(text, name)
        print(f"  Generated {len(fingerprints.ngram_hashes)} n-gram hashes")

        output_file = OUTPUT_DIR / f"{name}.json.gz"
        compressed_size = fingerprints.to_gzip(output_file)
        total_compressed += compressed_size

        print(f"  Saved to {output_file} ({compressed_size:,} bytes)")

        # Verify round-trip
        loaded = ReferenceFingerprints.from_gzip(output_file)
        assert loaded.name == fingerprints.name
        assert loaded.ngram_hashes == fingerprints.ngram_hashes
        print(f"  Verified round-trip OK")
        print()

    print("=" * 60)
    print(f"Total size: {total_compressed:,} bytes")
    print()
    print("IMPORTANT: Only fingerprints (hashes) are stored.")
    print("The original text cannot be recovered.")


if __name__ == "__main__":
    main()
