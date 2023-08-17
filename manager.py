from RequestTrophee import *
from InitDB import *
import random


def generate_uid():
    """
    Generate a unique ID for a game and trophy.

    Returns:
    int: A random integer between 10000000 and 99999999.
    """
    return random.randint(10000000, 99999999)


def removeGameAddedFromGameUID(GameUID):
    """
    Remove a game from the database based on its unique ID.

    Args:
    GameUID (int): The unique ID of the game to be removed.
    """
    removeGameInfoFromGameUID(GameUID)
    removeMainTropheeFromGameUID(GameUID)
    removeDLCTropheeFromGameUID(GameUID)


def showGameAdded() -> list:
    """
    Retrieve information about all games in the database.

    Returns:
    list: A list of dictionaries, where each dictionary contains information about a game.
    """
    Games = []
    for game in getAllGame():
        GameTemp = {}
        GameTemp["GameUID"] = game["GameUID"]
        GameTemp["pochette"] = game["Pochette"]
        GameTemp["URl"] = game["URL"]
        GameTemp["Titre"] = game["Titre"]
        GameTemp["DLC"] = game["DLC"]
        GameTemp["Console"] = game["Console"]
        GameTemp["Extra"] = game["Extra"]
        GameTemp["VR"] = game["VR"]
        GameTemp["PlatinePossible"] = game["PlatinePossible"]
        GameTemp["TropheePlatine"] = game["TropheePlatine"]
        GameTemp["TropheeGold"] = game["TropheeGold"]
        GameTemp["TropheeSilver"] = game["TropheeSilver"]
        GameTemp["TropheeBronze"] = game["TropheeBronze"]
        Games.append(GameTemp)
    return Games


def showSearchedGameFromPage(console, order, direction, qquery, letters, page) -> list:
    """
    Retrieve information about games that match a search query.

    Args:
    console (str): The console to search for (e.g. "ps4").
    order (str): The order in which to display the results (e.g. "proche").
    direction (str): The direction in which to display the results (e.g. "ASC").
    qquery (str): The search query.
    letters (str): The letters to search for.
    page (int): The page number of the search results.

    Returns:
    list: A list of dictionaries, where each dictionary contains information about a game.
    """
    return getGames(console, order, direction, qquery, letters, page)


def getNombrePageJeu(console, order, direction, qquery, letters) -> int:
    """
    Retrieve the number of pages of search results for a given search query.

    Args:
    console (str): The console to search for (e.g. "ps4").
    order (str): The order in which to display the results (e.g. "proche").
    direction (str): The direction in which to display the results (e.g. "ASC").
    qquery (str): The search query.
    letters (str): The letters to search for.

    Returns:
    int: The number of pages of search results.
    """
    return getNombrePageJeuRechercher(console, order, direction, qquery, letters)


def showSearchedGame(url) -> dict:
    """
    Retrieve information about a game based on its URL.

    Args:
    url (str): The URL of the game.

    Returns:
    dict: A dictionary containing information about the game.
    """
    return getGame(url)


def showAllSearchedGame(console, order, direction, qquery, letters) -> list:
    """
    Retrieve information about all games that match a search query.

    Args:
    console (str): The console to search for (e.g. "ps4").
    order (str): The order in which to display the results (e.g. "proche").
    direction (str): The direction in which to display the results (e.g. "ASC").
    qquery (str): The search query.
    letters (str): The letters to search for.

    Returns:
    list: A list of dictionaries, where each dictionary contains information about a game.
    """
    searchedGames = []
    for i in range(
        getNombrePageJeuRechercher(console, order, direction, qquery, letters)
    ):
        searchedGames.extend(getGames("ps4", "proche", "ASC", "io", "", i + 1))
    return searchedGames


def addSearchedGame(url):
    """
    Add a game to the database based on its URL.

    Args:
    url (str): The URL of the game to be added.
    """
    Game = getGame(url)
    GameUID = generate_uid()
    addGameInfo(
        GameUID,
        Game["pochette"],
        Game["URL"],
        Game["titre"],
        Game["TropheePlatine"],
        Game["TropheeGold"],
        Game["TropheeSilver"],
        Game["TropheeBronze"],
        Game["console"],
        Game["VR"],
        Game["PlatinePossible"],
        Game["Extra"],
        Game["Difficulte"],
        Game["NoteJeu"],
        Game["DateSortie"],
        Game["Genre"],
        Game["Territoire"],
        Game["nbrTropheeTotal"],
        Game["nbrTropheeOnline"],
        Game["nbrTropheeCacher"],
        Game["DLC"],
        Game["Pourcent"],
    )
    for dictTropheeMain in Game["Trophee"]["main"]["data"]:
        addMainTrophee(
            GameUID,
            dictTropheeMain["nom"],
            dictTropheeMain["description"],
            dictTropheeMain["trophee"],
            dictTropheeMain["pourcentage"],
            dictTropheeMain["image"],
            generate_uid(),
            0,
        )
    for i in range(int(Game["DLC"])):
        for dictTropheeDLC in Game["Trophee"]["DLC" + str(i + 1)]["data"]:
            addDLCTrophee(
                GameUID,
                i + 1,
                dictTropheeDLC["nom"],
                dictTropheeDLC["description"],
                dictTropheeDLC["trophee"],
                dictTropheeDLC["pourcentage"],
                dictTropheeDLC["image"],
                generate_uid(),
                0,
            )


def showGameSelected(GameUID) -> dict:
    """
    Retrieve information about a game based on its unique ID.

    Args:
    GameUID (int): The unique ID of the game.

    Returns:
    dict: A dictionary containing information about the game and its trophies.
    """
    # game info
    Game = getGameInfoFromGameUID(GameUID)

    # thophee main
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

    # trophee DLC
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


# ================================update trophee by ID================================#
def updateTropheeFromID(id):
    updateMainTropheeFromID("true", id)
    updateDLCTropheeFromID("true", id)


# print(showGameAdded())
# removeGameAddedFromGameUID(20340397)

# print(showSearchedGameFromPage("ps4", "proche", "ASC", "io", "", 1))
# print(showAllSearchedGame("ps4", "proche", "ASC", "io", ""))
# addSearchedGame("https://www.psthc.fr/unjeu/tom-clancy-ghost-recon-wildlands-ps4/liste-trophees.htm")
# print(showGameSelected(52273458))
# updateTropheeFromID(15603316)
