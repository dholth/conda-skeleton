# Copyright (C) 2014 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

import logging
import os
import pkgutil
from importlib import import_module
from os.path import expanduser
from typing import TYPE_CHECKING

from conda.base.context import context
from conda_build.config import Config, get_or_merge_config
from conda_build.utils import ensure_list

if TYPE_CHECKING:
    from collections.abc import Sequence

thisdir = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.INFO)


def parse_args(args: Sequence[str] | None):
    from conda.cli.conda_argparse import ArgumentParser

    parser = ArgumentParser(
        prog="conda skeleton",
        description="""
Generates a boilerplate/skeleton recipe, which you can then edit to create a
full recipe. Some simple skeleton recipes may not even need edits.
        """,
        epilog="""
Run --help on the subcommands like 'conda skeleton pypi --help' to see the
options available.
        """,
    )

    repos = parser.add_subparsers(dest="repo")

    skeletons = [
        name
        for _, name, _ in pkgutil.iter_modules([os.path.join(thisdir, "../skeletons")])
    ]
    for skeleton in skeletons:
        if skeleton.startswith("_"):
            continue
        module = import_module(f"conda_skeleton.skeletons.{skeleton}")
        module.add_parser(repos)

    return parser, parser.parse_args(args)


def skeletonize(
    packages: str | Sequence[str],
    repo: str,
    output_dir: str = ".",
    version: str | None = None,
    recursive: bool = False,
    config: Config | None = None,
    **kwargs,
) -> None:
    version = getattr(config, "version", version)
    if version:
        kwargs.update({"version": version})
    if recursive:
        kwargs.update({"recursive": recursive})
    if output_dir != ".":
        kwargs.update({"output_dir": expanduser(output_dir)})

    config = get_or_merge_config(config, **kwargs)
    config.compute_build_id("skeleton")
    packages = ensure_list(packages)

    module = import_module(f"conda_skeleton.skeletons.{repo}")

    func_args = module.skeletonize.__code__.co_varnames
    passed_kwargs = {
        name: getattr(config, name) for name in dir(config) if name in func_args
    }
    passed_kwargs.update(
        {name: value for name, value in kwargs.items() if name in func_args}
    )
    for arg in skeletonize.__code__.co_varnames:
        passed_kwargs.pop(arg, None)

    with config:
        module.skeletonize(
            packages,
            output_dir=output_dir,
            version=version,
            recursive=recursive,
            config=config,
            **passed_kwargs,
        )


def execute(args: Sequence[str] | None = None) -> int:
    parser, parsed = parse_args(args)
    context.__init__(argparse_args=parsed)

    config = Config(**parsed.__dict__)

    if not parsed.repo:
        parser.print_help()
        return 0

    skeletonize(
        parsed.packages,
        parsed.repo,
        output_dir=parsed.output_dir,
        recursive=parsed.recursive,
        version=parsed.version,
        config=config,
    )

    return 0
