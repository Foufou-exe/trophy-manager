from flask import Flask, render_template, request, jsonify
from manager import *
import subprocess

app = Flask(__name__, template_folder="web")


@app.route("/", methods=["GET"])
def getGameAdded():
    GameAdded = showGameAdded()
    return render_template("index.html", GameAdded=GameAdded)


@app.route("/", methods=["POST"])
def getSearchedGame():
    if request.form["search"] != "":
        text = str(request.form["search"])
        gamesearch = showSearchedGameFromPage("", "", "", text, "", 1)
        nbrPage = getNombrePageJeu("", "", "", text, "")
        return render_template("search.html", gamesearch=gamesearch, nbrPage=nbrPage)
    else:
        return render_template("returnMainMenu.html")


@app.route("/add", methods=["GET"])
def addGameSearch():
    if request.args.get("add") != "":
        addSearchedGame(request.args.get("add"))
        return render_template("returnMainMenu.html")
    else:
        return render_template("returnMainMenu.html")


@app.route("/remove", methods=["GET"])
def RemoveGameSearch():
    if request.args.get("GameUID") != "":
        removeGameAddedFromGameUID(request.args.get("GameUID"))
        return render_template("returnMainMenu.html")
    else:
        return render_template("returnMainMenu.html")


@app.route("/update", methods=["GET"])
def updateGameSearch():
    if request.args.get("update") != "":
        updateTropheeFromID(request.args.get("update"))
        if request.args.get("affichage") == "1":
            game = showGameSelected(request.args.get("GameUID"))
            return render_template(
                "show.html", game=game, str=str, affichage=1, bool=bool
            )
        elif request.args.get("affichage") == "0":
            game = showGameSelected(request.args.get("GameUID"))
            return render_template(
                "show.html", game=game, str=str, affichage=0, bool=bool
            )
        else:
            game = showGameSelected(request.args.get("GameUID"))
            return render_template(
                "show.html", game=game, str=str, affichage=2, bool=bool
            )
    else:
        return render_template("returnMainMenu.html")


@app.route("/show", methods=["GET"])
def showGame():
    if type(request.args.get("GameUID")) != type(None):
        if request.args.get("affichage") == "1":
            game = showGameSelected(request.args.get("GameUID"))
            return render_template(
                "show.html", game=game, str=str, affichage=1, bool=bool
            )
        elif request.args.get("affichage") == "0":
            game = showGameSelected(request.args.get("GameUID"))
            return render_template(
                "show.html", game=game, str=str, affichage=0, bool=bool
            )
        else:
            game = showGameSelected(request.args.get("GameUID"))
            return render_template(
                "show.html", game=game, str=str, affichage=2, bool=bool
            )
    else:
        return render_template("returnMainMenu.html")



if __name__ == "__main__":
    subprocess.call(["python", "InitDB.py"])
    app.run(host="0.0.0.0", port=5600)
