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
