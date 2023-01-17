from RequestTrophee import *
from InitDB import *
import random

#================================generate UID for game and id trophee================================#
def generate_uid():
    return random.randint(10000000, 99999999)
#================================remove game added================================#
def removeGameAddedFromGameUID(GameUID):
    removeGameInfoFromGameUID(GameUID)
    removeMainTropheeFromGameUID(GameUID)
    removeDLCTropheeFromGameUID(GameUID)

#---------------------------Menu principal-------------------------------------#
#================================show game added================================#
def showGameAdded() -> list:
    Games = [] 
    for game in getAllGame():
        GameTemp = {}
        GameTemp["GameUID"] = game['GameUID']
        GameTemp["pochette"] = game['Pochette']
        GameTemp["URl"] = game['URL']
        GameTemp["Titre"] = game['Titre']
        GameTemp["DLC"] = game['DLC']
        GameTemp["Console"] = game['Console']
        GameTemp["Extra"] = game['Extra']
        GameTemp["VR"] = game['VR']
        GameTemp["PlatinePossible"] = game['PlatinePossible']
        GameTemp["TropheePlatine"] = game['TropheePlatine']
        GameTemp["TropheeGold"] = game['TropheeGold']
        GameTemp["TropheeSilver"] = game['TropheeSilver']
        GameTemp["TropheeBronze"] = game['TropheeBronze']
        Games.append(GameTemp)
    return Games

#---------------------------Menu recherche-------------------------------------#
#================================show game recherche from page================================#
def showSearchedGameFromPage(console, order, direction, qquery, letters, page) -> list:
    return getGames(console, order, direction, qquery, letters, page)
def getNombrePageJeu(console, order, direction, qquery, letters) -> int:
    return getNombrePageJeuRechercher(console, order, direction, qquery, letters)
def showSearchedGame(url) -> dict:
    return getGame(url)

#================================show all game recherche================================#
def showAllSearchedGame(console, order, direction, qquery, letters) -> list:
    searchedGames = []
    for i in range(getNombrePageJeuRechercher(console, order, direction, qquery, letters)):
        searchedGames.extend(getGames("ps4", "proche", "ASC", "io", "", i+1))
    return searchedGames
#================================add game searched================================#
def addSearchedGame(url):
    Game = getGame(url)
    GameUID = generate_uid()
    addGameInfo(GameUID, Game["pochette"], Game["URL"], Game["titre"], Game["TropheePlatine"], Game["TropheeGold"], Game["TropheeSilver"], Game["TropheeBronze"], Game["console"], Game["VR"], Game["PlatinePossible"], Game["Extra"], Game["Difficulte"], Game["NoteJeu"], Game["DateSortie"], Game["Genre"], Game["Territoire"], Game["nbrTropheeTotal"], Game["nbrTropheeOnline"], Game["nbrTropheeCacher"], Game["DLC"], Game["Pourcent"])
    for dictTropheeMain in Game["Trophee"]["main"]["data"]:
        addMainTrophee(GameUID, dictTropheeMain["nom"], dictTropheeMain["description"], dictTropheeMain["trophee"], dictTropheeMain["pourcentage"], dictTropheeMain["image"], generate_uid(), 0)
    for i in range(int(Game["DLC"])):
        for dictTropheeDLC in Game["Trophee"]["DLC"+str(i+1)]["data"]:
            addDLCTrophee(GameUID, i+1, dictTropheeDLC["nom"], dictTropheeDLC["description"], dictTropheeDLC["trophee"], dictTropheeDLC["pourcentage"], dictTropheeDLC["image"], generate_uid(), 0)

#---------------------------Menu du jeu-------------------------------------#
#================================show game recherche from page================================#
def showGameSelected(GameUID) -> dict:
    #game info
    Game = getGameInfoFromGameUID(GameUID)

    #thophee main
    nbrPlatine = 0
    nbrGold = 0
    nbrSilver = 0
    nbrBronze = 0
    mainTrophee = []
    for trophee in getAllMainTropheeFromGameUID(GameUID):
        if trophee["Trophee"] == "bronze":
            nbrBronze += 1
        elif trophee["Trophee"] == "argent":
            nbrSilver += 1
        elif trophee["Trophee"] == "gold":
            nbrGold += 1
        elif trophee["Trophee"] == "platine":
            nbrPlatine += 1
        mainTrophee.append(trophee)
    Game["Trophee"] = {}
    Game["Trophee"]["main"] = {}
    Game["Trophee"]["main"]["nbr"] = {}
    Game["Trophee"]["main"]["nbr"]["TropheePlatine"] = nbrPlatine
    Game["Trophee"]["main"]["nbr"]["TropheeGold"] = nbrGold
    Game["Trophee"]["main"]["nbr"]["TropheeSilver"] = nbrSilver
    Game["Trophee"]["main"]["nbr"]["TropheeBronze"] = nbrBronze
    Game["Trophee"]["main"]["data"] = mainTrophee

    #trophee DLC
    DLC = {}
    for tropheeDLC in getAllDLCTropheeFromGameUID(GameUID):
        if "DLC" + str(tropheeDLC["numDLC"]) not in DLC:
            DLC["DLC" + str(tropheeDLC["numDLC"])] = {}
            DLC["DLC" + str(tropheeDLC["numDLC"])]["nbr"] = {}
            DLC["DLC" + str(tropheeDLC["numDLC"])]["nbr"]["TropheePlatine"] = 0
            DLC["DLC" + str(tropheeDLC["numDLC"])]["nbr"]["TropheeGold"] = 0
            DLC["DLC" + str(tropheeDLC["numDLC"])]["nbr"]["TropheeSilver"] = 0
            DLC["DLC" + str(tropheeDLC["numDLC"])]["nbr"]["TropheeBronze"] = 0
            DLC["DLC" + str(tropheeDLC["numDLC"])]["data"] = []
            DLC["DLC" + str(tropheeDLC["numDLC"])]["data"].append(tropheeDLC)
            if tropheeDLC["Trophee"] == "bronze":
                DLC["DLC" + str(tropheeDLC["numDLC"])]["nbr"]["TropheeBronze"] += 1
            elif tropheeDLC["Trophee"] == "argent":
                DLC["DLC" + str(tropheeDLC["numDLC"])]["nbr"]["TropheeSilver"] += 1
            elif tropheeDLC["Trophee"] == "gold":
                DLC["DLC" + str(tropheeDLC["numDLC"])]["nbr"]["TropheeGold"] += 1
            elif tropheeDLC["Trophee"] == "platine":
                DLC["DLC" + str(tropheeDLC["numDLC"])]["nbr"]["TropheePlatine"] += 1
        else:
            DLC["DLC" + str(tropheeDLC["numDLC"])]["data"].append(tropheeDLC)
            if tropheeDLC["Trophee"] == "bronze":
                DLC["DLC" + str(tropheeDLC["numDLC"])]["nbr"]["TropheeBronze"] += 1
            elif tropheeDLC["Trophee"] == "argent":
                DLC["DLC" + str(tropheeDLC["numDLC"])]["nbr"]["TropheeSilver"] += 1
            elif tropheeDLC["Trophee"] == "gold":
                DLC["DLC" + str(tropheeDLC["numDLC"])]["nbr"]["TropheeGold"] += 1
            elif tropheeDLC["Trophee"] == "platine":
                DLC["DLC" + str(tropheeDLC["numDLC"])]["nbr"]["TropheePlatine"] += 1
    tempdict = Game["Trophee"]
    tempdict.update(DLC)
    Game["Trophee"] = tempdict
    return Game
#================================update trophee by ID================================#
def updateTropheeFromID(id):
    updateMainTropheeFromID('true', id)
    updateDLCTropheeFromID('true', id)

# print(showGameAdded())
# removeGameAddedFromGameUID(20340397)

# print(showSearchedGameFromPage("ps4", "proche", "ASC", "io", "", 1))
# print(showAllSearchedGame("ps4", "proche", "ASC", "io", ""))
# addSearchedGame("https://www.psthc.fr/unjeu/tom-clancy-ghost-recon-wildlands-ps4/liste-trophees.htm")
# print(showGameSelected(52273458))
# updateTropheeFromID(15603316)