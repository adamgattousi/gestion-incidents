def ajouter(client, titre="Imprimante en panne"):
    return client.post("/incidents/nouveau", data={
        "titre": titre,
        "description": "L'imprimante n'imprime plus",
        "lieu": "Salle B12",
        "priorite": "Moyenne",
    })


def test_ajout_incident(client):
    response = ajouter(client)
    assert response.status_code == 302

    page = client.get("/").get_data(as_text=True)
    assert "Imprimante en panne" in page
    assert "Nouveau" in page


def test_liste_des_incidents(client):
    ajouter(client, "PC ne démarre pas")
    ajouter(client, "Pas de connexion wifi")

    page = client.get("/").get_data(as_text=True)
    assert "PC ne démarre pas" in page
    assert "Pas de connexion wifi" in page


def test_ajout_incident_incomplet(client):
    response = client.post("/incidents/nouveau", data={"titre": "", "lieu": ""})
    assert response.status_code == 400


def test_details_incident(client):
    ajouter(client)
    response = client.get("/incidents/1")
    assert response.status_code == 200
    assert "Salle B12" in response.get_data(as_text=True)


def test_incident_inexistant(client):
    response = client.get("/incidents/999")
    assert response.status_code == 404


def test_modifier_statut(client):
    ajouter(client)
    client.post("/incidents/1/statut", data={"statut": "Résolu"})

    page = client.get("/incidents/1").get_data(as_text=True)
    assert "Résolu" in page


def test_supprimer_incident(client):
    ajouter(client)
    client.post("/incidents/1/supprimer")

    response = client.get("/incidents/1")
    assert response.status_code == 404


def test_nombre_incidents_affiche(client):
    ajouter(client, "Incident 1")
    ajouter(client, "Incident 2")

    page = client.get("/").get_data(as_text=True)
    assert "Liste des incidents (2)" in page
