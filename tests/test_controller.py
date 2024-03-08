import pytest
from roachcase import _controller, _repositories
from roachcase._infrastructure import shelf_repositories


def test_set_persistence(tmp_path):
    factory = _controller.get_use_case_factory()
    repofactory = factory.get_repo_factory()
    assert isinstance(repofactory, _repositories.InMemoryRepositoryFactory)

    # we can set to persiste on file system
    _controller.set_persistence("shelf", tmp_path)
    repofactory = factory.get_repo_factory()
    assert isinstance(repofactory, shelf_repositories.ShelfRepositoryFactory)

    # and we can reset back to memory
    _controller.set_persistence("memory")
    repofactory = factory.get_repo_factory()
    assert isinstance(repofactory, _repositories.InMemoryRepositoryFactory)

    with pytest.raises(ValueError):
        _controller.set_persistence("sql")
