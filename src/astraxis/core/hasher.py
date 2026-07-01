"""
ASTRAXIS-AI Cryptographic Artifact Hasher.

Produces SHA-256 fingerprints of audit reports and payload files
to guarantee tamper-proof integrity verification across enterprise deployments.

Key Concept:
    SHA-256 (Secure Hash Algorithm 256-bit) is a one-way cryptographic function.
    Even changing a single character in the input produces a completely different hash.
    This guarantees that any report exported by ASTRAXIS-AI cannot be quietly modified
    without the fingerprint mismatch being detected.
"""
import hashlib
import json
from pathlib import Path


class ArtifactHasher:
    """
    Cryptographic artifact integrity verifier using SHA-256.

    Usage:
        hasher = ArtifactHasher()
        fingerprint = hasher.hash_dict(report_dict)
        is_valid = hasher.verify_dict(report_dict, fingerprint)
    """

    ALGORITHM = "sha256"

    def hash_string(self, content: str) -> str:
        """
        Compute SHA-256 hash of a raw string.

        Args:
            content: Any string (e.g., serialized JSON report).

        Returns:
            64-character lowercase hex digest string.
        """
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def hash_dict(self, data: dict) -> str:
        """
        Compute SHA-256 hash of a Python dictionary.

        The dict is serialized with sorted keys to ensure consistent hashing
        regardless of insertion order.

        Args:
            data: Any Python dictionary (e.g., audit report payload).

        Returns:
            64-character SHA-256 hex digest.
        """
        serialized = json.dumps(data, sort_keys=True, default=str)
        return self.hash_string(serialized)

    def hash_file(self, path: Path) -> str:
        """
        Compute SHA-256 hash of a file on disk, reading in 64KB chunks
        to handle large files without loading them fully into RAM.

        Args:
            path: Path to the file to hash.

        Returns:
            64-character SHA-256 hex digest.

        Raises:
            FileNotFoundError: If the path does not exist.
        """
        if not path.exists():
            raise FileNotFoundError(f"[ArtifactHasher] File not found: {path}")

        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def verify_dict(self, data: dict, expected_hash: str) -> bool:
        """
        Verify that a dictionary's SHA-256 fingerprint matches an expected hash.

        Args:
            data: The Python dictionary to verify.
            expected_hash: The previously computed SHA-256 hash to compare against.

        Returns:
            True if the hash matches (tamper-proof), False if corrupted.
        """
        return self.hash_dict(data) == expected_hash
