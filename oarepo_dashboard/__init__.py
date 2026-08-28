# SPDX-FileCopyrightText: 2025 CESNET z.s.p.o
# SPDX-License-Identifier: MIT

"""OARepo Dashboard module initialization."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("oarepo-dashboard")
except PackageNotFoundError:
    __version__ = "0.0.0dev0+unknown"

__all__ = [
    "__version__",
]
