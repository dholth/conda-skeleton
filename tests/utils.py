# Copyright (C) 2014 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from pathlib import Path

tests_path = Path(__file__).parent
metadata_path = tests_path / "test-recipes" / "metadata"
subpackage_path = tests_path / "test-recipes" / "split-packages"
fail_path = tests_path / "test-recipes" / "fail"
variants_path = tests_path / "test-recipes" / "variants"
dll_path = tests_path / "test-recipes" / "dll-package"
go_path = tests_path / "test-recipes" / "go-package"
published_path = tests_path / "test-recipes" / "published_code"
archive_path = tests_path / "archives"
cran_path = tests_path / "test-cran-skeleton"

# backport
thisdir = str(tests_path)
metadata_dir = str(metadata_path)
subpackage_dir = str(subpackage_path)
fail_dir = str(fail_path)
variants_dir = str(variants_path)
dll_dir = str(dll_path)
go_dir = str(go_path)
published_dir = str(published_path)
archive_dir = str(archive_path)
cran_dir = str(cran_path)
