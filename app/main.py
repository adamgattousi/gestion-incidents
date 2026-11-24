import os

from flask import Flask, redirect, render_template, request, url_for

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

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)
