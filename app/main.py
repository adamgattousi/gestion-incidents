import os

from flask import Flask, abort, redirect, render_template, request, url_for

from app import database

PRIORITES = ["Faible", "Moyenne", "Élevée"]
STATUTS = ["Nouveau", "En cours", "Résolu"]


def create_app(db_path=None):
    app = Flask(__name__)

    # en local : data/incidents.db, dans Docker on peut changer avec DATABASE_PATH
    db = db_path or os.environ.get("DATABASE_PATH", "data/incidents.db")
    database.init_db(db)

    @app.route("/")
    def index():
        incidents = database.get_all_incidents(db)
        return render_template("index.html", incidents=incidents)

    @app.route("/incidents/nouveau", methods=["GET", "POST"])
    def nouvel_incident():
        if request.method == "POST":
            titre = request.form.get("titre", "").strip()
            description = request.form.get("description", "").strip()
            lieu = request.form.get("lieu", "").strip()
            priorite = request.form.get("priorite", "Faible")

            if not titre or not description or not lieu or priorite not in PRIORITES:
                erreur = "Veuillez remplir tous les champs."
                return render_template("nouveau.html", priorites=PRIORITES, erreur=erreur), 400

            database.add_incident(db, titre, description, lieu, priorite)
            return redirect(url_for("index"))

        return render_template("nouveau.html", priorites=PRIORITES)

    @app.route("/incidents/<int:incident_id>")
    def details(incident_id):
        incident = database.get_incident(db, incident_id)
        if incident is None:
            abort(404)
        return render_template("details.html", incident=incident, statuts=STATUTS)

    @app.route("/incidents/<int:incident_id>/statut", methods=["POST"])
    def changer_statut(incident_id):
        statut = request.form.get("statut")
        if statut not in STATUTS:
            abort(400)
        database.update_statut(db, incident_id, statut)
        return redirect(url_for("details", incident_id=incident_id))

    @app.route("/incidents/<int:incident_id>/supprimer", methods=["POST"])
    def supprimer(incident_id):
        database.delete_incident(db, incident_id)
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)
