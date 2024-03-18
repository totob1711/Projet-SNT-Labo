# import de la librairie pour interagir avec la base de donnée (pymysql) et des class et fonctions
import pymysql
from graphic_functions import * 
from Users import *

if __name__ == "__main__":
    # Création de la base de donnée si c'est la première fois que nous lançons l'application
    try:
        database = pymysql.connect(host="localhost", user="root", password="")
        try:
            with database.cursor() as request:
                create = 'create database appobjet;'
                request.execute(create)
                select_bdd = 'use appobjet;'
                request.execute(select_bdd)
                sql = 'CREATE TABLE regions(ID_regions INT AUTO_INCREMENT, PRIMARY KEY(ID_regions))ENGINE=INNODB;'
                sql2 = 'CREATE TABLE unites(ID_unites INT AUTO_INCREMENT, numero INT, fonction VARCHAR(50), ID_regions INT NOT NULL, PRIMARY KEY(ID_unites), FOREIGN KEY(ID_regions) REFERENCES Régions(ID_regions) ON DELETE CASCADE);'
                sql3 = 'CREATE TABLE utilisateurs(ID_utilisateurs INT AUTO_INCREMENT, login VARCHAR(50), pwd VARCHAR(256), nom VARCHAR(50), prenom VARCHAR(50), mail VARCHAR(50), tel VARCHAR(50), droit VARCHAR(50), roles VARCHAR(50), PRIMARY KEY(ID_utilisateurs));'
                sql4 = 'CREATE TABLE responsables_Scientifiques(ID_Responsables_scientifiques INT AUTO_INCREMENT, dates DATE, ID_unites INT NOT NULL, PRIMARY KEY(ID_Responsables_scientifiques), FOREIGN KEY(ID_unites) REFERENCES Unités(ID_unites) ON DELETE CASCADE);'
                sql5 = 'CREATE TABLE travailler(ID_unites INT, ID_utilisateurs INT,PRIMARY KEY(ID_unites, ID_utilisateurs), FOREIGN KEY(ID_unites) REFERENCES Unités(ID_unites) ON DELETE CASCADE, FOREIGN KEY(ID_utilisateurs) REFERENCES Utilisateurs(ID_utilisateurs) ON DELETE CASCADE);'
                request.execute(sql)
                request.execute(sql2)
                request.execute(sql3)
                request.execute(sql4)
                request.execute(sql5)
                # Création du super admin si c'est la première fois que nous lançons l'application
                DefaultPwd = "password"
                hashage = hashlib.sha256(DefaultPwd.encode()) # Hash du mot de passe par defaut
                hash_DefaultPwd = hashage.hexdigest() # Hash du mot de passe par défaut
                try:
                    bdd = pymysql.connect(host="localhost", user="root", password="", db="appobjet")
                    with bdd.cursor() as request:
                        insertDefaultAdmin = f"INSERT INTO utilisateurs (login, pwd, nom, prenom, mail, tel, droit, roles) VALUES ('admin', '{hash_DefaultPwd}', 'dupont', 'jean', 'jean.dupont@gmail.com', '061234578', 'tous les droits', 'admin');"
                        request.execute(insertDefaultAdmin)
                except:
                    pass
        except:
            pass
    except:
        pass
    
    # Appel de la fonction d'affichage de l'interface graphique
    window()