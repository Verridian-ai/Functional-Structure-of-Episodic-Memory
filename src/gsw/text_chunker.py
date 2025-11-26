"""
Text Chunker
============

Utilities for splitting legal text into processable chunks.
"""

from typing import List, Tuple


def chunk_legal_text(
    text: str,
    max_chunk_size: int = 15000,
    overlap: int = 500
) -> List[Tuple[str, int, int]]:
    """
    Split legal text into chunks for processing.

    Tries to split at paragraph boundaries.

    Args:
        text: The full text to chunk
        max_chunk_size: Maximum characters per chunk
        overlap: Character overlap between chunks

    Returns:
        List of (chunk_text, start_pos, end_pos)
    """
    if len(text) <= max_chunk_size:
        return [(text, 0, len(text))]

    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chunk_size

        if end >= len(text):
            chunks.append((text[start:], start, len(text)))
            break

        # Try to find a paragraph break
        para_break = text.rfind('\n\n', start + overlap, end)
        if para_break > start + overlap:
            end = para_break

        # Or sentence break
        else:
            sent_break = text.rfind('. ', start + overlap, end)
            if sent_break > start + overlap:
                end = sent_break + 1

        chunks.append((text[start:end], start, end))
        start = end - overlap

    return chunks
