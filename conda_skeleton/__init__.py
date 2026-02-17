# Copyright (C) 2014 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("conda-skeleton")
except PackageNotFoundError:
    # package is not installed
    pass
