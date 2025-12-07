from proper_new import gen_app


def _assert_structure(root):
    assert (root / "static").is_dir()
    assert (root / "static" / "css").is_dir()
    assert (root / "static" / "css" / "not-found-page.css").exists()

    assert (root / "myapp" / "config").is_dir()
    assert (root / "myapp" / "controllers").is_dir()
    assert (root / "myapp" / "forms").is_dir()
    assert (root / "myapp" / "models").is_dir()
    assert (root / "myapp" / "views").is_dir()

    assert (root / "myapp" / "main.py").exists()
    assert (root / "myapp" / "router.py").exists()


def test_gen_app(tmp_path):
    name = "myapp"
    root = tmp_path / name
    gen_app(root, force=True, install_deps=False)

    _assert_structure(root)


def test_gen_app_custom(tmp_path):
    name = "myapp"
    root = tmp_path / "project"
    gen_app(root, name=name, force=True, install_deps=False)

    _assert_structure(root)

