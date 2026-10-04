from wardrobe_ai import create_app


def test_health_endpoint(monkeypatch, tmp_path) -> None:
    data_dir = tmp_path / "wardrobe"
    monkeypatch.setenv("WARDROBE_DATA_DIR", str(data_dir))
    app = create_app()
    app.config["TESTING"] = True

    response = app.test_client().get("/health")

    assert response.status_code == 200
    assert response.is_json
    assert response.json == {"status": "ok"}
    assert app.config["DATA_DIR"] == data_dir
    assert not data_dir.exists()
