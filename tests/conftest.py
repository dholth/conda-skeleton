# Copyright (C) 2014 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

import os
from typing import TYPE_CHECKING

import conda_build.config
import pytest
from conda.common.compat import on_mac
from conda_build.config import (
    Config,
    _get_or_merge_config,
    _src_cache_root_default,
    conda_pkg_format_default,
    enable_static_default,
    error_overdepending_default,
    error_overlinking_default,
    exit_on_verify_error_default,
    filename_hashing_default,
    ignore_verify_codes_default,
    no_rewrite_stdout_env_default,
)

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from pytest import MonkeyPatch


@pytest.fixture(scope="function")
def testing_workdir(monkeypatch: MonkeyPatch, tmp_path: Path) -> Iterator[str]:
    monkeypatch.chdir(tmp_path)
    yield str(tmp_path)


@pytest.fixture(scope="function")
def testing_config(testing_workdir: str) -> Config:
    def boolify(v: str) -> bool:
        return v == "true"

    testing_config_kwargs = dict(
        croot=testing_workdir,
        anaconda_upload=False,
        verbose=True,
        activate=False,
        debug=False,
        test_run_post=False,
        filename_hashing=filename_hashing_default,
        _src_cache_root=_src_cache_root_default,
        error_overlinking=boolify(error_overlinking_default),
        error_overdepending=boolify(error_overdepending_default),
        enable_static=boolify(enable_static_default),
        no_rewrite_stdout_env=boolify(no_rewrite_stdout_env_default),
        ignore_verify_codes=ignore_verify_codes_default,
        exit_on_verify_error=exit_on_verify_error_default,
        conda_pkg_format=conda_pkg_format_default,
    )

    if on_mac and "CONDA_BUILD_SYSROOT" in os.environ:
        var_dict = {
            "CONDA_BUILD_SYSROOT": [os.environ["CONDA_BUILD_SYSROOT"]],
        }
    else:
        var_dict = None

    result = Config(variant=var_dict, **testing_config_kwargs)
    result._testing_config_kwargs = testing_config_kwargs
    assert result.no_rewrite_stdout_env is False
    assert result._src_cache_root is None
    assert result.src_cache_root == testing_workdir
    return result


@pytest.fixture(scope="function", autouse=True)
def default_testing_config(
    testing_config: Config,
    monkeypatch: MonkeyPatch,
    request: pytest.FixtureRequest,
) -> None:
    if "no_default_testing_config" in request.keywords:
        return

    def get_or_merge_testing_config(config, variant=None, **kwargs):
        if not config:
            kwargs.update(
                {
                    key: value
                    for key, value in testing_config._testing_config_kwargs.items()
                    if kwargs.get(key) is None
                }
            )
        return _get_or_merge_config(config, variant, **kwargs)

    monkeypatch.setattr(
        conda_build.config,
        "_get_or_merge_config",
        get_or_merge_testing_config,
    )
