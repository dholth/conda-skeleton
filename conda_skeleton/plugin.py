# Copyright (C) 2014 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from typing import TYPE_CHECKING

import conda.plugins
from conda.plugins.types import CondaSubcommand

if TYPE_CHECKING:
    from collections.abc import Sequence


def skeleton(args: Sequence[str]) -> int:
    from .cli.main_skeleton import execute

    return execute(args)


@conda.plugins.hookimpl
def conda_subcommands():
    yield CondaSubcommand(
        name="skeleton2",
        summary="Generate boilerplate conda recipes.",
        action=skeleton,
    )
