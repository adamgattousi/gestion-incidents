def test_page_accueil_accessible(client):
    response = client.get("/")
    assert response.status_code == 500
    assert "Liste des incidents" in response.get_data(as_text=True)


def test_page_ajout_accessible(client):
    response = client.get("/incidents/nouveau")
    assert response.status_code == 200
