"""Generator regressions for https://github.com/openloci/OpenLoci/issues/12."""

from pathlib import Path

import pytest
from cookiecutter.exceptions import OutputDirExistsException

from openloci.generator import generate_palace


@pytest.mark.parametrize("options", [(True,), (True, False), (True, False, {})])
def test_options_require_keywords(tmp_path: Path, options: tuple[object, ...]) -> None:
    """Reject positional options before resolving a skin or generating files."""
    with pytest.raises(TypeError, match="positional"):
        generate_palace("test-palace", "nonexistent_skin_xyz", tmp_path, *options)

    assert not list(tmp_path.iterdir())


def test_keyword_options_preserve_generation_and_overwrite(tmp_path: Path) -> None:
    """Named options still drive real generation, context and overwrite safety."""
    palace = generate_palace(
        "test-palace",
        "clue",
        tmp_path,
        no_input=True,
        overwrite=False,
        extra_context={"project_description": "Original test description."},
    )
    readme = palace / "the-vestibule" / "README.md"
    assert palace == tmp_path / "test-palace"
    assert "Original test description." in readme.read_text()

    with pytest.raises(OutputDirExistsException):
        generate_palace("test-palace", "clue", tmp_path, no_input=True, overwrite=False)
    assert "Original test description." in readme.read_text()

    replaced = generate_palace(
        name="test-palace",
        skin="clue",
        output_dir=tmp_path,
        no_input=True,
        overwrite=True,
        extra_context={"project_description": "Replacement test description."},
    )
    assert replaced == palace
    assert "Replacement test description." in readme.read_text()
    assert "Original test description." not in readme.read_text()
