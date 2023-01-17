# Ce fichier est le module Requester c'est celui qui gere les recherche sur le site en question
# Voici les function qui son connue dans ce fichier
    # getGames est une fonction qui va permettre de nous reourner une list qui contiendra tout les jeux concerner par notre recherche
    # getGame est une fonction qui permet de charger tous les elements relatif a une jeu a partir de son URL
    # getNombreJeuxRechercher est une fonction qui va permettre de nous reourner le nombre de resultat de notre recherche
    # getImportantLinks est une fonction qui va permettre de nous reourner une dictionnaire qui contiendra les liens importants du jeu

import requests
from bs4 import BeautifulSoup
from lxml import etree


#Par erreur les developpeur on laisser les requete ajax passer par le GET, on exploite ceci pour lister les games
#Voici la liste des options get que l'on peux passer et que l'on utilise (les plus importants a connaitre):
#ajax=ajax -> cette option designe que la requete et executer en ajax


#===============================descrition de la function getGames=======================================================#
#getGames est une fonction qui va permettre de nous reourner une list qui contiendra tout les jeux concerner par notre recherche
#----------------------------------------------------------------
#arguments de l'entree
    # console -> La console que l'on recherche
        # - toutes = toutes les consoles
        # - [ps3,ps4,ps5,vita,psvr,psnow,impossible] = selecteur de console que l'on peux cumuler ou appeler seul par exemple pour chercher PS4 et PS3 : ps3ps4
    # order -> tri par orde 
        # - proche = par pertinence
        # - nouveau = par nouveauter
        # - alpha = par ordre alphabetique
        # - populaire = par populariter
        # - notetest = par la note attribuer par la communauté du site
    # direction -> tri le order par ordre croissant ou non
        # - ASC = tri l'ordre par croissance
        # - DESC = tri l'ordre par decroissance
        # exemple si tri par alphabetique et ASC alors les jeux sont trier du A au Z
        # exmeple si tri par populariter et DESC alors les jeux sont trier du moins connue au plus connue
    # qquery -> le nom du jeu rechercher
    # letters
        # -  = aucun filtre de début
        # - 9 = commence par un chiffre
        # - [a-z] = commmence par la ou les lettre selectionner
        # exemple az alors les jeux afficher commence par a ou z
    #page -> c'est la page sur laquelle on se trouve, on peux afficher 50 jeux par page
        #si la page demander est superieur aux nobre de page, un liste avec un seul element null sera envoyée
#----------------------------------------------------------------
#format de la sorti -> list contenant
    #[titre, dispo ps plus     , nombre DLC, console, VR                , platine impossible, nbr platine, nbr gold, nbr silver, nbr bronze, note/20, dificulté/10, Pochette, URL]
    #[str  , int(O non, 1 oui) , int       , str    , int(O non, 1 oui) , int(O non, 1 oui) , int        , int     , int       , int       , Float  , float       , str     , str]
#----------------------------------------------------------------
def getGames(console = "ps4", order = "proche", direction = "ASC", qquery = "", letters = "", page = 1) -> list:
    headers = {
        "Host": "www.psthc.fr",
        "User-Agent": "Mozilla/5.0",
        "Content-Length": "0"
    }
    mode = "games"
    nbrJeux = getNombreJeuxRechercher(console, order, direction, qquery, letters)
    if (nbrJeux%50) > 0:
        nbrPage = int(nbrJeux/50)+1
    else :
        nbrPage = int(nbrJeux/50)
    if page > 0 and page <= nbrPage:
        offset = (page-1) * 50
    elif page > nbrPage:
        offset = (nbrPage-1) * 50
    else:
        offset = 0
    getValue = f"&mode={mode}&qquery={qquery}&console={console}&letters={letters}&order={order}&direction={direction}&offset={offset}"
    url = f"https://www.psthc.fr/recherche-avancee.htm?ajax=ajax{getValue}"
    soup = BeautifulSoup(requests.get(url, headers=headers).content, "lxml")

    allGames = soup.find_all('div', attrs={'class': 'horizontal-game-block'})
    gamesFind = []
    for game in allGames:
        gameFind = {}

        #Premiere section
        startHead = game.find('div', attrs={'class': 'game-name'})
        bottomHead = game.find('div', attrs={'class': 'game-right'})
        URLHead = game.find_all('a')[0]
        #tri de l'entete avec les element "game-name"
        startHeadSectionDiv = startHead.find_all('div')
        startHeadSectionImg = startHead.find_all('img')
        #tri de l'entete avec les element "game-right"
        bottomHeadSectionDiv = bottomHead.find_all('div')
        bottomHeadSectionA = bottomHead.find_all('a')

#=============================game-name===================================#
        #ajout du titre
        gameFind["titre"] = str(startHead.find('h3')).split("<h3>")[1].split("</h3>")[0].replace('\n', '')
        #Ajout du ps extra
        indexExtra = [startHeadSectionDiv.index(index) for index in startHeadSectionDiv if "Extra" in index]
        if(len(indexExtra) > 0):
            gameFind["Extra"] = 1
            del startHeadSectionDiv[indexExtra[0]]
        else:
            gameFind["Extra"] = 0
        #Ajout du DLC
        indexDLC = [startHeadSectionDiv.index(index) for index in startHeadSectionDiv if "DLC" in str(index)]
        if(len(indexDLC) > 0):
            gameFind["DLC"] = int(str(startHeadSectionDiv[indexDLC[0]]).split(">")[1].split("<")[0].replace(' DLC', ''))
            del startHeadSectionDiv[indexDLC[0]]
        else:
            gameFind["DLC"] = 0
        #Ajout du Console
        if len(startHeadSectionDiv) > 1:
            finalConsole = ""
            for cons in startHeadSectionDiv:
                if finalConsole == "":
                    finalConsole += str(cons).split(">")[1].split("<")[0]
                else:
                    finalConsole += ", " + str(cons).split(">")[1].split("<")[0]
            gameFind["console"] = finalConsole
        else:
            gameFind["console"] = str(startHeadSectionDiv[0]).split(">")[1].split("<")[0]
        startHeadSectionDiv = []
        #Ajout VR jeux
        indexVR = [startHeadSectionImg.index(index) for index in startHeadSectionImg if "VR" in str(index)]
        if(len(indexVR) > 0):
            gameFind["VR"] = 1
        else:
            gameFind["VR"] = 0
        #Ajout platine impossible
        indexImpossible = [startHeadSectionImg.index(index) for index in startHeadSectionImg if "impossible" in str(index)]
        if(len(indexImpossible) > 0):
            gameFind["PlatinePossible"] = 1
        else:
            gameFind["PlatinePossible"] = 0

#=============================game-right===================================#
        #trophee platine
        indexPlatine = [bottomHeadSectionDiv.index(index) for index in bottomHeadSectionDiv if "platine" in str(index)]
        gameFind["TropheePlatine"] = int(str(bottomHeadSectionDiv[indexPlatine[0]]).split(">")[1].split("<")[0])
        #trophee Gold
        indexGold = [bottomHeadSectionDiv.index(index) for index in bottomHeadSectionDiv if "gold" in str(index)]
        gameFind["TropheeGold"] = int(str(bottomHeadSectionDiv[indexGold[0]]).split(">")[1].split("<")[0])
        #trophee Silver
        indexSilver = [bottomHeadSectionDiv.index(index) for index in bottomHeadSectionDiv if "silver" in str(index)]
        gameFind["TropheeSilver"] = int(str(bottomHeadSectionDiv[indexSilver[0]]).split(">")[1].split("<")[0])
        #trophee Bronze
        indexBronze = [bottomHeadSectionDiv.index(index) for index in bottomHeadSectionDiv if "bronze" in str(index)]
        gameFind["TropheeBronze"] = int(str(bottomHeadSectionDiv[indexBronze[0]]).split(">")[1].split("<")[0])
        #Note du jeu
        testNote = [bottomHeadSectionA.index(index) for index in bottomHeadSectionA if "test-note" in str(index)]
        if(len(testNote) > 0):
            gameFind["NoteJeu"] = float(str(bottomHeadSectionA[testNote[0]]).replace('\n','').split('>')[1].split('<')[0])
        else:
            gameFind["NoteJeu"] = float(0)
        #Difficulte
        dificulte = [bottomHeadSectionA.index(index) for index in bottomHeadSectionA if "guide-note" in str(index)]
        if(len(dificulte) > 0):
            gameFind["Difficulte"] = float(str(bottomHeadSectionA[dificulte[0]]).replace('\n','').split('>')[1].split('<')[0])
        else:
            gameFind["Difficulte"] = float(0)
        gamesFind.append(gameFind)

#=============================link===================================#
        #url game
        gameFind["URL"] = "https://www.psthc.fr" + str(URLHead).split('>')[0].split('?')[0].split('href="')[1]
        #url pochette
        gameFind["pochette"] = str(URLHead).split("url('")[1].split("')")[0]
    return gamesFind


#===============================descrition de la function getGame=======================================================#
#getGame est une fonction qui permet de charger tous les elements relatif a une jeu a partir de son URL
#----------------------------------------------------------------
#arguments de l'entree
    # url -> c'est l'URL du jeu que lon charge
#----------------------------------------------------------------
#format de la sorti -> dictionaire avec
#key                    #value
                     
#GameUID                #UID du jeu                     
#pochette               #Url de la pochette du jeu
#URl                    #URL du jeu
#titre                  #Titre complet du jeu
#TropheePlatine         #nombre de trophee platine
#TropheeGold            #nombre de trophee gold
#TropheeSilver          #nombre de trophee silver
#TropheeBronze          #nombre de trophee bronze
#console                #affiche les consoles compatible avec le jeu
#VR                     #indique si le jeu est disponoble en VR
#PlatinePossible        #indique si le trophee platine est realisable
#Extra                  #indique si le jeu est disponible avec le PSPlus
#Difficulte             #affiche la difficulté du jeu
#NoteJeu                #affiche une note du jeu
#DateSortie             #affiche la date de sortie du jeu
#Genre                  #affiche le ou les genre(s) du jeu
#Territoire             #affiche le territoire de disponibilité du jeu
#nbrTropheeTotal        #indique le nombre de trophee total
#nbrTropheeOnline       #indique le nombre de trophee total en ligne
#nbrTropheeCacher       #indique le nombre de trophee total caché
#DLC                    #indique le nombre de DLC du jeu

# Pour la gestion de la liste des trophee du jeu principal est des DLC nous les gerons avec des dictionnaire contenue sur la key "Trophee" du dicionnaire game
#     dictionnaire main
#         key             value
#         nbr             affiche une dictionnaire avec le nombre total des type de trophee(gold, sivler, etc...)
#         data            affiche une list contenant un dictionnaire pour chaque trophee -> (nom, trophee, pourcentage, image, description)
    
#     dictionnaire DLC{+numeroDLC}
#         key             value
#         nbr             affiche une dictionnaire avec le nombre total des type de trophee(gold, sivler, etc...)
#         data            affiche une list contenant un dictionnaire pour chaque trophee -> (nom, trophee, pourcentage, image, description)
#----------------------------------------------------------------
def getGame(url) -> dict:
    headers = {
        "Host": "www.psthc.fr",
        "User-Agent": "Mozilla/5.0",
        "Content-Length": "0"
    }
    Game = {}
    soup = BeautifulSoup(requests.get(url, headers=headers).content, "lxml")
    allGames = soup.find('div', attrs={'class': 'content'})
    
    #Premiere section
    startHead = allGames.find('div', attrs={'id': 'game-header-1'})
    middleHead = allGames.find('div', attrs={'id': 'game-header-2'})
    TropheeList = allGames.find('div', attrs={'id': 'game-guide'})
    #tri de l'entete avec les element "game-header-1"
    startHeadGameCenter = startHead.find('div', attrs={'class': 'game-center'})
    startHeadGameCenterTrophee = startHead.find('div', attrs={'class': 'game-trophies'})
    startHeadGameCenterImg = startHeadGameCenter.find_all('img')
    startHeadGameNote = startHead.find('div', attrs={'id': 'game-notes'})
    #tri de l'entete avec les element "game-header-2"
    middleHeadLeft = middleHead.find('div', attrs={'class': 'left'})
    middleHeadLeftBR = str(middleHeadLeft).split("<br/>")

#=============================game-header-1===================================#
    #Ajout de la pochette
    Game["pochette"] = str(startHead.find('div', attrs={'class': 'game-picture-container'})).split("url('")[1].split("')")[0]
    #Ajout de l'URL
    Game["URL"] = str(url)
    #Ajout du titre
    Game["titre"] = str(startHeadGameCenter.find('h1')).split(">")[1].split("<")[0]
    #Ajout des trophee platine
    if type(startHeadGameCenterTrophee.find('div', attrs={'class': 'platine'})) != type(None) :
        Game["TropheePlatine"] = str(startHeadGameCenterTrophee.find('div', attrs={'class': 'platine'})).split(">")[1].split("<")[0]
    else:
        Game["TropheePlatine"] = 0
    #Ajout des trophee Gold
    if type(startHeadGameCenterTrophee.find('div', attrs={'class': 'gold'})) != type(None) :
        Game["TropheeGold"] = str(startHeadGameCenterTrophee.find('div', attrs={'class': 'gold'})).split(">")[1].split("<")[0]
    else:
        Game["TropheeGold"] = 0
    #Ajout des trophee Silver
    if type(startHeadGameCenterTrophee.find('div', attrs={'class': 'silver'})) != type(None) :
        Game["TropheeSilver"] = str(startHeadGameCenterTrophee.find('div', attrs={'class': 'silver'})).split(">")[1].split("<")[0]
    else:
        Game["TropheeSilver"] = 0
    #Ajout des trophee Bronze
    if type(startHeadGameCenterTrophee.find('div', attrs={'class': 'bronze'})) != type(None) :
        Game["TropheeBronze"] = str(startHeadGameCenterTrophee.find('div', attrs={'class': 'bronze'})).split(">")[1].split("<")[0]
    else:
        Game["TropheeBronze"] = 0
    #Ajout des consoles
    FinalConsole = ""
    for cons in startHeadGameCenter.find_all('div', attrs={'class': 'jeu-pf'}):
        if str(cons).split(">")[1].split("<")[0] != "Extra":
            if FinalConsole == "":
                FinalConsole += str(cons).split(">")[1].split("<")[0]
            else:
                FinalConsole += "," + str(cons).split(">")[1].split("<")[0]
    Game["console"] = FinalConsole
    #Ajout des VR
    indexVR = [startHeadGameCenterImg.index(index) for index in startHeadGameCenterImg if "VR" in str(index)]
    if(len(indexVR) > 0):
        Game["VR"] = 1
    else:
        Game["VR"] = 0
    #Ajout des platine impossible
    indexImpossible = [startHeadGameCenterImg.index(index) for index in startHeadGameCenterImg if "impossible" in str(index)]
    if(len(indexImpossible) > 0):
        Game["PlatinePossible"] = 1
    else:
        Game["PlatinePossible"] = 0
    #Ajout des Extra
    for cons in startHeadGameCenter.find_all('div', attrs={'class': 'jeu-pf'}):
        if str(cons).split(">")[1].split("<")[0] == "Extra":
            Game["Extra"] = 1
        else:
            Game["Extra"] = 0
    #Ajout des Difficulte
    try:
        Game["Difficulte"] = float(str(startHeadGameNote.find('div', attrs={'class': 'guide-note'})).split(">")[1].split("<")[0])
    except:
        Game["Difficulte"] = float(0)
    #Ajout des note
    try:
        Game["NoteJeu"] = float(str(startHeadGameNote.find('div', attrs={'class': 'test-note'})).split(">")[1].split("<")[0])
    except:
        Game["NoteJeu"] = float(0)
    
#=============================game-header-2===================================#
    
    #Ajout date de sortie
    sortie = [middleHeadLeftBR.index(index) for index in middleHeadLeftBR if "Date de sortie" in str(index)]
    if(len(sortie) > 0):
        Game["DateSortie"] = str(middleHeadLeftBR[sortie[0]]).split(": ")[1]
    else:
        Game["DateSortie"] = "00/00/0000"
    #Ajout du genre
    Genre = [middleHeadLeftBR.index(index) for index in middleHeadLeftBR if "Genre(s)" in str(index)]
    if(len(Genre) > 0):
        Game["Genre"] = str(middleHeadLeftBR[Genre[0]]).split(": ")[1].replace("\xa0", "")
    else:
        Game["Genre"] = ""
    #Ajout du teritoire
    Territoire = [middleHeadLeftBR.index(index) for index in middleHeadLeftBR if "Territoire(s)" in str(index)]
    if(len(Territoire) > 0):
        Game["Territoire"] = str(middleHeadLeftBR[Territoire[0]]).split(": ")[1]
    else:
        Game["Territoire"] = ""
    #Ajout du nbrTropheeTotal
    Game["nbrTropheeTotal"] = int(str(middleHeadLeft.find('div', attrs={'id': "game-total-trophies"})).split(">")[1].split(" ")[0])
    #Ajout du nbrTropheeOnline
    Game["nbrTropheeOnline"] = int(str(middleHeadLeft.find('div', attrs={'id': "game-total-online"})).split(">")[1].split(" ")[0])
    #Ajout du nbrTropheeCacher
    Game["nbrTropheeCacher"] = int(str(middleHeadLeft.find('div', attrs={'id': "game-total-hidden"})).split(">")[1].split(" ")[0])
    #Ajout du nbrDLC
    if (type(middleHeadLeft.find('div', attrs={'id': "game-total-dlc"})) is not type(None)) :
        Game["DLC"] = int(str(middleHeadLeft.find('div', attrs={'id': "game-total-dlc"})).split(">")[1].split(" ")[0])
    else :
        Game["DLC"] = 0
    Game["Pourcent"] = 0
#=============================TropheeProcess===================================#
    
    TropheeProc = {}
    mainTropheeHead = TropheeList.findAll('div', attrs={'class': 'horizontal-game-block'})
    if(len(mainTropheeHead) > 0) :
        for line in mainTropheeHead :
            if('DLC' in str(line)) :
                TropheeProcDLCNbr = {}
                TropheeProcDLCNum = int(str(line.find('h3')).split(')')[0].split('n°')[1])
                TropheeProcDLCNbr['TropheePlatine'] = int(str(line.find('div', attrs={'class': 'platine'})).split('platine">')[1].split('<')[0])
                TropheeProcDLCNbr['TropheeGold'] = int(str(line.find('div', attrs={'class': 'gold'})).split('gold">')[1].split('<')[0])
                TropheeProcDLCNbr['TropheeSilver'] = int(str(line.find('div', attrs={'class': 'silver'})).split('silver">')[1].split('<')[0])
                TropheeProcDLCNbr['TropheeBronze'] = int(str(line.find('div', attrs={'class': 'bronze'})).split('bronze">')[1].split('<')[0])
                TropheeProc['DLC'+str(TropheeProcDLCNum)] = {}
                TropheeProc['DLC'+str(TropheeProcDLCNum)]['nbr'] = TropheeProcDLCNbr

                TropheeProcDLCTrophee = {}
                TropheeProcDLCTropheeList = []
                TropheeProcDLCTropheeTemp = TropheeList.find('div', attrs={'id': 'guide-main-content-'+str(TropheeProcDLCNum)})
                TropheeProcDLCTropheeTempline = TropheeProcDLCTropheeTemp.findAll('div', attrs={'class': 'guide_line'})
                for line in TropheeProcDLCTropheeTempline :
                    TropheeProcDLCTrophee['nom'] = str(line).split('name="')[1].split('"')[0]
                    TropheeProcDLCTrophee['trophee'] = str(line).split('niveau="')[1].split('"')[0]
                    TropheeProcDLCTrophee['pourcentage'] = float(str(line).split('pourcj="')[1].split('"')[0])
                    TropheeProcDLCTrophee['image'] = str(line).split('<img class=')[1].split('src="')[1].split('"')[0]
                    TropheeProcDLCTrophee['description'] = str(line).split('guide_trophy_description">')[1].split('<')[0].replace('\n', '')
                    TropheeProcDLCTropheeCopy = TropheeProcDLCTrophee.copy()
                    TropheeProcDLCTropheeList.append(TropheeProcDLCTropheeCopy)
                    TropheeProc['DLC'+str(TropheeProcDLCNum)]['data'] = TropheeProcDLCTropheeList
            else :
                TropheeProcMainNbr = {}
                TropheeProcMainNbr['TropheePlatine'] = int(str(line.find('div', attrs={'class': 'platine'})).split('platine">')[1].split('<')[0])
                TropheeProcMainNbr['TropheeGold'] = int(str(line.find('div', attrs={'class': 'gold'})).split('gold">')[1].split('<')[0])
                TropheeProcMainNbr['TropheeSilver'] = int(str(line.find('div', attrs={'class': 'silver'})).split('silver">')[1].split('<')[0])
                TropheeProcMainNbr['TropheeBronze'] = int(str(line.find('div', attrs={'class': 'bronze'})).split('bronze">')[1].split('<')[0])
                TropheeProc['main'] = {}
                TropheeProc['main']['nbr'] = TropheeProcMainNbr

                TropheeProcMainTrophee = {}
                TropheeProcMainTropheeList = []
                TropheeProcMainTropheeTemp = TropheeList.find('div', attrs={'id': 'guide-main-content-0'})
                TropheeProcMainTropheeTempline = TropheeProcMainTropheeTemp.findAll('div', attrs={'class': 'guide_line'})
                for line in TropheeProcMainTropheeTempline :
                    TropheeProcMainTrophee['nom'] = str(line).split('name="')[1].split('"')[0]
                    TropheeProcMainTrophee['trophee'] = str(line).split('niveau="')[1].split('"')[0]
                    TropheeProcMainTrophee['pourcentage'] = float(str(line).split('pourcj="')[1].split('"')[0])
                    TropheeProcMainTrophee['image'] = str(line).split('<img class=')[1].split('src="')[1].split('"')[0]
                    TropheeProcMainTrophee['description'] = str(line).split('guide_trophy_description">')[1].split('<')[0].replace('\n', '')
                    TropheeProcMainTropheeCopy = TropheeProcMainTrophee.copy()
                    TropheeProcMainTropheeList.append(TropheeProcMainTropheeCopy)
                    TropheeProc['main']['data'] = TropheeProcMainTropheeList
    else:
        TropheeProcMainNbr = {}
        TropheeProcMainNbr['TropheePlatine'] = Game['TropheePlatine']
        TropheeProcMainNbr['TropheeGold'] = Game['TropheeGold']
        TropheeProcMainNbr['TropheeSilver'] = Game['TropheeSilver']
        TropheeProcMainNbr['TropheeBronze'] = Game['TropheeBronze']
        TropheeProc['main'] = {}
        TropheeProc['main']['nbr'] = TropheeProcMainNbr

        TropheeProcMainTrophee = {}
        TropheeProcMainTropheeList = []
        TropheeProcMainTropheeTemp = TropheeList.find('div', attrs={'id': 'guide-main-content-0'})
        TropheeProcMainTropheeTempline = TropheeProcMainTropheeTemp.findAll('div', attrs={'class': 'guide_line'})
        for line in TropheeProcMainTropheeTempline :
            TropheeProcMainTrophee['nom'] = str(line).split('name="')[1].split('"')[0]
            TropheeProcMainTrophee['trophee'] = str(line).split('niveau="')[1].split('"')[0]
            TropheeProcMainTrophee['pourcentage'] = float(str(line).split('pourcj="')[1].split('"')[0])
            TropheeProcMainTrophee['image'] = str(line).split('<img class=')[1].split('src="')[1].split('"')[0]
            TropheeProcMainTrophee['description'] = str(line).split('guide_trophy_description">')[1].split('<')[0].replace('\n', '')
            TropheeProcMainTropheeCopy = TropheeProcMainTrophee.copy()
            TropheeProcMainTropheeList.append(TropheeProcMainTropheeCopy)
            TropheeProc['main']['data'] = TropheeProcMainTropheeList
    TropheeProcCopy = TropheeProc.copy()
    Game['Trophee'] = TropheeProcCopy
    return(Game)


#===============================descrition de la function getNombreJeuxRechercher=======================================================#
#getNombreJeuxRechercher est une fonction qui va permettre de nous reourner le nombre de resultat de notre recherche
#----------------------------------------------------------------
#arguments de l'entree
    # console -> La console que l'on recherche
        # - toutes = toutes les consoles
        # - [ps3,ps4,ps5,vita,psvr,psnow,impossible] = selecteur de console que l'on peux cumuler ou appeler seul par exemple pour chercher PS4 et PS3 : ps3ps4
    # order -> tri par orde 
        # - proche = par pertinence
        # - nouveau = par nouveauter
        # - alpha = par ordre alphabetique
        # - populaire = par populariter
        # - notetest = par la note attribuer par la communauté du site
    # direction -> tri le order par ordre croissant ou non
        # - ASC = tri l'ordre par croissance
        # - DESC = tri l'ordre par decroissance
        # exemple si tri par alphabetique et ASC alors les jeux sont trier du A au Z
        # exmeple si tri par populariter et DESC alors les jeux sont trier du moins connue au plus connue
    # qquery -> le nom du jeu rechercher
    # letters
        # -  = aucun filtre de début
        # - 9 = commence par un chiffre
        # - [a-z] = commmence par la ou les lettre selectionner
        # exemple az alors les jeux afficher commence par a ou z
#----------------------------------------------------------------
#format de la sorti -> int
#----------------------------------------------------------------
def getNombreJeuxRechercher(console = "ps4", order = "proche", direction = "ASC", qquery = "", letters = "") -> int:
    headers = {
        "Host": "www.psthc.fr",
        "User-Agent": "Mozilla/5.0",
        "Content-Length": "0"
    }
    mode = "games"
    getValue = f"&mode={mode}&qquery={qquery}&console={console}&letters={letters}&order={order}&direction={direction}"
    url = f"https://www.psthc.fr/recherche-avancee.htm?ajax=ajax{getValue}"
    soup = BeautifulSoup(requests.get(url, headers=headers).content, "lxml")
    nbrGame = soup.find('div', attrs={'class': 'list-content'})
    nbrGameText = nbrGame.find('p')
    return int(str(nbrGameText).split('>')[1].split('<')[0].split(' ')[0])


#===============================descrition de la function getImportantLinks=======================================================#
#getImportantLinks est une fonction qui va permettre de nous reourner une dictionnaire qui contiendra les liens importants du jeu
#----------------------------------------------------------------
#arguments de l'entree
    # url -> c'est l'URL du jeu que lon charge
#----------------------------------------------------------------
#format de la sorti -> dictionnaire
#key                    #value
#guideURL               #URL du guide
#listURL                #URL de la liste des trophee
#testURL                #URL du test du jeu
#forum                  #URL du forum du jeu
#----------------------------------------------------------------
def getImportantLinks(url) -> dict:
    headers = {
        "Host": "www.psthc.fr",
        "User-Agent": "Mozilla/5.0",
        "Content-Length": "0"
    }
    link = {}
    soup = BeautifulSoup(requests.get(url, headers=headers).content, "lxml")
    allLinks = soup.find('div', attrs={'id': 'tab-bar'})
    allLinksClear = allLinks.findAll('a', attrs={'class': 'tab-bar-item'})
    for linkItem in allLinksClear :
        if("guide-trophees" in str(linkItem)) :
            link['guideURL'] = 'https://www.psthc.fr' + str(linkItem).split('href="')[1].split('?')[0]
        if("liste-trophees" in str(linkItem)) :
            link['listURL'] = 'https://www.psthc.fr' + str(linkItem).split('href="')[1].split('?')[0]
        if("test-jeu" in str(linkItem)) :
            link['testURL'] = 'https://www.psthc.fr' + str(linkItem).split('href="')[1].split('?')[0]
        if("unjeu" not in str(linkItem)) :
            link['forumURL'] = 'https://www.psthc.fr' + str(linkItem).split('href="')[1].split('?')[0]
    return(link)


#===============================descrition de la function getNombrePageJeuRechercher=======================================================#
#getNombrePageJeuRechercher est une fonction qui va permettre de nous retourner un interger du nombre de page total de la recherche
#----------------------------------------------------------------
#arguments de l'entree
    #arguments de l'entree
    # console -> La console que l'on recherche
        # - toutes = toutes les consoles
        # - [ps3,ps4,ps5,vita,psvr,psnow,impossible] = selecteur de console que l'on peux cumuler ou appeler seul par exemple pour chercher PS4 et PS3 : ps3ps4
    # order -> tri par orde 
        # - proche = par pertinence
        # - nouveau = par nouveauter
        # - alpha = par ordre alphabetique
        # - populaire = par populariter
        # - notetest = par la note attribuer par la communauté du site
    # direction -> tri le order par ordre croissant ou non
        # - ASC = tri l'ordre par croissance
        # - DESC = tri l'ordre par decroissance
        # exemple si tri par alphabetique et ASC alors les jeux sont trier du A au Z
        # exmeple si tri par populariter et DESC alors les jeux sont trier du moins connue au plus connue
    # qquery -> le nom du jeu rechercher
    # letters
        # -  = aucun filtre de début
        # - 9 = commence par un chiffre
        # - [a-z] = commmence par la ou les lettre selectionner
        # exemple az alors les jeux afficher commence par a ou z
#----------------------------------------------------------------
#format de la sorti -> int
#----------------------------------------------------------------
def getNombrePageJeuRechercher(console, order, direction, qquery, letters) -> int:
    nbrJeux = getNombreJeuxRechercher(console, order, direction, qquery, letters)
    if (nbrJeux%50) > 0:
        nbrPage = int(nbrJeux/50)+1
    else :
        nbrPage = int(nbrJeux/50)
    return nbrPage