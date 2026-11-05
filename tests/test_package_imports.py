"""Every module in the package imports cleanly.

Catches broken, misnamed or misplaced files as the package structure grows.
"""

import importlib
import pkgutil

import pytest

import sensitive_prompt_insights

MODULES = sorted(
    info.name
    for info in pkgutil.walk_packages(
        sensitive_prompt_insights.__path__, prefix="sensitive_prompt_insights."
    )
)


def test_expected_subpackages_exist() -> None:
    for sub in (
        "data",
        "detection",
        "clustering",
        "uncertainty",
        "labelling",
        "reporting",
    ):
        assert f"sensitive_prompt_insights.{sub}" in MODULES


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name: str) -> None:
    importlib.import_module(name)
