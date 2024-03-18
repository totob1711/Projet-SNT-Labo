import customtkinter
import pymysql
import Users
import hashlib

fail_log = 0

# Fonction permettant de se deconnecter et de retourner à la page de connexion
def quit_session():
    new_body.destroy()
    
    home_body()
    
# Fonction permettant de lister tous les utilisateurs de la base de données
def list_user():
    
    # Definition de la fonction pour revenir a l'accueil après le listing utilisateurs
    def back_home():
        # Suppression du corps de la page de liste utilisateur
        ListUserBody.destroy()
        
        # Appel de la fonction pour afficher le corps de la fenetre d'accueil
        NewBody()
        
    # Suppression de l'ancien corps 
    new_body.destroy()
    
    # Creation de variables permettant de stocker et de boucler sur les utilisateurs
    all_users = []
    n = 0
    height = 0
    
    # Creation d'un nouveau corps pour afficher les utilisateurs
    ListUserBody = customtkinter.CTkFrame(root, width=350, height=400)
    ListUserBody.place(x=0, y=100)
    
    # Connection à la base de données pour recuperer les utilisateurs
    try:
        database = pymysql.connect(host="localhost", user="root", password="", db="appobjet")
        try:
            with database.cursor() as request:
                sql = "SELECT nom, prenom, mail, tel, roles FROM utilisateurs"
                request.execute(sql)
                users = request.fetchall()
                number_users = len(users)
                all_users.append(users)

                # Boucle permettant d'afficher tous les différents utilisateurs
                for i in range(number_users):
                        
                    name = customtkinter.CTkLabel(ListUserBody, text=all_users[0][n][0], font=("Calibri",12), text_color="white", width=15, justify='center')
                    name.place(x=5, y=height)
                    firstName = customtkinter.CTkLabel(ListUserBody, text=all_users[0][n][1], font=("Calibri",12), text_color="white", width=15, justify='center')
                    firstName.place(x=55, y=height)
                    mail = customtkinter.CTkLabel(ListUserBody, text=all_users[0][n][2], font=("Calibri",12), text_color="white", width=15, justify='center')
                    mail.place(x=105, y=height)
                    tel = customtkinter.CTkLabel(ListUserBody, text=all_users[0][n][3], font=("Calibri",12), text_color="white", width=15, justify='center')
                    tel.place(x=225, y=height)
                    role = customtkinter.CTkLabel(ListUserBody, text=all_users[0][n][4], font=("Calibri",12), text_color="white", width=15, justify='center')
                    role.place(x=285, y=height)

                    n += 1
                    height += 30
                
                height += 40
                btn_home = customtkinter.CTkButton(ListUserBody, text="Retourner à l'accueil", text_color="white", fg_color="green", width=200, command=back_home)
                btn_home.place(x=70, y=height)
                    
        except Exception as erreur:
            print(erreur)
    except:
        pass

# Fonction permettant de valider la suppression d'un utilisateur dans la base de données
def validate_del_user():
    
    # Definition de la fonction pour revenir a l'accueil après la suppression d'un utilisateur
    def back_home():
        # Suppression du corps de la page de validation de la suppression utilisateur
        DelUserBody.destroy()
        
        # Appel de la fonction pour afficher le corps de la fenetre d'accueil
        NewBody()
    
    name = DelNameInput.get()
    firstName = DelFirstNameInput.get()
    
    try:
        database = pymysql.connect(host="localhost", user="root", password="", db="appobjet")
        try:
            with database.cursor() as request:
                sql = f"DELETE FROM utilisateurs WHERE nom = '{name}' and prenom = '{firstName}'"
                request.execute(sql)
                DelNameTitle.destroy()
                DelNameInput.destroy()
                DelFirstNameTitle.destroy()
                DelFirstNameInput.destroy()
                btn_validate_delete.destroy()
                
                validation_message = customtkinter.CTkLabel(DelUserBody, text="La suppression a été effectuée", font=("Arial",20), width=20, text_color="white")
                validation_message.place(x=30, y=50)
                
                btn_home = customtkinter.CTkButton(DelUserBody, text="Retourner à l'accueil", text_color="white", fg_color="green", width=200, command=back_home)
                btn_home.place(x=70, y=90)
        except:
            DelNameTitle.destroy()
            DelNameInput.destroy()
            DelFirstNameTitle.destroy()
            DelFirstNameInput.destroy()
            btn_validate_delete.destroy()
            
            error_message = customtkinter.CTkLabel(DelUserBody, text="Une erreur est survenu, rééssayez ulterieurement", font=("Arial",20), width=20, text_color="white")
            error_message.place(x=70, y=50)
    except:
        pass
          
# Fonction permettant de selectionner un utilisateur a supprimer          
def del_user():
    new_body.destroy()
    
    global DelNameInput, DelFirstNameInput, DelNameTitle, DelFirstNameTitle, btn_validate_delete, DelUserBody
    DelUserBody = customtkinter.CTkFrame(root, width=350, height=400)
    DelUserBody.place(x=0, y=100)
    
    DelNameTitle = customtkinter.CTkLabel(DelUserBody, text="Nom", font=("Calibri",12), text_color="white", width=20)
    DelNameTitle.place(x=70, y=20)
    DelNameInput = customtkinter.CTkEntry(DelUserBody, placeholder_text="Entrez le nom de l'utilisateur", text_color="white", width=200)
    DelNameInput.place(x=70, y=45)

    DelFirstNameTitle = customtkinter.CTkLabel(DelUserBody, text="Prénom", font=("Calibri",12), text_color="white", width=20)
    DelFirstNameTitle.place(x=70, y=80)
    DelFirstNameInput = customtkinter.CTkEntry(DelUserBody, placeholder_text="Entrez le prenom de l'utilisateur", text_color="white", width=200)
    DelFirstNameInput.place(x=70, y=105)
    
    btn_validate_delete = customtkinter.CTkButton(DelUserBody, text="Valider la suppression", font=("Calibri",12), fg_color="red", width=200, command=validate_del_user)
    btn_validate_delete.place(x=70, y=150)

# Fonction permettant de créer un nouvel utilisateur
def add_user():
    
    # Definition de la fonction pour revenir a l'accueil après la creation de l'utilisateur
    def back_home():
        # Suppression du corps de la page de creation utilisateur
        ValidationBody.destroy()
        
        # Appel de la fonction pour afficher le corps de la fenetre d'accueil
        NewBody()
    
    # Definition de la fonction pour revenir en arrière en cas d'erreur
    def function_back():
        
        # Suppression du corps de creation utilisateur
        AddUserBody.destroy()
        
        # Remplacement de l'ancien corps par le corps d'accueil
        NewBody()
    
    # Definition de la fonction pour continuer la modification des utilisateurs
    def function_next():
        # Assignation des droits en fonction du role de l'utilisateur 
        nom = NameInput.get()
        prenom = FirstnameInput.get()
        mail = MailInput.get()
        tel = TelInput.get()
        role = RoleInput.get()
        if role == "Commercial":
            droit = "Lecture uniquement"
        elif role == "Medecin":
            droit = "Ecriture limitée et lecture"
        elif role == "Scientifique":
            droit = "Ecriture et lecture"
        elif role == "Assistant":
            droit = "Lecture uniquement"
        user = Users.Users(nom, prenom, mail, tel, role, droit)
        # Hashage du mot de passe avant de le stocker dans la base de données
        pwd = Users.Users.generate_password(user, 12)
        hashage = hashlib.sha256(pwd.encode())
        hash_pwd = hashage.hexdigest()
        login = prenom[:1] + nom
        # Insertion de l'utilisateur dans la base de données
        try:
            database = pymysql.connect(host="localhost", user="root", password="", db="appobjet")
            try:
                with database.cursor() as request:
                    sql = f"INSERT INTO utilisateurs (login, pwd, nom, prenom, mail, tel, droit, roles) VALUES ('{login}', '{hash_pwd}', '{nom}', '{prenom}', '{mail}', '{tel}', '{droit}', '{role}');"
                    request.execute(sql)
                    
                    # Suppression de l'ancien corps
                    AddUserBody.destroy()
                    
                    # Creation d'un nouveau corps permettant de voir le login et le password de l'utilisateur afin de lui transmettre7
                    global ValidationBody
                    ValidationBody = customtkinter.CTkFrame(root, width=350, height=400)
                    ValidationBody.place(x=0, y=100)
                    
                    validationMessage = customtkinter.CTkLabel(ValidationBody, text="L'utilisateur a bien été créé", font=("Arial",20), width=20)
                    validationMessage.place(x=70, y=50)
                    
                    userNameTitle = customtkinter.CTkLabel(ValidationBody, text="Login : ", font=("Calibri",12), text_color="white", width=10)
                    userNameTitle.place(x=70, y=75)
                    
                    userName = customtkinter.CTkLabel(ValidationBody, text=login, font=("Calibri",12), text_color='white', width=10)
                    userName.place(x=140, y=75)
                    
                    pwdTitle = customtkinter.CTkLabel(ValidationBody, text="Password : ", font=("Calibri",12), text_color="white", width=10)
                    pwdTitle.place(x=70, y=100)
                    
                    SeePwd = customtkinter.CTkLabel(ValidationBody, text=pwd, font=("Calibri",12), text_color='white', width=10)
                    SeePwd.place(x=140, y=100)
                    
                    btn_home = customtkinter.CTkButton(ValidationBody, text="Retourner à l'accueil", text_color="white", fg_color="green", width=200, command=back_home)
                    btn_home.place(x=70, y=140)
                    
            except Exception as error:
                print(error)
        except:
            pass      
            
    # Suppression de l'ancien corps
    new_body.destroy()
    
    # Creation d'un nouveau corps pour placer les widgets nécéssaire à la création d'un nouvel utilisateur
    AddUserBody = customtkinter.CTkFrame(root, width=350, height=400)
    AddUserBody.place(x=0, y=100)
    
    NameTitle = customtkinter.CTkLabel(AddUserBody, text="Nom : ", font=("Calibri",12), text_color="white", width=10)
    NameTitle.place(x=70, y=10)
    NameInput = customtkinter.CTkEntry(AddUserBody, font=("Calibri",12), placeholder_text="Entrez le nom de l'utilisateur", text_color="white", width=200)
    NameInput.place(x=70, y=35)
    
    FirstnameTitle = customtkinter.CTkLabel(AddUserBody, text="Prénom : ", font=("Calibri",12), text_color="white", width=10)
    FirstnameTitle.place(x=70, y=70)
    FirstnameInput = customtkinter.CTkEntry(AddUserBody, font=("Calibri",12), placeholder_text="Entrez le prénom de l'utilisateur", text_color="white", width=200)
    FirstnameInput.place(x=70, y=95)
    
    MailTitle = customtkinter.CTkLabel(AddUserBody, text="E-mail : ", font=("Calibri",12), text_color="white", width=10)
    MailTitle.place(x=70, y=130)
    MailInput = customtkinter.CTkEntry(AddUserBody, font=("Calibri",12), placeholder_text="Entrez l'e-mail de l'utilisateur", text_color="white", width=200)
    MailInput.place(x=70, y=155)
    
    TelTitle = customtkinter.CTkLabel(AddUserBody, text="Téléphone : ", font=("Calibri",12), text_color="white", width=10)
    TelTitle.place(x=70, y=190)
    TelInput = customtkinter.CTkEntry(AddUserBody, font=("Calibri",12), placeholder_text="Entrez le téléphone de l'utilisateur", text_color="white", width=200)
    TelInput.place(x=70, y=215)
    
    RoleTitle = customtkinter.CTkLabel(AddUserBody, text="Rôle : ", font=("Calibri",12), text_color="white", width=10)
    RoleTitle.place(x=70, y=250)    
    RoleInput = customtkinter.CTkOptionMenu(AddUserBody, values=["Commercial", "Medecin", "Scientifique", "Assistant"], width=200)
    RoleInput.set("Choisissez un rôle")
    RoleInput.place(x=70, y=275)
    
    next = customtkinter.CTkButton(AddUserBody, text="Suivant", font=("Calibri",12), width=100, fg_color="green", text_color="white", command=function_next)
    next.place(x=230, y=330)
    
    back = customtkinter.CTkButton(AddUserBody, text="Retour", font=("Calibri",12), width=100, fg_color="red", text_color="white", command=function_back)
    back.place(x=20, y=330)

# Fonction permettant d'envoyer les modifications vers la base de données
def send_modifications():
    
    def back_home():
        
        # Suppression du corps pour afficher la confirmation
        MessageModifBody.destroy()
        
        # Appel de la fonction qui affiche le corps contenant l'ecran d'accueil
        NewBody()
    
    # Connection a la base de données pour effectuer les requêtes 
    try:
        database = pymysql.connect(host="localhost", user="root", password="", db="appobjet")
        try:
            with database.cursor() as request:
                # Verification des options qui ont été choisis ou non sur la page précédente
                if valueTel == 1:
                    tel = TelModif.get()
                    sql_tel = f"UPDATE utilisateurs SET tel = '{tel}' WHERE nom = '{NameUser}' and prenom = '{FirstNameUser}'"
                    request.execute(sql_tel)     
                else:
                    pass
                
                if valuePwd == 1:
                    pwd = PwdModif.get()
                    hashage = hashlib.sha256(pwd.encode())
                    hash_pwd = hashage.hexdigest()
                    sql_pwd = f"UPDATE utilisateurs SET pwd = '{hash_pwd}' WHERE nom = '{NameUser}' and prenom = '{FirstNameUser}'"
                    request.execute(sql_pwd)
                else:
                    pass
                
                if valueMail == 1:
                    mail = MailModif.get()
                    sql_mail = f"UPDATE utilisateurs SET mail = '{mail}' WHERE nom = '{NameUser}' and prenom = '{FirstNameUser}'"
                    request.execute(sql_mail) 
                else:
                    pass
                
                if valueRole == 1:
                    role = RoleModif.get()
                    if role == "Commercial" or role == "Assistant":
                        sql_role1 = f"UPDATE utilisateurs SET roles = '{role}', droit = 'Lecture uniquement' WHERE nom = '{NameUser}' and prenom = '{FirstNameUser}'"
                        request.execute(sql_role1)
                    elif role == "Medecin":
                        sql_role2 = f"UPDATE utilisateurs SET roles = '{role}', droit = 'Lecture et ecriture limitée' WHERE nom = '{NameUser}' and prenom = '{FirstNameUser}'"
                        request.execute(sql_role2)
                    elif role == "Scientifique":
                        sql_role3 = f"UPDATE utilisateurs SET roles = '{role}', droit = 'Lecture et ecriture' WHERE nom = '{NameUser}' and prenom = '{FirstNameUser}'"
                        request.execute(sql_role3)
                else:
                    pass
                
                if valueName == 1:
                    name = NameModif.get()
                    sql_name = f"UPDATE utilisateurs SET nom = '{name}' WHERE nom = '{NameUser}' and prenom = '{FirstNameUser}'"
                    request.execute(sql_name)
                else:
                    pass
                    
        except: 
            pass
    except:
        pass
    
    # Suppression du corps contenant les widgets sur les informations à changer
    ValidateModifBody.destroy()
    
    # Creation d'un nouveau corps
    MessageModifBody = customtkinter.CTkFrame(root, width=350, height=400)
    MessageModifBody.place(x=0, y=100) 
    
    # Affichage des messages de confirmation en fonction des données qui ont été modifiées
    if valueTel == 1:
        ValidationModifTel = customtkinter.CTkLabel(MessageModifBody, text="Le téléphone à été mis à jour avec succès", width=25, font=("Calibri",12), text_color="white", justify='center')
        ValidationModifTel.place(x=70, y=20) 
    else:
        pass
    
    if valuePwd == 1:
        ValidationModifPwd = customtkinter.CTkLabel(MessageModifBody, text="Le mot de passe à été mis à jour avec succès", width=25, font=("Calibri",12), text_color="white", justify='center')
        ValidationModifPwd.place(x=70, y=50)
    else:
        pass 
    
    if valueRole == 1:
        ValidationModifRole = customtkinter.CTkLabel(MessageModifBody, text="Le rôle à été mis à jour avec succès", width=25, font=("Calibri",12), text_color="white", justify='center')
        ValidationModifRole.place(x=70, y=110)
    else:
        pass
    
    if valueName == 1:
        ValidationModifName = customtkinter.CTkLabel(MessageModifBody, text="Le nom à été mis à jour avec succès", width=25, font=("Calibri",12), text_color="white", justify='center')
        ValidationModifName.place(x=70, y=140)
    else:
        pass
    
    if valueMail == 1:
        ValidationModifName = customtkinter.CTkLabel(MessageModifBody, text="Le mail à été mis à jour avec succès", width=25, font=("Calibri",12), text_color="white", justify='center')
        ValidationModifName.place(x=70, y=80)
    else:
        pass

    btn_home = customtkinter.CTkButton(MessageModifBody, text="Retourner à l'accueil", font=("Calibri",12), text_color="white", width=200, fg_color="green", command=back_home)
    btn_home.place(x=70, y=180)

# Fonction permettant de definir les nouvelles valeurs à assigner
def validate_modifications():
    
    # Recuperation du nom et prenom de l'utilisateur à modifier
    global NameUser, FirstNameUser
    NameUser = modifNameInput.get()
    FirstNameUser = modifFirstNameInput.get()
    
    # Suppression de l'ancien corps
    ModifUserBody.destroy()
    
    # Creation d'un nouveau corps pour placer les widgets
    global ValidateModifBody
    ValidateModifBody = customtkinter.CTkFrame(root, width=350, height=400)
    ValidateModifBody.place(x=0, y=100)
    
    # Creation des widgets pour entrer les valeurs a modifier
    global NameModif, PwdModif, MailModif, TelModif, RoleModif
    NameModif = customtkinter.CTkEntry(ValidateModifBody, text_color="white", placeholder_text="Entrez le nouveau nom de l'utilisateur", font=("Calibri",12), width=250)
    PwdModif = customtkinter.CTkEntry(ValidateModifBody, text_color="white", placeholder_text="Entrez le nouveau mot de passe de l'utilisateur", font=("Calibri",12), width=250)
    MailModif = customtkinter.CTkEntry(ValidateModifBody, text_color="white", placeholder_text="Entrez le nouveau mail de l'utilisateur", font=("Calibri",12), width=250)
    TelModif = customtkinter.CTkEntry(ValidateModifBody, text_color="white", placeholder_text="Entrez le nouveau téléphone de l'utilisateur", font=("Calibri",12), width=250)
    RoleModif = customtkinter.CTkOptionMenu(ValidateModifBody, values=["Commercial", "Medecin", "Scientifique", "Assistant"], width=200)
    RoleModif.set("Choisissez un rôle")
    
    # Verification des colones choisis pour être modifier et placement des widgets sur l'application en fonction
    global valueName, valuePwd, valueMail, valueTel, valueRole
    valueName = selectName.get()
    valuePwd = selectPwd.get()
    valueMail = selectMail.get()
    valueTel = selectTel.get()
    valueRole = selectRole.get()
    if valueName == 1:
        NameModif.place(x=50, y=20)
    else:
        pass
    if valuePwd == 1 and valueName == 1:
        PwdModif.place(x=50, y=60)
    elif valuePwd == 1 and valueName == 0:
        PwdModif.place(x=50, y=20)
    else:
        pass
    if valueMail == 1 and valueName == 1 and valuePwd == 1:
        MailModif.place(x=50, y=100)
    elif valueMail == 1 and valueMail == 0 and valuePwd == 1:
        MailModif.place(x=50, y=60)   
    elif valueMail == 1 and valueMail == 1 and valuePwd == 0:
        MailModif.place(x=50, y=60) 
    elif valueMail == 1 and valueMail == 0 and valuePwd == 0:
        MailModif.place(x=50, y=20)
    else:
        pass
    if valueTel == 1 and valueName == 1 and valuePwd == 1 and valueMail == 1:
        TelModif.place(x=50, y=140)
    elif valueTel == 1 and valueName == 0 and valuePwd == 1 and valueMail == 1:
        TelModif.place(x=50, y=100)
    elif valueTel == 1 and valueName == 1 and valuePwd == 0 and valueMail == 1:
        TelModif.place(x=50, y=100)
    elif valueTel == 1 and valueName == 1 and valuePwd == 1 and valueMail == 0:
        TelModif.place(x=50, y=100)
    elif valueTel == 1 and valueName == 0 and valuePwd == 0 and valueMail == 1:
        TelModif.place(x=50, y=60)
    elif valueTel == 1 and valueName == 1 and valuePwd == 0 and valueMail == 0:
        TelModif.place(x=50, y=60)
    elif valueTel == 1 and valueName == 0 and valuePwd == 1 and valueMail == 0:
        TelModif.place(x=50, y=60)
    elif valueTel == 1 and valueName == 0 and valuePwd == 0 and valueMail == 0:
        TelModif.place(x=50, y=20)
    else:
        pass
    if valueRole == 1 and valueName == 1 and valuePwd == 1 and valueMail == 1 and valueTel == 1:
        RoleModif.place(x=50, y=180)
    elif valueRole == 1 and valueName == 0 and valuePwd == 1 and valueMail == 1 and valueTel == 1:
        RoleModif.place(x=0, y=140)
    elif valueRole == 1 and valueName == 1 and valuePwd == 0 and valueMail == 1 and valueTel == 1:
        RoleModif.place(x=0, y=140)
    elif valueRole == 1 and valueName == 1 and valuePwd == 1 and valueMail == 0 and valueTel == 1:
        RoleModif.place(x=0, y=140)
    elif valueRole == 1 and valueName == 1 and valuePwd == 1 and valueMail == 1 and valueTel == 0:
        RoleModif.place(x=0, y=140)
    elif valueRole == 1 and valueName == 0 and valuePwd == 0 and valueMail == 1 and valueTel == 1:
        RoleModif.place(x=0, y=100)
    elif valueRole == 1 and valueName == 1 and valuePwd == 1 and valueMail == 0 and valueTel == 0:
        RoleModif.place(x=0, y=100)
    elif valueRole == 1 and valueName == 0 and valuePwd == 1 and valueMail == 1 and valueTel == 0:
        RoleModif.place(x=0, y=100)
    elif valueRole == 1 and valueName == 1 and valuePwd == 0 and valueMail == 0 and valueTel == 1:
        RoleModif.place(x=0, y=100)
    elif valueRole == 1 and valueName == 1 and valuePwd == 0 and valueMail == 0 and valueTel == 0:
        RoleModif.place(x=0, y=60)
    elif valueRole == 1 and valueName == 0 and valuePwd == 1 and valueMail == 0 and valueTel == 0:
        RoleModif.place(x=0, y=60)
    elif valueRole == 1 and valueName == 0 and valuePwd == 0 and valueMail == 1 and valueTel == 0:
        RoleModif.place(x=0, y=60)
    elif valueRole == 1 and valueName == 0 and valuePwd == 0 and valueMail == 0 and valueTel == 1:
        RoleModif.place(x=0, y=60)
    elif valueRole == 1 and valueName == 0 and valuePwd == 0 and valueMail == 0 and valueTel == 0:
        RoleModif.place(x=0, y=20)
    else:
        pass
    
    btn_validate_mofif = customtkinter.CTkButton(ValidateModifBody, text="Valider les modifications", font=("Calibri",12), fg_color="green", text_color="white", width=250, command=send_modifications)
    btn_validate_mofif.place(x=50, y=220)

# Fonction permettant de choisir l'utilisateur a modifier ainsi que les données a modifier
def modif_user():
        
    new_body.destroy()
    all_users = []
    
    # Recuperation de tous les noms et prénoms des utilisateurs de la base de donnée
    try:
        database = pymysql.connect(host="localhost", user="root", password="", db="appobjet")
        try:
            with database.cursor() as request:
                selectUsers = "SELECT nom, prenom FROM utilisateurs"
                request.execute(selectUsers)
                users = request.fetchall()
                for user in users:
                    all_users.append(user)
        except Exception as erreur:
            print(erreur)
    except Exception as err:
        print(err)
    
    # Creation d'un nouveau corps pour paramettrer la modification des utilisateurs
    global ModifUserBody, modifNameInput, modifFirstNameInput, selectName, selectPwd, selectMail, selectTel, selectRole
    ModifUserBody = customtkinter.CTkFrame(root, width=350, height=400)
    ModifUserBody.place(x=0, y=100)
    
    NameTitle = customtkinter.CTkLabel(ModifUserBody, text="Nom", font=("Calibri",12), text_color="white", width=10)
    NameTitle.place(x=70, y=20)
    modifNameInput = customtkinter.CTkEntry(ModifUserBody, placeholder_text="Entrez le nom de l'utilisateur", font=("Calibri",12), text_color="white", width=200)
    modifNameInput.place(x=70, y=45)
    
    FirstNameTitle = customtkinter.CTkLabel(ModifUserBody, text="Prénom", font=("Calibri",12), text_color="white", width=10)
    FirstNameTitle.place(x=70, y=75)
    modifFirstNameInput = customtkinter.CTkEntry(ModifUserBody, placeholder_text="Entrez le prénom de l'utilisateur", font=("Calibri",12), text_color="white", width=200)
    modifFirstNameInput.place(x=70, y=100)
    
    selectName = customtkinter.CTkCheckBox(ModifUserBody, text="Nom", font=("Calibri",16), width=10, text_color="white")
    selectName.place(x=50, y=140)
    
    selectPwd = customtkinter.CTkCheckBox(ModifUserBody, text="Mot de passe", font=("Calibri",16), width=10, text_color="white")
    selectPwd.place(x=50, y=170)
    
    selectMail = customtkinter.CTkCheckBox(ModifUserBody, text="E-mail", font=("Calibri",16), width=10, text_color="white")
    selectMail.place(x=50, y=200)
    
    selectTel = customtkinter.CTkCheckBox(ModifUserBody, text="Téléphone", font=("Calibri",16), width=10, text_color="white")
    selectTel.place(x=50, y=230)
    
    selectRole = customtkinter.CTkCheckBox(ModifUserBody, text="Rôle", font=("Calibri",16), width=10, text_color="white")
    selectRole.place(x=50, y=260)
    
    btn_modif_continue = customtkinter.CTkButton(ModifUserBody, text="Continuer", font=("Calibri",12), text_color="white", fg_color="green", width=250, command=validate_modifications)
    btn_modif_continue.place(x=50, y=300)

# Fonction permettant de valider la connexion d'un utilisateur 
def validate_authentification():
    login = loginInput.get()
    pwd = pwdInput.get()
    logs = []
    n = 0
    # Connection a la base de donnée pour comparer l'username et le password
    try: 
        bdd = pymysql.connect(host='localhost', user='root', password="", db="appobjet")
        with bdd.cursor() as request:
            select = 'SELECT login, pwd, roles from utilisateurs'
            request.execute(select)
            results = request.fetchall()
            for result in results:
                logs.append(result)
    except Exception as errrr:
        print(errrr)
    
    # Hashage des password pour pouvoir les comparer a ceux de la base de donnée
    adminPwd = "password"
    hashageAdminPws = hashlib.sha256(adminPwd.encode())
    hash_adminPwd = hashageAdminPws.hexdigest()
    hashage = hashlib.sha256(pwd.encode())
    hash_pwd = hashage.hexdigest()
    for i in logs:
        # Verification de qui se connecte a l'application (admin, scientifique, medecin, commercial ou assistant)
        if login == logs[n][0] and hash_pwd == logs[n][1]:
            if logs[n][2] == "Scientifique":
                body.destroy()
                
                new_body = customtkinter.CTkFrame(root, width=350, height=400)
                new_body.place(x=0, y=100)
                
                title = customtkinter.CTkLabel(new_body, text="Bienvenu sur l'espace Scientifique", font=("Calibri",14), text_color="white", width=20)
                title.place(x=80, y=30)
                subtitle = customtkinter.CTkLabel(new_body, text="Vous avez accès aux documents en lecture et écriture", font=("Calibri",14), text_color="white", width=30)
                subtitle.place(x=10, y=60)
            elif logs[n][2] == "Medecin":
                body.destroy()
               
                new_body = customtkinter.CTkFrame(root, width=350, height=400)
                new_body.place(x=0, y=100)
                
                title = customtkinter.CTkLabel(new_body, text="Bienvenu sur l'espace Médecin", font=("Calibri",14), text_color="white", width=20)
                title.place(x=80, y=30)
                subtitle = customtkinter.CTkLabel(new_body, text="Vous avez accès aux documents en lecture et écriture limitée", font=("Calibri",14), text_color="white", width=30)
                subtitle.place(x=10, y=60)
                
            elif logs[n][2] == "Commercial":
                body.destroy()
                
                new_body = customtkinter.CTkFrame(root, width=350, height=400)
                new_body.place(x=0, y=100)
                
                title = customtkinter.CTkLabel(new_body, text="Bienvenu sur l'espace Commercial", font=("Calibri",14), text_color="white", width=20)
                title.place(x=80, y=30)
                subtitle = customtkinter.CTkLabel(new_body, text="Vous avez accès aux documents en lecture uniquement", font=("Calibri",14), text_color="white", width=30)
                subtitle.place(x=10, y=60)
                
            elif logs[n][2] == "Assistant":
                body.destroy()
                
                new_body = customtkinter.CTkFrame(root, width=350, height=400)
                new_body.place(x=0, y=100)
                
                title = customtkinter.CTkLabel(new_body, text="Bienvenu sur l'espace Assistant", font=("Calibri",14), text_color="white", width=20)
                title.place(x=80, y=30)
                subtitle = customtkinter.CTkLabel(new_body, text="Vous avez accès aux documents en lecture uniquement", font=("Calibri",14), text_color="white", width=30)
                subtitle.place(x=10, y=60)
                
            elif login == "admin" and hash_pwd == hash_adminPwd:
                body.destroy()

                # Creation d'un nouveau corps pour l'interface administrateur de l'application
                global NewBody
                def NewBody():
                    global new_body
                    new_body = customtkinter.CTkFrame(root, width=350, height=400)
                    new_body.place(x=0, y=100)

                    btn_add_user = customtkinter.CTkButton(new_body, text="Ajouter un utilisateur", font=("Arial",12), text_color="white", width=200, command=add_user)
                    btn_add_user.place(x=70, y=30) 
                    
                    btn_del_user = customtkinter.CTkButton(new_body, text="Supprimer un utilisateur", font=("Arial",12), text_color="white", width=200, command=del_user)
                    btn_del_user.place(x=70, y=70)
                    
                    btn_modif_user = customtkinter.CTkButton(new_body, text="Modifier un utilisateur", font=("Arial",12), text_color="white", width=200, command=modif_user)
                    btn_modif_user.place(x=70, y=110)
                    
                    btn_list_user = customtkinter.CTkButton(new_body, text="Lister les utilisateurs", font=("Arial",12), text_color="white", width=200, command=list_user)
                    btn_list_user.place(x=70, y=150)
                    
                    btn_quit = customtkinter.CTkButton(new_body, text="Quitter la session", font=("Arial",12), text_color="white", fg_color='red', width=200, command=quit_session)
                    btn_quit.place(x=70, y=200)
                
                NewBody()
        else:
            global fail_log
            fail_log += 1
            if fail_log >= 5:
                blocked = customtkinter.CTkLabel(body, text="Votre compte à été bloqué, contactez vos superieurs", font=("Calibri",10), text_color='red', width=20, justify='center')
                blocked.place(x=60, y=160)
                blocked = True
                validate.destroy()
            else:
                try: 
                    loginErreur = customtkinter.CTkLabel(body, text="Les informations sont incorrectes, rééssayez", font=("Calibri",10), text_color='red', width=20, justify='center')
                    loginErreur.place(x=90, y=160)
                except:
                    pass
        n += 1

# Fonction permettant d'afficher la fenetre de connexion
def window():
    # Parametrage de la fenetre de connexion
    global root
    root = customtkinter.CTk()
    root.title("Login")
    root.geometry("350x500")
    root.minsize(350,500)
    root.maxsize(350,500)

    # Creation d'un header commun a toute les pages de l'application
    header = customtkinter.CTkFrame(root, width=350, height=100)
    header.place(x=0, y=0)

    title = customtkinter.CTkLabel(header, text="SnTLabo", font=("Arial",26), width=10)
    title.place(x=120, y=35)

    global home_body
    
    # Creation d'un corps qui changera en fonction des pages de l'application
    def home_body():
        
        global body, loginInput, pwdInput, validate
        body = customtkinter.CTkFrame(root, width=350, height=400)
        body.place(x=0, y=100)

        loginTitle = customtkinter.CTkLabel(body, text='Login : ', font=("Calibri",14), width=10)
        loginTitle.place(x=70, y=20)

        loginInput = customtkinter.CTkEntry(body, font=("Calibri",12), placeholder_text="Entrez votre nom d'utilisateur", width=200)
        loginInput.place(x=70, y=50)

        pwdTitle = customtkinter.CTkLabel(body, text='Password : ', font=("Calibri",14), width=10)
        pwdTitle.place(x=70, y=90)

        pwdInput = customtkinter.CTkEntry(body, font=("Calibri",12), placeholder_text="Entrez votre mot de passe", width=200, show="*")
        pwdInput.place(x=70, y=120)

        validate = customtkinter.CTkButton(body, text='Valider', font=("Calibri",12), fg_color='green', width=200, command=validate_authentification)
        validate.place(x=70, y=190)
    home_body()

    root.mainloop()
