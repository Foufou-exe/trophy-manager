import sqlite3

#===============================initialize database=======================================================#
#Init est la fonction qui nous permet d'initialiser la base de donnée
#----------------------------------------------------------------
#arguments de l'entree
     #Aucun
#----------------------------------------------------------------
#format de la sorti
     #Aucun
#----------------------------------------------------------------
#Action de la fonction
     #Cree la table GameRegisterInfo si elle n'existe pas
          #Cree la colone GameUID si elle n'existe pas
          #Cree la colone Pochette si elle n'existe pas
          #Cree la colone URL si elle n'existe pas
          #Cree la colone Titre si elle n'existe pas
          #Cree la colone TropheePlatine si elle n'existe pas
          #Cree la colone TropheeGold si elle n'existe pas
          #Cree la colone TropheeSilver si elle n'existe pas
          #Cree la colone TropheeBronze si elle n'existe pas
          #Cree la colone Console si elle n'existe pas
          #Cree la colone VR si elle n'existe pas
          #Cree la colone PlatinePossible si elle n'existe pas
          #Cree la colone Extra si elle n'existe pas
          #Cree la colone Difficulte si elle n'existe pas
          #Cree la colone NoteJeu si elle n'existe pas
          #Cree la colone DateSortie si elle n'existe pas
          #Cree la colone Genre si elle n'existe pas
          #Cree la colone Territoire si elle n'existe pas
          #Cree la colone nbrTropheeTotal si elle n'existe pas
          #Cree la colone nbrTropheeOnline si elle n'existe pas
          #Cree la colone nbrTropheeCacher si elle n'existe pas
          #Cree la colone DLC si elle n'existe pas
          #Cree la colone Pourcent si elle n'existe pas
     #Cree la table GameRegisterMainTrophee si elle n'existe pas
          #Cree la colone GameUID si elle n'existe pas
          #Cree la colone Nom si elle n'existe pas
          #Cree la colone Description si elle n'existe pas
          #Cree la colone Trophee si elle n'existe pas
          #Cree la colone Pourcentage si elle n'existe pas
          #Cree la colone Image si elle n'existe pas
          #Cree la colone id si elle n'existe pas
          #Cree la colone Terminer si elle n'existe pas
     #Cree la table GameRegisterDLCTrophee si elle n'existe pas
          #Cree la colone GameUID si elle n'existe pas
          #Cree la colone numDLC si elle n'existe pas
          #Cree la colone Nom si elle n'existe pas
          #Cree la colone Description si elle n'existe pas
          #Cree la colone Trophee si elle n'existe pas
          #Cree la colone Pourcentage si elle n'existe pas
          #Cree la colone Image si elle n'existe pas
          #Cree la colone id si elle n'existe pas
          #Cree la colone Terminer si elle n'existe pas
#----------------------------------------------------------------
def Init():
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()

     #===============================init game all info=======================================================#
     cursor.execute("""
     CREATE TABLE IF NOT EXISTS GameRegisterInfo(
          GameUID INTEGER PRIMARY KEY UNIQUE,
          Pochette TEXT,
          URL TEXT,
          Titre TEXT,
          TropheePlatine INTERGER,
          TropheeGold INTERGER,
          TropheeSilver INTERGER,
          TropheeBronze INTERGER,
          Console TEXT,
          VR INTERGER,
          PlatinePossible INTERGER,
          Extra INTERGER,
          Difficulte INTERGER,
          NoteJeu INTERGER,
          DateSortie TEXT,
          Genre TEXT,
          Territoire TEXT,
          nbrTropheeTotal INTERGER,
          nbrTropheeOnline INTERGER,
          nbrTropheeCacher INTERGER,
          DLC INTERGER,
          Pourcent INTERGER
     )
     """)
     conn.commit()

     #===============================init game main trophee=======================================================#
     cursor.execute("""
     CREATE TABLE IF NOT EXISTS GameRegisterMainTrophee(
          GameUID INTEGER NOT NULL,
          Nom TEXT,
          Description TEXT,
          Trophee TEXT,
          Pourcentage REAL,
          Image TEXT,
          id INTEGER,
          Terminer TEXT,
          FOREIGN KEY (GameUID)
               REFERENCES GameRegisterInfo (GameUID) 

     )
     """)
     conn.commit()

     #===============================init game DLC trophee=======================================================#
     cursor.execute("""
     CREATE TABLE IF NOT EXISTS GameRegisterDLCTrophee(
          GameUID INTEGER NOT NULL,
          numDLC INTEGER,
          Nom TEXT,
          Description TEXT,
          Trophee TEXT,
          Pourcentage REAL,
          Image TEXT,
          id INTEGER,
          Terminer TEXT,
          FOREIGN KEY (GameUID)
               REFERENCES GameRegisterInfo (GameUID) 
     )
     """)
     conn.commit()

     conn.close()

#===============================get all game added=======================================================#
#getAllGame est la fonction qui nous permet de recuperer 
#----------------------------------------------------------------
#arguments de l'entree
     #Aucun
#----------------------------------------------------------------
#format de la sorti -> une list qui contient des dictionnaire avec les jeux ajouter 
#key                               #value

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
#Pourcent               #affiche le pourcentage d'avancement dans le jeu
#----------------------------------------------------------------
def getAllGame() ->list:
     conn = sqlite3.connect('TropheeBdd.db')
     cur = conn.cursor()
     cur.execute("SELECT * FROM GameRegisterInfo")
     rows = cur.fetchall()
     listGame = []
     if type(rows) is not type(None):
          for row in rows:
               gameRow = {}
               gameRow['GameUID'] = row[0]
               gameRow['Pochette'] = row[1]
               gameRow['URL'] = row[2]
               gameRow['Titre'] = row[3]
               gameRow['TropheePlatine'] = row[4]
               gameRow['TropheeGold'] = row[5]
               gameRow['TropheeSilver'] = row[6]
               gameRow['TropheeBronze'] = row[7]
               gameRow['Console'] = row[8]
               gameRow['VR'] = row[9]
               gameRow['PlatinePossible'] = row[10]
               gameRow['Extra'] = row[11]
               gameRow['Difficulte'] = row[12]
               gameRow['NoteJeu'] = row[13]
               gameRow['DateSortie'] = row[14]
               gameRow['Genre'] = row[15]
               gameRow['Territoire'] = row[16]
               gameRow['nbrTropheeTotal'] = row[17]
               gameRow['nbrTropheeOnline'] = row[18]
               gameRow['nbrTropheeCacher'] = row[19]
               gameRow['DLC'] = row[20]
               gameRow['Pourcent'] = row[21]
               listGame.append(gameRow)
          return listGame

#===============================add game all info=======================================================#
#addGameInfo est la fonction qui nous permet d'ecrire dans la base de donne les information d'un jeu
#----------------------------------------------------------------
#arguments de l'entree
     #Aucun
#----------------------------------------------------------------
#format de la sorti
     #Aucun
#----------------------------------------------------------------
#Action de la fonction
     #insert dans GameRegisterInfo les information de jeu
#----------------------------------------------------------------
def addGameInfo(GameUID, Pochette, URL, Titre, TropheePlatine, TropheeGold, TropheeSilver, TropheeBronze, Console, VR, PlatinePossible, Extra, Difficulte, NoteJeu, DateSortie, Genre, Territoire, nbrTropheeTotal, nbrTropheeOnline, nbrTropheeCacher, DLC, Pourcent):
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_insert_query = f"INSERT INTO GameRegisterInfo (GameUID, Pochette, URL, Titre, TropheePlatine, TropheeGold, TropheeSilver, TropheeBronze, Console, VR, PlatinePossible, Extra, Difficulte, NoteJeu, DateSortie, Genre, Territoire, nbrTropheeTotal, nbrTropheeOnline, nbrTropheeCacher, DLC, Pourcent) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
     cursor.execute(sqlite_insert_query, (GameUID, Pochette, URL, Titre, TropheePlatine, TropheeGold, TropheeSilver, TropheeBronze, Console, VR, PlatinePossible, Extra, Difficulte, NoteJeu, DateSortie, Genre, Territoire, nbrTropheeTotal, nbrTropheeOnline, nbrTropheeCacher, DLC, Pourcent))
     conn.commit()
     print("Record inserted successfully into GameRegisterInfo table ", cursor.rowcount)
     cursor.close()
#===============================remove game all info from GameUID=======================================================#
def removeGameInfoFromGameUID(GameUID):
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_insert_query = f"DELETE FROM GameRegisterInfo WHERE GameUID = ?"
     cursor.execute(sqlite_insert_query, (GameUID,))
     conn.commit()
     print("Record inserted successfully into GameRegisterInfo table ", cursor.rowcount)
     cursor.close()
#===============================update terminer to game all info db table with GameUID=======================================================#
def updateGameInfoFromGameUID(pourcent, GameUID) :
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_update_query = 'UPDATE GameRegisterInfo SET pourcent = ? WHERE GameUID = ?'
     cursor.execute(sqlite_update_query, (pourcent, GameUID))
     conn.commit()
     print("Record update successfully from GameRegisterInfo table ", cursor.rowcount)
     cursor.close()
#===============================Get all main trophee db table from GameUID=======================================================#
def getGameInfoFromGameUID(GameUID) -> dict :
     conn = sqlite3.connect('TropheeBdd.db')
     cur = conn.cursor()
     cur.execute("SELECT * FROM GameRegisterInfo WHERE GameUID = ?", (GameUID,))
     row = cur.fetchone()
     gameRow = {}
     gameRow['GameUID'] = row[0]
     gameRow['Pochette'] = row[1]
     gameRow['URL'] = row[2]
     gameRow['Titre'] = row[3]
     gameRow['TropheePlatine'] = row[4]
     gameRow['TropheeGold'] = row[5]
     gameRow['TropheeSilver'] = row[6]
     gameRow['TropheeBronze'] = row[7]
     gameRow['Console'] = row[8]
     gameRow['VR'] = row[9]
     gameRow['PlatinePossible'] = row[10]
     gameRow['Extra'] = row[11]
     gameRow['Difficulte'] = row[12]
     gameRow['NoteJeu'] = row[13]
     gameRow['DateSortie'] = row[14]
     gameRow['Genre'] = row[15]
     gameRow['Territoire'] = row[16]
     gameRow['nbrTropheeTotal'] = row[17]
     gameRow['nbrTropheeOnline'] = row[18]
     gameRow['nbrTropheeCacher'] = row[19]
     gameRow['DLC'] = row[20]
     gameRow['Pourcent'] = row[21]
     return gameRow

#===============================add to main trophee db table=======================================================#
def addMainTrophee(GameUID, Nom, Description, Trophee, Pourcentage, Image, id, Terminer) :
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_insert_query = f"INSERT INTO GameRegisterMainTrophee (GameUID, Nom, Description, Trophee, Pourcentage, Image, id, Terminer) VALUES (?,?,?,?,?,?,?,?)"
     cursor.execute(sqlite_insert_query, (GameUID, Nom, Description, Trophee, Pourcentage, Image, id, Terminer))
     conn.commit()
     print("Record inserted successfully into GameRegisterMainTrophee table ", cursor.rowcount)
     cursor.close()
#===============================remove to main trophee db table whit id=======================================================#
def removeMainTropheeFromID(id) :
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_remove_query = 'DELETE FROM GameRegisterMainTrophee WHERE id=?'
     cursor.execute(sqlite_remove_query, (id,))
     conn.commit()
     print("Record removed successfully from GameRegisterMainTrophee table ", cursor.rowcount)
     cursor.close()
#===============================remove to main trophee db table whit GameUID=======================================================#
def removeMainTropheeFromGameUID(GameUID) :
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_remove_query = 'DELETE FROM GameRegisterMainTrophee WHERE GameUID=?'
     cursor.execute(sqlite_remove_query, (GameUID,))
     conn.commit()
     print("Record removed successfully from GameRegisterMainTrophee table ", cursor.rowcount)
     cursor.close()
#===============================update terminer to main trophee db table with id=======================================================#
def updateMainTropheeFromID(terminer, id) :
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_update_query = 'UPDATE GameRegisterMainTrophee SET Terminer = ? WHERE id = ?'
     cursor.execute(sqlite_update_query, (terminer, id))
     conn.commit()
     print("Record update successfully from GameRegisterMainTrophee table ", cursor.rowcount)
     cursor.close()
#===============================update terminer to main trophee db table with GameUID=======================================================#
def updateMainTropheeFromGameUID(terminer, GameUID) :
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_update_query = 'UPDATE GameRegisterMainTrophee SET Terminer = ? WHERE GameUID = ?'
     cursor.execute(sqlite_update_query, (terminer, GameUID))
     conn.commit()
     print("Record update successfully from GameRegisterMainTrophee table ", cursor.rowcount)
     cursor.close()
#===============================Get all main trophee db table from GameUID=======================================================#
def getAllMainTropheeFromGameUID(GameUID) -> list :
     conn = sqlite3.connect('TropheeBdd.db')
     cur = conn.cursor()
     cur.execute("SELECT * FROM GameRegisterMainTrophee WHERE GameUID = ?", (GameUID,))
     rows = cur.fetchall()
     listGame = []
     for row in rows:
          gameRow = {}
          gameRow['GameUID'] = row[0]
          gameRow['Nom'] = row[1]
          gameRow['Description'] = row[2]
          gameRow['Trophee'] = row[3]
          gameRow['Pourcentage'] = row[4]
          gameRow['Image'] = row[5]
          gameRow['id'] = row[6]
          gameRow['Terminer'] = row[7]
          listGame.append(gameRow)
     return listGame
#===============================Get main trophee db table from id and gameuid=======================================================#
def getMainTropheeFromID(GameUID, id) -> dict:
     conn = sqlite3.connect('TropheeBdd.db')
     cur = conn.cursor()
     cur.execute("SELECT * FROM GameRegisterMainTrophee WHERE id = ? AND GameUID = ?", (id, GameUID))
     rows = cur.fetchone()
     if type(rows) is not type(None):
          game = {}
          game['GameUID'] = rows[0]
          game['Nom'] = rows[1]
          game['Description'] = rows[2]
          game['Trophee'] = rows[3]
          game['Pourcentage'] = rows[4]
          game['Image'] = rows[5]
          game['id'] = id
          game['Terminer'] = rows[7]
          return game


#===============================add to DLC trophee db table=======================================================#
def addDLCTrophee(GameUID, numDLC, Nom, Description, Trophee, Pourcentage, Image, id, Terminer) :
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_insert_query = f"INSERT INTO GameRegisterDLCTrophee (GameUID, numDLC, Nom, Description, Trophee, Pourcentage, Image, id, Terminer) VALUES (?,?,?,?,?,?,?,?,?)"
     cursor.execute(sqlite_insert_query, (GameUID, numDLC, Nom, Description, Trophee, Pourcentage, Image, id, Terminer))
     conn.commit()
     print("Record inserted successfully into GameRegisterDLCTrophee table ", cursor.rowcount)
     cursor.close()
#===============================remove to DLC trophee db table whit id=======================================================#
def removeDLCTropheeFromID(id) :
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_remove_query = 'DELETE FROM GameRegisterDLCTrophee WHERE id=?'
     cursor.execute(sqlite_remove_query, (id,))
     conn.commit()
     print("Record removed successfully from GameRegisterDLCTrophee table ", cursor.rowcount)
     cursor.close()
#===============================remove to DLC trophee db table whit GameUID=======================================================#
def removeDLCTropheeFromGameUID(GameUID) :
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_remove_query = 'DELETE FROM GameRegisterDLCTrophee WHERE GameUID=?'
     cursor.execute(sqlite_remove_query, (GameUID,))
     conn.commit()
     print("Record removed successfully from GameRegisterDLCTrophee table ", cursor.rowcount)
     cursor.close()
#===============================remove to DLC trophee db table whit numDLC=======================================================#
def removeDLCTropheeFromNumDLC(numDLC) :
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_remove_query = 'DELETE FROM GameRegisterDLCTrophee WHERE numDLC=?'
     cursor.execute(sqlite_remove_query, (numDLC,))
     conn.commit()
     print("Record removed successfully from GameRegisterDLCTrophee table ", cursor.rowcount)
     cursor.close()
#===============================update terminer to DLC trophee db table with id=======================================================#
def updateDLCTropheeFromID(terminer, id) :
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_update_query = 'UPDATE GameRegisterDLCTrophee SET Terminer = ? WHERE id = ?'
     cursor.execute(sqlite_update_query, (terminer, id))
     conn.commit()
     print("Record update successfully from GameRegisterDLCTrophee table ", cursor.rowcount)
     cursor.close()
#===============================update terminer to DLC trophee db table with GameUID=======================================================#
def updateDLCTropheeFromGameUID(terminer, GameUID) :
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_update_query = 'UPDATE GameRegisterDLCTrophee SET Terminer = ? WHERE GameUID = ?'
     cursor.execute(sqlite_update_query, (terminer, GameUID))
     conn.commit()
     print("Record update successfully from GameRegisterDLCTrophee table ", cursor.rowcount)
     cursor.close()
#===============================update terminer to DLC trophee db table with numDLC=======================================================#
def updateDLCTropheeFromNumDLC(terminer, numDLC) :
     conn = sqlite3.connect('TropheeBdd.db')
     cursor = conn.cursor()
     sqlite_update_query = 'UPDATE GameRegisterDLCTrophee SET Terminer = ? WHERE numDLC = ?'
     cursor.execute(sqlite_update_query, (terminer, numDLC))
     conn.commit()
     print("Record update successfully from GameRegisterDLCTrophee table ", cursor.rowcount)
     cursor.close()
#===============================Get all DLC trophee db table from GameUID=======================================================#
def getAllDLCTropheeFromGameUID(GameUID) -> list :
     conn = sqlite3.connect('TropheeBdd.db')
     cur = conn.cursor()
     cur.execute("SELECT * FROM GameRegisterDLCTrophee WHERE GameUID = ?", (GameUID,))
     rows = cur.fetchall()
     listGame = []
     if type(rows) is not type(None):
          for row in rows:
               gameRow = {}
               gameRow['GameUID'] = row[0]
               gameRow['numDLC'] = row[1]
               gameRow['Nom'] = row[2]
               gameRow['Description'] = row[3]
               gameRow['Trophee'] = row[4]
               gameRow['Pourcentage'] = row[5]
               gameRow['Image'] = row[6]
               gameRow['id'] = row[7]
               gameRow['Terminer'] = row[8]
               listGame.append(gameRow)
     return listGame
#===============================Get all DLC trophee db table from GameUID and numDLC=======================================================#
def getAllDLCTropheeFromNumDLC(GameUID, numDLC) -> list :
     conn = sqlite3.connect('TropheeBdd.db')
     cur = conn.cursor()
     cur.execute("SELECT * FROM GameRegisterDLCTrophee WHERE GameUID = ? AND numDLC = ?", (GameUID, numDLC))
     rows = cur.fetchall()
     listGame = []
     if type(rows) is not type(None):
          for row in rows:
               gameRow = {}
               gameRow['GameUID'] = row[0]
               gameRow['numDLC'] = row[1]
               gameRow['Nom'] = row[2]
               gameRow['Description'] = rows[3]
               gameRow['Trophee'] = row[4]
               gameRow['Pourcentage'] = row[5]
               gameRow['Image'] = row[6]
               gameRow['id'] = row[7]
               gameRow['Terminer'] = row[8]
               listGame.append(gameRow)
     return listGame
#===============================Get DLC trophee db table from id and gameuid=======================================================#
def getDLCTropheeFromID(GameUID, id) -> dict:
     conn = sqlite3.connect('TropheeBdd.db')
     cur = conn.cursor()
     cur.execute("SELECT * FROM GameRegisterDLCTrophee WHERE id = ? AND GameUID = ?", (id, GameUID))
     rows = cur.fetchone()
     if type(rows) is not type(None):
          game = {}
          game['GameUID'] = rows[0]
          game['Nom'] = rows[1]
          game['Description'] = rows[2]
          game['Trophee'] = rows[3]
          game['Pourcentage'] = rows[4]
          game['Image'] = rows[5]
          game['id'] = id
          game['Terminer'] = rows[7]
          return game

# Init()

# print(getAllGame())

# addGameInfo(99, "https://", "https://", "titre du jeu", 1, 2, 5, 3, "PS4", 0, 1, 1, 8, 20, "28/05/2002", "RPG", "France", 11, 2, 2, 2, 0)
# removeGameInfoFromGameUID(99)
# updateGameInfoFromGameUID(50, 99)
# print(getGameInfoFromGameUID(99))

# addMainTrophee(99, "trophee main", 'platine', 39.5, "https://test.com", 1, 'false')
# removeMainTropheeFromID(1)
# removeMainTropheeFromGameUID(99)
# updateMainTropheeFromID('true', 1)
# updateMainTropheeFromGameUID('true', 99)
# print(getMainTropheeFromID(99, 1))
# print(getAllMainTropheeFromGameUID(99))

# addDLCTrophee(98, 2, "trophee DLC", 'bronze', 38.5, "https://test.sscom", 1, 'false')
# removeDLCTropheeFromID(1)
# removeDLCTropheeFromGameUID(98)
# removeDLCTropheeFromNum#DLC(1)
# updateDLCTropheeFromID('true', 1)
# updateDLCTropheeFromGameUID('true', 98)
# updateDLCTropheeFromNumDLC('true', 1)
# print(getAllDLCTropheeFromGameUID(52273458))
# print(getAllDLCTropheeFromNumDLC(98, 2))
# print(getDLCTropheeFromID(98, 1))