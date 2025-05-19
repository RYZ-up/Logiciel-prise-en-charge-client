from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import platform
from customtkinter import *
from PIL import Image
from datetime import datetime,date
from tkcalendar import Calendar
import shutil
from PyPDF2 import PdfReader, PdfWriter
import io
import win32api
import smtplib
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import subprocess
import logging
import sqlite3
import threading

def mise_a_jour_parameters(): 
    global values_color,values_modele,values_reparations_possibles,identifiant_de_connexion,mot_de_passe_de_connexion
    resultats_indexs = gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "index_data", None, 5)
    resultats_marque = gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "marque", None, 5)
    resultats_couleur = gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "couleur", None, 5)
    resultats_reparation = gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "reparation", None, 5)
    resultats_identifiant = gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "identifiant", None, 5)
    resultats_motdepasse = gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "motdepasse", None, 5)

    values_color = []
    values_modele = []
    values_reparations_possibles = []
    for element in resultats_marque : 
        if element[0] == None : 
            pass
        else : 
            values_modele.append(element[0])
    

    for element in resultats_couleur : 
        if element[0] == None : 
            pass
        else : 
            values_color.append(element[0])
    

    for element in resultats_reparation : 
        if element[0] == None : 
            pass
        else : 
            values_reparations_possibles.append(element[0])
    


    
    identifiant_de_connexion = str((resultats_identifiant[0][0]).strip())
    mot_de_passe_de_connexion = str((resultats_motdepasse[0][0]).strip())





    print("parameters mis a jours")
def mise_a_jour_index(x = 0):
    global database_python,resultats_index
    
    # Récupérer les résultats de l'index
    resultats_index = gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA", "data_index", None, 5)
    resultats_name = gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA", "name", None, 5)




    
    max_val = max((e for element in resultats_index for e in element if isinstance(e, (int, float))), default=-float('inf'))
    index_actuelle.configure(text=str(max_val + 1))

    if x == 1:
        database_python = []
        for element in resultats_name:
            valeur_recherche = element[0] 

            resultats_lignes = gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA", "name", valeur_recherche, 7)


            database_python.append(resultats_lignes)
    else : 
        pass
def gestion_bdd(a, b, c, d, e, f=None):
    """
    Fonction pour gérer une base de données SQL.

    :param a: Nom de la base de données.
    :param b: Nom de la table.
    :param c: Nom de la colonne (ou liste de colonnes pour ajout multiple).
    :param d: Valeur pour l'opération (clé de recherche ou valeurs à insérer).
    :param e: Action (1 = Mettre à NULL, 2 = Modifier, 3 = Ajouter, 4 = Supprimer, 5 = Récupérer une colonne, 6 = Ajouter une liste dans une ligne, 7 = Récupérer une ligne complète).
    :param f: Nouvelle valeur (pour modification ou liste d'insertion pour `e == 6`).
    """
    try:
        conn = sqlite3.connect(a)
        cursor = conn.cursor()

        if e == 1 and c:  # Mettre un élément d'une colonne à NULL
            sql = f"UPDATE {b} SET {c} = NULL WHERE {c} = ?"
            cursor.execute(sql, (d,))
            print(f"Valeur {d} mise à NULL dans la colonne {c}.")

        elif e == 2 and f is not None:  # Modifier un élément
            sql = f"UPDATE {b} SET {c} = ? WHERE {c} = ?"
            cursor.execute(sql, (f, d))
            print(f"Valeur {d} modifiée en {f} dans la colonne {c}.")

        elif e == 3:  # Ajouter un élément unique
            sql = f"INSERT INTO {b} ({c}) VALUES (?)"
            cursor.execute(sql, (d,))
            print(f"Valeur {d} ajoutée dans la colonne {c}.")

        elif e == 4:  # Supprimer une ligne
            if c:  # On vérifie qu'une colonne de condition est fournie
                sql = f"DELETE FROM {b} WHERE {c} = ?"
                cursor.execute(sql, (d,))
                print(f"Ligne avec {c} = {d} supprimée de la table {b}.")
            else:
                print("Erreur : La condition de suppression est manquante.")

        elif e == 5:  # Récupérer une colonne
            sql = f"SELECT {c} FROM {b}" if d is None else f"SELECT {c} FROM {b} WHERE {c} = ?"
            cursor.execute(sql, (d,)) if d is not None else cursor.execute(sql)
            return cursor.fetchall()

        elif e == 6 and isinstance(f, list):  # Ajouter une liste dans une ligne
            if isinstance(c, list) and len(c) == len(f):  # Vérifier correspondance colonnes/valeurs
                placeholders = ', '.join(['?'] * len(f))  # Générer `?` pour chaque valeur
                columns = ', '.join(c)  # Liste des colonnes formatée
                sql = f"INSERT INTO {b} ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, tuple(f))
                print(f"Ligne ajoutée dans {b} avec les valeurs : {f}.")
            else:
                print("Erreur: Le nombre de colonnes et de valeurs ne correspond pas.")

        elif e == 7 and d is not None:  # Récupérer une ligne entière
            sql = f"SELECT * FROM {b} WHERE {c} = ?"
            cursor.execute(sql, (d,))
            return cursor.fetchall()

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        print(f"Erreur SQL : {error}")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
def start():
    global background3,background2,background1
    background1.destroy()
    background2.destroy()
    background3.destroy()
    root.bind("<Escape>",on_tab)
    root.bind("<Alt_L>",on_space)
    root.bind("<Control-s>", database_link_1)
    root.bind("<Control-i>", print_to_pdf)
    root.bind("<Control-q>", lambda event: root.destroy())

    root.bind("<Control-n>", clear)

def send_mail():
    threading.Thread(target=send_mail_thread, daemon=True).start()
def send_mail_thread():
    global entrys, date_aujourdhui
    

    try:
        # Vérification de l'email
        fameux_mail = entrys[11].get().strip()
        if not fameux_mail:
            raise ValueError("L'adresse email est vide ou invalide.")
        
        logging.info(f"Envoi de l'email à : {fameux_mail}")

        # Construction du chemin du fichier
        file_path = f"PDFs\{entrys[8].get()}-{entrys[9].get()}-{date_aujourdhui}.pdf"
        
        if not os.path.exists(file_path):
            logging.warning(f"Le fichier '{file_path}' n'existe pas. Génération du PDF...")
            try:
                print_to_pdf(1)
                root.after(5500, database_link_1)
                  # Assurez-vous que cette fonction est bien définie
            except Exception as e:
                raise RuntimeError(f"Erreur lors de la génération du PDF : {e}")
        else:
            logging.info(f"Le fichier '{file_path}' existe déjà.")

        # Configuration de l'email
        expediteur = "noreplyphoneaddict@gmail.com"
        mot_de_passe = "oqie nflc ztzc nysa"  # Ne pas mettre en dur dans la version finale !
        destinataire = fameux_mail

        message = MIMEMultipart()
        message["From"] = expediteur
        message["To"] = destinataire
        message["Subject"] = "Bon de prise en charge - ATELIER PHONE ADDICT -"
        
        # Corps de l'email
        corps = "Bonjour,\n\nVoici le bon de prise en charge ci-joint.\n\nCordialement."
        message.attach(MIMEText(corps, "plain"))

        # Pièces jointes
        fichiers = [
            getressources(file_path),
            getressources("CONDITIONS-GENERALES-DE-VENTE-PHONE-ADDICT.pdf")  # Vérifiez que cette fonction existe
        ]

        for fichier in fichiers:
            if os.path.exists(fichier):
                try:
                    with open(fichier, "rb") as attachement:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachement.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename={os.path.basename(fichier)}"
                        )
                        message.attach(part)
                except Exception as e:
                    logging.error(f"Erreur lors de l'attachement du fichier {fichier} : {e}")
                    raise
            else:
                logging.warning(f"Fichier introuvable : {fichier}")

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as serveur:  # Correction du port SMTP
                serveur.starttls()  # Sécurisation de la connexion
                serveur.login(expediteur, mot_de_passe)
                serveur.sendmail(expediteur, destinataire, message.as_string())
                frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
                frame_flot.place(x=225, y=10)

                label = CTkLabel(frame_flot, text="Mail envoyé", text_color="white",
                                  width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                                  font=("Verdana", 14))
                label.pack(padx=10, pady=(5, 2))
                # Barre de progression dans le frame

                progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                              width=200, height=5)
                progress_bar.pack(padx=10, pady=(0, 5))
                progress_bar.set(1.0)  # Définition de la valeur initiale
                # Assurer que le frame reste au-dessus
                frame_flot.lift()
                # Lancer la diminution après 1 seconde
                diminuer_progression(progress_bar, label, frame_flot)
                logging.info("✅ Email envoyé avec succès !")
        except smtplib.SMTPException as e:
            raise RuntimeError(f"Erreur lors de l'envoi de l'email : {e}")

    except Exception as e:
        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)

        label = CTkLabel(frame_flot, text="Mail vide ou incorrect", text_color="white",
                          width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                          font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame python -m pip install auto-py-to-exe --upgrade python -m pip install pyinstaller --upgrade

        progress_bar = CTkProgressBar(frame_flot, progress_color="red",
                                      width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)
        logging.error(f"❌ Une erreur est survenue dans send_mail : {e}")
    mise_a_jour_index(1)
    hide_panel()
def on_tab(event):
    global main_button
    if not main_button.winfo_exists():  # Vérifie si le bouton existe toujours
        return "break"
    main_button.invoke()  # Simule un clic sur le bouton

    return "break"
def on_space(event):
    global next_bouton,page_actuelle,back_bouton
    if page_actuelle == 1: 
        if not next_bouton.winfo_exists():  # Vérifie si le bouton existe toujours
            return "break"
        next_bouton.invoke()
    elif page_actuelle == 2 :
        if not back_bouton.winfo_exists():  # Vérifie si le bouton existe toujours
            return "break"
        back_bouton.invoke()


    return "break"
def slide_panel(x_target):
    """ Fait glisser le panneau jusqu'à x_target avec une animation fluide. """
    x_current = panel.winfo_x()
    if x_current != x_target:
        step = 20 if x_current < x_target else -20  
        x_new = x_current + step if abs(x_current - x_target) > 20 else x_target
        panel.place(x=x_new, y=5)
        root.after(10, lambda: slide_panel(x_target))
def show_panel():
    global main_button, big_back_button,panel,elements_in_root,elements_in_root1,elements_in_root2,elements_in_root3
    main_button.configure(command=hide_panel)
    big_back_button = CTkButton(root, text="", command=hide_panel, width=1000, height=1000, fg_color="#202020", bg_color="#202020",hover = False)
    big_back_button.place(x=0, y=0)
    panel.lift()  
    if page_actuelle == 1 : 

        for boutons in elements_in_root:
            boutons.lift()
        for boutons in timeliste:
            try : 
                boutons.lift()
            except Exception as e :
                pass
    elif page_actuelle == 2 : 
        for boutons in elements_in_root1:
            boutons.lift()
        for boutons in timeliste:
            try : 
                boutons.lift()
            except Exception as e :
                pass
    elif page_actuelle == 3: 
        for boutons in elements_in_root2:
            try : 
                boutons.lift()
            except :
                print("element already destroyed")
        for boutons in timeliste:
            try : 
                boutons.lift()
            except Exception as e :
                pass

    elif page_actuelle == 4 : 
        

        for boutons in elements_in_root3:
            try : 
                boutons.lift()
            except :
                pass
        for boutons in timeliste:
            try : 
                boutons.lift()
            except Exception as e :
                pass
    else : 
        pass
            
    slide_panel(0)  
def hide_panel():
    global main_button, big_back_button
    slide_panel(-panel_width)
    main_button.configure(command=show_panel)
    big_back_button.destroy()
def getressources(ressources):
    try:
        base_path = sys._MEIPASS  # Si le code est exécuté à partir d'un fichier pyinstaller
    except Exception:
        base_path = os.path.abspath(".")  # Si le code est exécuté depuis un fichier normal
    
    return os.path.join(base_path, ressources)
def update_time():
    global cal

    # 🔹 Obtenir la date actuelle
    date_aujourdhui = date.today()
    date_fr = str(date_aujourdhui).split("-")  # ["YYYY", "MM", "DD"]

    # 🔹 Formater correctement la date pour l'affichage
    current_date_for_label = f"{date_fr[2]} / {date_fr[1]} / {date_fr[0]}"

    # 🔹 Mettre à jour l'affichage de la date sans modifier `timeliste`
    timeliste[0].configure(text=current_date_for_label)

    # 🔹 Mettre à jour l'heure
    current_time = datetime.now().strftime("%H:%M:%S")
    label_hour_calendar.configure(text=current_time)

    # 🔹 Mettre à jour le calendrier proprement
    today = datetime.today().date()  # Extraire uniquement la date
    cal.calevent_remove('today')  # Supprimer l'ancien événement
    cal.calevent_create(today, "Aujourd'hui", "today")
    cal.tag_config('today', foreground="#ff0000", background="#202020")

    # 🔹 Rafraîchir la mise à jour toutes les secondes
    root.after(1000, update_time)
def boutons_panel():
    global enregistrer_button
    close_button = CTkLabel(panel, text="",fg_color = "#292929",width = 5,height = 5,image =photo_menu)
    close_button.place(y=-15, x=25)
    close_button = CTkButton(panel, text="",command=hide_panel,fg_color = "#292929",image= photo_3,width = 15,height = 15,hover="gray")
    close_button.place(y=2.5, x=180)

    enregistrer_button = CTkButton(panel, text="Enregistrer",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17),command = database_link_1)
    enregistrer_button.place(x=70, y=150)
    enregistrer_button_image = CTkLabel(panel, text="",corner_radius=10,text_color="white",bg_color = "#292929",fg_color="#292929",width = 40,height = 40,image = photo_save)
    enregistrer_button_image.place(x=20, y=150)

    main_button = CTkButton(panel, text="Effacer",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17),command = lambda : intermediaire(1))
    main_button.place(x=70, y=205)
    main_button = CTkLabel(panel, text="",corner_radius=10,text_color="white",bg_color = "#292929",fg_color="#292929",width = 40,height = 40,image = photo_clear)
    main_button.place(x=20, y=205)

    main_button = CTkButton(panel, text="Imprimer",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17),command=print_to_pdf)
    main_button.place(x=70, y=260)
    main_button = CTkLabel(panel, text="",corner_radius=10,text_color="white",bg_color = "#292929",fg_color="#292929",width = 40,height = 40,image = photo_print)
    main_button.place(x=20, y=260)

    main_button = CTkButton(panel, text="Imprimer CGV",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17) ,command = lambda :imprimation(1))
    main_button.place(x=70, y=315)
    main_button = CTkLabel(panel, text="",corner_radius=10,text_color="white",fg_color="#292929",bg_color="#292929",width = 40,height = 40,image = photo_cgv)
    main_button.place(x=20, y=315)

    main_button = CTkButton(panel, text="Ouvrir PDFs",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17),command = open_file_manager)
    main_button.place(x=70, y=370)
    main_button = CTkLabel(panel, text="",corner_radius=10,text_color="white",bg_color = "#292929",fg_color="#292929",width = 40,height = 40,image = photo_folder)
    main_button.place(x=20, y=370)

    main_button = CTkButton(panel, text="Envoyer Mail",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17), command = send_mail)
    main_button.place(x=70, y=425)
    main_button = CTkLabel(panel, text="",corner_radius=10,text_color="white",bg_color = "#292929",fg_color="#292929",width = 40,height = 40,image = photo_mail)
    main_button.place(x=20, y=425)

    main_button = CTkButton(panel, text="Historique",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17),command = history)
    main_button.place(x=70, y=480)
    main_button = CTkLabel(panel, text="",corner_radius=10,text_color="white",bg_color = "#292929",fg_color="#292929",width = 40,height = 40,image = photo_history)
    main_button.place(x=20, y=480)

    main_button = CTkButton(panel, text="Administrateur",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17),command = admin_interface_connexion)
    main_button.place(x=70, y=535)
    main_button = CTkLabel(panel, text="",corner_radius=10,text_color="white",bg_color = "#292929",fg_color="#292929",width = 40,height = 40,image = photo_admin)
    main_button.place(x=20, y=535)
def admin_interface_connexion():
    global database_python,page_actuelle,panel,elements_in_root3,mot_de_passe,identifiant,timeliste,try_validate
    page_actuelle = 4
    root.unbind("<Alt_L>")
    root.unbind("<Control-s>")
    root.bind("<Control-i>")

    root.unbind("<Control-n>")
    


    background1 = CTkLabel(root,width = 750,height = 620,fg_color = "#202020",text = "")
    background1.place(x = 275,y = 60)

    background_panel1 = CTkLabel(panel,width = 750,height = 500,fg_color = "#292929",text = "")
    background_panel1.place(x = 0,y = 150)
    main_button1 = CTkButton(panel, text="Accueil",corner_radius=10,text_color="white",bg_color="#292929",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17),command = lambda :intermediaire(4))
    main_button1.place(x=55, y=150)
    main_button_image1 = CTkLabel(panel, text="",width= 40,height=40,image= home_photo)
    main_button_image1.place(x=10, y=150)

    progress_bar1 = CTkProgressBar(root, width=300, height=5, fg_color="black", progress_color="white",)
    progress_bar1.place(x = 350,y = 250)
    progress_bar1.set(1)
    identifiant = CTkEntry(root,width= 250,height = 50 , placeholder_text= "Identifiant" ,corner_radius= 15,fg_color= "#202020",border_width= 0,font = ("verdana",20),bg_color="#202020",placeholder_text_color="grey")
    identifiant.place(x = 350,y = 200)


    progress_bar2 = CTkProgressBar(root, width=300, height=5, fg_color="black", progress_color="white",)
    progress_bar2.place(x = 350,y = 350)
    progress_bar2.set(1)
    mot_de_passe = CTkEntry(root,width= 250,height = 50 , placeholder_text= "Mot de passe" ,show = "•",corner_radius= 15,fg_color= "#202020",border_width= 0,font = ("verdana",20),bg_color="#202020",placeholder_text_color="grey")
    mot_de_passe.place(x = 350,y = 300)
    try_validate = CTkButton(root,text = "Connexion",width = 150,height = 50,corner_radius= 50,bg_color= "#202020",fg_color="#202020",border_color="orange",border_width=2,hover_color= "orange",font = ("verdana",20),command = trynaenter)
    try_validate.place(x = 400,y = 400)
    root.bind("<Return>",trynaenter)
    hide_panel()

    elements_in_root3.append(background1)
    elements_in_root3.append(background_panel1)
    elements_in_root3.append(progress_bar1)
    elements_in_root3.append(progress_bar2)
    elements_in_root3.append(identifiant)
    elements_in_root3.append(mot_de_passe)
    elements_in_root3.append(try_validate)
    elements_in_root3.append(main_button1)
    elements_in_root3.append(main_button_image1)
def trynaenter(event = None):
    global mot_de_passe, identifiant, try_validate,identifiant_de_connexion,mot_de_passe_de_connexion

    if mot_de_passe.get() == mot_de_passe_de_connexion and identifiant.get() == identifiant_de_connexion:
        try_validate.configure(hover=False,border_color = 'green')
        try_validate.configure(text="Connecté!", fg_color="green", hover=False)
        root.after(1500, lambda: try_validate.configure(fg_color="#202020")) 
        root.after(1000, connected)  

    elif mot_de_passe.get() == "" and identifiant.get() == "":
        mot_de_passe.delete(0,"end")
        identifiant.delete(0,"end")
        mot_de_passe.configure(placeholder_text="*requis", placeholder_text_color="red")
        identifiant.configure(placeholder_text="*requis", placeholder_text_color="red")
        root.after(500, lambda: identifiant.configure(placeholder_text_color="grey")) 
        root.after(500, lambda: mot_de_passe.configure(placeholder_text_color="grey"))  

    else:
        mot_de_passe.delete(0,"end")
        identifiant.delete(0,"end")
        mot_de_passe.configure(placeholder_text="*incorrect", placeholder_text_color="red")
        identifiant.configure(placeholder_text="*incorrect", placeholder_text_color="red")
        root.after(500, lambda: identifiant.configure(placeholder_text_color="grey"))  
        root.after(500, lambda: mot_de_passe.configure(placeholder_text_color="grey"))  

    root.focus()
def connected():
    global database_python,elements_in_root3,label_state,trash_admin,first1
    root.unbind("<Return>")
    background12 = CTkLabel(root,width = 750,height = 500,fg_color = "#202020",text = "")
    background12.place(x = 275,y = 60)
    elements_in_root3.append(background12)
    trash_admin = []
    first1 = CTkScrollableFrame(root,width = 350,height = 585,fg_color="#292929",bg_color="#202020")
    first1.place(x= 300,y = 70)
    trash_admin.append(first1)  
    elements_in_root3.append(first1) 


    main_modeles = CTkButton(panel, text="Utilisateurs",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17),command = lambda : gération("users"))
    main_modeles.place(x=55, y=205)
    main_modeles_image = CTkLabel(panel, text="",corner_radius=10,text_color="white",bg_color = "#292929",fg_color="#292929",width = 40,height = 40,image = photo_options)
    main_modeles_image.place(x=5, y=205)

    main_couleurs = CTkButton(panel, text="Modèles",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17),command = lambda : gération("models"))
    main_couleurs.place(x=55, y=260)
    main_couleurs_image = CTkLabel(panel, text="",corner_radius=10,text_color="white",bg_color = "#292929",fg_color="#292929",width = 40,height = 40,image = photo_options)
    main_couleurs_image.place(x=5, y=260)

    main_reparation_type = CTkButton(panel, text="Couleurs",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17),command = lambda : gération("colors"))
    main_reparation_type.place(x=55, y=315)
    main_reparation_type_image = CTkLabel(panel, text="",corner_radius=10,text_color="white",fg_color="#292929",bg_color="#292929",width = 40,height = 40,image = photo_options)
    main_reparation_type_image.place(x=5, y=315)

    main_identifiant = CTkButton(panel, text="Réparations",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17),command = lambda : gération("reparations"))
    main_identifiant.place(x=55, y=370)
    main_identifiant_image = CTkLabel(panel, text="",corner_radius=10,text_color="white",bg_color = "#292929",fg_color="#292929",width = 40,height = 40,image =photo_options )
    main_identifiant_image.place(x=5, y=370)

    main_mot_de_passe = CTkButton(panel, text="Identifiants",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17),command = lambda : gération("identifiants"))
    main_mot_de_passe.place(x=55, y=425)
    main_mot_de_passe_image = CTkLabel(panel, text="",corner_radius=10,text_color="white",bg_color = "#292929",fg_color="#292929",width = 40,height = 40,image = photo_options)
    main_mot_de_passe_image.place(x=5, y=425)

    main_ajouter = CTkButton(panel, text="Ajouter",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17),command = lambda : gération("ajouter"))
    main_ajouter.place(x=55, y=480)
    main_ajouter_image = CTkLabel(panel, text="",corner_radius=10,text_color="white",bg_color = "#292929",fg_color="#292929",width = 40,height = 40,image = photo_options)
    main_ajouter_image.place(x=5, y=480)   

    main_modifier = CTkButton(panel, text="Modifier",corner_radius=10,text_color="white",hover_color="gray",fg_color="#202020",width = 150,height = 40,font = ("Arial",17),command = lambda : gération("modifier"))
    main_modifier.place(x=55, y=535)
    main_modifier_image = CTkLabel(panel, text="",corner_radius=10,text_color="white",bg_color = "#292929",fg_color="#292929",width = 40,height = 40,image = photo_options)
    main_modifier_image.place(x=5, y=535)



    elements_in_root3.append(main_modeles)
    elements_in_root3.append(main_modeles_image)

    elements_in_root3.append(main_couleurs)
    elements_in_root3.append(main_couleurs_image)

    elements_in_root3.append(main_reparation_type)
    elements_in_root3.append(main_reparation_type_image)

    elements_in_root3.append(main_identifiant)
    elements_in_root3.append(main_identifiant_image)

    elements_in_root3.append(main_mot_de_passe)
    elements_in_root3.append(main_mot_de_passe_image)

    elements_in_root3.append(main_modifier)
    elements_in_root3.append(main_modifier_image)

    elements_in_root3.append(main_ajouter)
    elements_in_root3.append(main_ajouter_image)


    label_state = CTkLabel(root, text="",corner_radius=10,text_color="orange",fg_color="#202020",width = 50,height = 25,bg_color= "#202020")
    label_state.place(y=680, x=520)
    
    elements_in_root3.append(label_state)
    gération("users")
def gération(x):
    global label_state,elements_in_root3,decision,trash_admin,database_python,values_modele,values_color,values_reparations_possibles,first1,choix_interaction_only,information,identifiant1,mot_de_passe1,try_validate1
    if x == 'users' :
        try :
            root.unbind("<Return>",trynavalidate)
        except : 
            pass
        
        label_state.configure(text = "Utilisateurs")
        for i in choix_interaction_only :
            try :
                i.destroy()
            except :
                pass
        for element in trash_admin[:0:-1]:  # On commence du dernier élément jusqu’au deuxième
            element.destroy()
            trash_admin.remove(element)

            
        for element,i in zip(database_python,range(len(database_python)+1)) : 
            tabel_filled1 = CTkButton(first1,command = lambda i = i: interaction(i,1),width = 300,height = 40,corner_radius=12.5,text = f"{str(element[0][1])} {str(element[0][2])}" ,bg_color="#292929",fg_color="#292929",font = ("arial",15),hover = False,border_color='white',border_width=3)
            tabel_filled1.pack(pady=10, padx=10)
            elements_in_root3.append(tabel_filled1)
            trash_admin.append(tabel_filled1)


    elif x == 'models' : 
        try :
            root.unbind("<Return>",trynavalidate)
        except : 
            pass
        label_state.configure(text = "Modèles")
        for i in choix_interaction_only :
            try :
                i.destroy()
            except :
                pass
        for element in trash_admin[:0:-1]:  # On commence du dernier élément jusqu’au deuxième
            element.destroy()
            trash_admin.remove(element)

            
        for i in range(len(values_modele)) : 
            tabel_filled1 = CTkButton(first1,command = lambda i = i: interaction(i,2),width = 300,height = 40,corner_radius=12.5,text = values_modele[i],bg_color="#292929",fg_color="#292929",font = ("arial",15),hover = False,border_color='white',border_width=3)
            tabel_filled1.pack(pady=10, padx=10)
            elements_in_root3.append(tabel_filled1)
            trash_admin.append(tabel_filled1)

    elif x == 'colors' : 
        try :
            root.unbind("<Return>",trynavalidate)
        except : 
            pass
        label_state.configure(text = "Couleurs")
        for i in choix_interaction_only :
            try :
                i.destroy()
            except :
                pass
        for element in trash_admin[:0:-1]:  # On commence du dernier élément jusqu’au deuxième
            element.destroy()
            trash_admin.remove(element)


        for i in range(len(values_color)) : 
            tabel_filled1 = CTkButton(first1,command = lambda i = i: interaction(i,3),width = 300,height = 40,corner_radius=12.5,text = values_color[i],fg_color="#292929",font = ("arial",15),hover = False,border_color='white',border_width=3)
            tabel_filled1.pack(pady=10, padx=10)
            elements_in_root3.append(tabel_filled1)
            trash_admin.append(tabel_filled1)


    elif x == 'reparations' : 
        try :
            root.unbind("<Return>",trynavalidate)
        except : 
            pass
        label_state.configure(text = "Réparations")
        for i in choix_interaction_only :
            try :
                i.destroy()
            except :
                pass
        for element in trash_admin[:0:-1]:  # On commence du dernier élément jusqu’au deuxième
            element.destroy()
            trash_admin.remove(element)


        for i in range(len(values_reparations_possibles)) : 
            tabel_filled1 = CTkButton(first1,command = lambda  i = i: interaction(i,4),width = 300,height = 40,corner_radius=12.5,text = values_reparations_possibles[i],bg_color="#292929",fg_color="#292929",font = ("arial",15),hover = False,border_color='white',border_width=3)
            tabel_filled1.pack(pady=10, padx=10)
            elements_in_root3.append(tabel_filled1)
            trash_admin.append(tabel_filled1)


    elif x == 'identifiants' : 
        label_state.configure(text = "Identifiants")
        for i in choix_interaction_only :
            try :
                i.destroy()
            except :
                pass
        for element in trash_admin[:0:-1]:  # On commence du dernier élément jusqu’au deuxième
            element.destroy()
            trash_admin.remove(element)

        cache = CTkLabel(root,width=400, height=635, fg_color="#292929",bg_color="#202020",text= "",corner_radius=60)
        cache.place(x = 280,y = 45)
        progress_bar11 = CTkProgressBar(root, width=300, height=5, fg_color="black", progress_color="white")
        progress_bar11.place(x = 350,y = 250)
        progress_bar11.set(1)
        identifiant1 = CTkEntry(root,width= 290,height = 50 , placeholder_text= "Identifiant" ,corner_radius= 15,fg_color= "#292929",border_width= 0,font = ("verdana",20),bg_color="#292929",placeholder_text_color="grey")
        identifiant1.place(x = 350,y = 200)
        identifiant1.configure(validate="key", validatecommand=(root.register(lambda v:  len(v)<= 20 or v == ""), "%P"))



        progress_bar21 = CTkProgressBar(root, width=300, height=5, fg_color="black", progress_color="white",)
        progress_bar21.place(x = 350,y = 350)
        progress_bar21.set(1)
        mot_de_passe1 = CTkEntry(root,width= 290,height = 50 , placeholder_text= "Mot de passe" ,show = "•",corner_radius= 15,fg_color= "#292929",border_width= 0,font = ("verdana",20),bg_color="#292929",placeholder_text_color="grey")
        mot_de_passe1.place(x = 350,y = 300)
        mot_de_passe1.configure(validate="key", validatecommand=(root.register(lambda v: len(v) <= 20 or v == ""), "%P"))



        try_validate1 = CTkButton(root,text = "Valider",width = 150,height = 50,corner_radius= 50,bg_color= "#292929",fg_color="#292929",border_color="orange",border_width=2,hover_color= "orange",font = ("verdana",20),command = trynavalidate)
        try_validate1.place(x = 405,y = 450)
        information = CTkLabel(root,width=300, height=50, fg_color="#292929",bg_color="#292929",text= "Entrez vos identifiants actuels",font =("verdana",20))
        information.place(x = 330,y = 70)

        elements_in_root3.append(cache)
        elements_in_root3.append(progress_bar21)
        elements_in_root3.append(progress_bar11)
        elements_in_root3.append(identifiant1)
        elements_in_root3.append(mot_de_passe1)
        elements_in_root3.append(progress_bar21)
        elements_in_root3.append(progress_bar21)
        elements_in_root3.append(try_validate1)
        elements_in_root3.append(information)

        trash_admin.append(cache)
        trash_admin.append(progress_bar21)
        trash_admin.append(progress_bar11)
        trash_admin.append(identifiant1)
        trash_admin.append(mot_de_passe1)
        trash_admin.append(progress_bar21)
        trash_admin.append(progress_bar21)
        trash_admin.append(try_validate1)
        trash_admin.append(information)
        root.bind("<Return>",trynavalidate)

    elif x == "ajouter" : 

        try :
            root.unbind("<Return>",trynavalidate)
        except : 
            pass
        label_state.configure(text = "Ajouter")
        for i in choix_interaction_only :
            try :
                i.destroy()
            except :
                pass
        for element in trash_admin[:0:-1]:  # On commence du dernier élément jusqu’au deuxième
            element.destroy()
            trash_admin.remove(element)
        cache = CTkLabel(root,width=400, height=635, fg_color="#292929",bg_color="#202020",text= "",corner_radius=60)
        cache.place(x = 280,y = 45)

        decision = CTkEntry(root,width= 290,height = 50 ,border_color="white",placeholder_text= "Contenu" ,corner_radius= 15,fg_color= "#292929",border_width= 2,font = ("verdana",20),bg_color="#292929",placeholder_text_color="grey")
        decision.place(x = 345,y = 150)
        decision.configure(validate="key", validatecommand=(root.register(lambda v:  len(v)<= 20 or v == ""), "%P"))

        information1 = CTkLabel(root,width=300, height=50, fg_color="#292929",bg_color="#292929",text= "Que souhaitez vous ajouter ?",font =("verdana",20))
        information1.place(x = 330,y = 70)
        information2 = CTkButton(root,width=380,corner_radius= 45,hover_color='orange',border_color="orange",border_width=2, height=50, fg_color="#292929",bg_color="#292929",text= "Couleurs de téléphones",font =("verdana",18),command = lambda : add(str(decision.get()),2))
        information2.place(x = 290,y =310)
        information3 = CTkButton(root,width=380,corner_radius= 45,hover_color='orange',border_color="orange",border_width=2, height=50, fg_color="#292929",bg_color="#292929",text= "Marques de téléphones",font =("verdana",18),command = lambda : add(str(decision.get()),1))
        information3.place(x = 290,y =390)
        information4 = CTkButton(root,width=380,corner_radius= 45,hover_color='orange',border_color="orange",border_width=2, height=50, fg_color="#292929",bg_color="#292929",text= "Types de réparations",font =("verdana",18),command = lambda : add(str(decision.get()),3))
        information4.place(x = 290,y =470)
        trash_admin.append(cache)
        trash_admin.append(decision)
        trash_admin.append(information1)
        trash_admin.append(information3)
        trash_admin.append(information2)
        trash_admin.append(information4)

        elements_in_root3.append(cache)
        elements_in_root3.append(decision)
        elements_in_root3.append(information1)
        elements_in_root3.append(information3)
        elements_in_root3.append(information2)
        elements_in_root3.append(information4)


        

    elif x == "modifier" : 

        try :
            root.unbind("<Return>",trynavalidate)
        except : 
            pass
        for i in choix_interaction_only :
            try :
                i.destroy()
            except :
                pass
        for element in trash_admin[:0:-1]:  # On commence du dernier élément jusqu’au deuxième
            element.destroy()
            trash_admin.remove(element)


        segmented_btn = CTkSegmentedButton(first1,selected_hover_color="orange",selected_color="orange", corner_radius=45,bg_color="#292929",width=120,border_width=2,fg_color="#202020",height = 50,values=["Couleurs", "Marques", "Réparations"], command=lambda c: update(c),font = ("verdana",12))
        segmented_btn.pack(padx = 10,pady = 10)
        trash_admin.append(segmented_btn)
        elements_in_root3.append(segmented_btn)

        # Liste pour stocker les boutons affichés
        buttons = []

        def update(choice):
            global values_color,values_modele,values_reparations_possibles,etat,etat_modifier_list
            if etat == 1: 
                for element in etat_modifier_list:
                    try:
                        element.destroy()  # Détruit l'élément s'il existe
                    except:
                        pass
                    try:
                        elements_in_root3.remove(element)  # Le retirer de la liste des éléments actifs
                    except:
                        pass
                    try:
                        trash_admin.remove(element)  # Le retirer de la liste des éléments à supprimer
                    except:
                        pass
                etat_modifier_list.clear()  # On vide la liste après suppression
        
            else:
                pass
            for btn in buttons:
                btn.destroy()
            buttons.clear()

            items = values_color if choice == "Couleurs" else values_modele if choice == "Marques" else values_reparations_possibles
            
            for i, item in enumerate(items):
                btn = CTkButton(first1, width=300, corner_radius=10, hover_color='orange',
                                border_color="orange", border_width=2, height=50,
                                fg_color="#292929", text=item, font=("verdana", 15),command = lambda i = i : modifyer(i,items))
                btn.pack(padx = 10,pady = 10)
                buttons.append(btn)
                elements_in_root3.append(btn)
                trash_admin.append(btn)

        # Ajout des éléments au stockage
        trash_admin.extend([segmented_btn])
        elements_in_root3.extend([segmented_btn])
        
        
            

    hide_panel()
def add(x,y):
    global values_color ,values_modele,values_reparations_possibles,decision
    if str(x) == "":
        return 
    if y == 1:
        gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "marque",str(x), 3)
        values_modele.append(str(x))
        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)
        label = CTkLabel(frame_flot, text="Marque ajoutée", text_color="white",
                          width=200, height=18, fg_color="#292929", corner_radius=10,bg_color="#202020",
                          font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame
        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                      width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)
    elif y == 2 : 
        gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "couleur", str(x), 3)

        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)
        label = CTkLabel(frame_flot, text="Couleur ajoutée", text_color="white",
                          width=200, height=18, fg_color="#292929", corner_radius=10,bg_color="#202020",
                          font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame
        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                      width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)
        values_color.append(str(x))
    else :
        gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "reparation", str(x), 3)
        values_reparations_possibles.append(str(x))
        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)
        label = CTkLabel(frame_flot, text="Type de réparation ajouté", text_color="white",
                          width=200, height=18, fg_color="#292929", corner_radius=10,bg_color="#202020",
                          font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame
        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                      width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)

    decision.delete(0,"end")
    root.focus()
def interaction(x,y):
    global values_color,values_modele,values_reparations_possibles,database_python,choix_interaction_only

    if choix_interaction_only == []:
        choix_interaction_only.clear()
        choix = CTkButton(first1,width = 90,height = 10,text = "Supprimer ",bg_color="#292929",fg_color="#f93a3a",text_color= "white",font = ("arial",15),corner_radius=90,hover_color='#ffa0a0',command = lambda : delete_row(x,y))
        choix.place(x = 12,y = 37 + (int(x) * 60))  
        elements_in_root3.append(choix)
        choix_interaction_only.append(choix)
        choix_interaction_only.append(x)
    else : 
        for i in choix_interaction_only :
            try :
                i.destroy()
            except :
                pass
        choix_interaction_only.clear()
        choix = CTkButton(first1,width = 90,height = 10,text = "Supprimer ",bg_color="#292929",fg_color="#f93a3a",text_color= "white",font = ("arial",15),corner_radius=90,hover_color='#ffa0a0',command = lambda : delete_row(x,y))
        choix.place(x = 12,y = 37 + (int(x) * 60))
        elements_in_root3.append(choix)
        choix_interaction_only.append(choix)
        choix_interaction_only.append(x)
def modifyer(x,y):
    global etat,etat_modifier_list,elements_in_root3,trash_admin,first1
    if etat == 1: 
        for element in etat_modifier_list:
            try:
                element.destroy()  # Détruit l'élément s'il existe
            except:
                pass
            try:
                elements_in_root3.remove(element)  # Le retirer de la liste des éléments actifs
            except:
                pass
            try:
                trash_admin.remove(element)  # Le retirer de la liste des éléments à supprimer
            except:
                pass
        etat_modifier_list.clear()  # On vide la liste après suppression

    else:
        pass

    # Création du champ d'entrée et du bouton seulement s'ils ne sont pas déjà présents
    nouvelle_piece = CTkEntry(first1, width=300, corner_radius=10,
                    border_color="white", border_width=2, height=50,
                    fg_color="#292929", placeholder_text="Nouveau contenu", font=("verdana", 15))
    nouvelle_piece.place(x=25, y=80 + (x * 70))

    nouvelle_piece1 = CTkButton(first1, width=25, height=40, corner_radius=15, fg_color="orange",
                                bg_color="#292929", hover_color="yellow", text="Valider",
                                text_color="black", command=lambda: valider_nouveau_contenu(None, x, nouvelle_piece.get(), y))
    nouvelle_piece1.place(x=245, y=85 + (x * 70))

    # Ajout des nouveaux éléments dans les listes de suivi
    etat_modifier_list.extend([nouvelle_piece, nouvelle_piece1])
    trash_admin.extend([nouvelle_piece, nouvelle_piece1])
    elements_in_root3.extend([nouvelle_piece, nouvelle_piece1])

    # Association de la touche "Entrée" pour valider
    root.bind("<Return>", valider_nouveau_contenu)

    etat = 1  # Met à jour l'état après création
def delete_row(x,y):
    global values_color,values_modele,values_reparations_possibles,database_python,choix_interaction_only
    if y == 1 : 
        end_deleting = 'users'

        gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA", "data_index", int(database_python[x][0][0]), 4)
        del database_python[x]
        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)

        label = CTkLabel(frame_flot, text="Utilisateur supprimé", text_color="white",
                          width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                          font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame

        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                      width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)
        
    elif y == 2 : 
        end_deleting = 'models'
        gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "marque", str(values_modele[x]), 1)
        del values_modele[x]
        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)

        label = CTkLabel(frame_flot, text="Marque supprimée", text_color="white",
                          width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                          font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame

        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                      width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)
    
    elif y == 3 : 
        end_deleting = 'colors'
        gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "couleur", str(values_color[x]), 1)  
        del values_color[x]
        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)

        label = CTkLabel(frame_flot, text="Couleur supprimée", text_color="white",
                          width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                          font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame

        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                      width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)

    elif y == 4 : 
        end_deleting = 'reparations'
        str(values_reparations_possibles[x])
        gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "reparation", str(values_reparations_possibles[x]), 1)  
        del values_reparations_possibles[x]
        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)

        label = CTkLabel(frame_flot, text="Réparation supprimée", text_color="white",
                          width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                          font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame

        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                      width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)

    for i in choix_interaction_only :
        try :
            i.destroy()
        except :
            pass

    gération(end_deleting)
def valider_nouveau_contenu(event = None ,x = None,y = None,z = None) : 
    global elements_in_root3,trash_admin,etat_modifier_list,etat,values_color,values_modele,values_reparations_possibles
    root.unbind("<Return>")

    if y == "" : 
        for element in etat_modifier_list : 
            element.destroy()
            elements_in_root3.remove(element)
            trash_admin.remove(element)
        etat_modifier_list.clear()
        gération("modifier")
        etat = 0
        return
    if z == values_reparations_possibles : 
        gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "marque", values_reparations_possibles[int(x)], 2, str(y))  # Modifie Alice en Alicia
        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)

        label = CTkLabel(frame_flot, text=f"{values_reparations_possibles[int(x)]} modifié en {str(y)} ", text_color="white",
                                  width=200, height=20, fg_color="#292929", corner_radius=10,bg_color="#202020",
                                  font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame

        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                              width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)

        values_reparations_possibles[int(x)] = str(y)
        intermediaire(4)
        
    elif z == values_color : 
        gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "couleur", values_color[int(x)], 2, str(y))  # Modifie Alice en Alicia
        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)

        label = CTkLabel(frame_flot, text=f"{values_color[int(x)]} modifié en {str(y)} ", text_color="white",
                                  width=200, height=20, fg_color="#292929", corner_radius=10,bg_color="#202020",
                                  font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame

        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                              width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)

        values_color[int(x)] = str(y)
        intermediaire(4)
        
    else : 
        gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "reparation", values_modele[int(x)], 2, str(y))  # Modifie Alice en Alicia
        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)

        label = CTkLabel(frame_flot, text=f"{values_modele[int(x)]} modifié en {str(y)} ", text_color="white",
                                  width=200, height=20, fg_color="#292929", corner_radius=10,bg_color="#202020",
                                  font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame

        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                              width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)

        values_modele[int(x)] = str(y)
        intermediaire(4)
        


    for element in etat_modifier_list : 
        element.destroy()
        elements_in_root3.remove(element)
        trash_admin.remove(element)
    etat_modifier_list.clear()
    
    gération("modifier")
    etat = 0
def diminuer_progression(progress_bar, label, frame, valeur_progress=1.0, decrement=0.02, interval=40):
    """Diminue la progress bar en 2 secondes et supprime label + barre à la fin."""
    if valeur_progress > 0:
        valeur_progress -= decrement  # Diminue progressivement
        progress_bar.set(valeur_progress)
        frame.lift()  # Assurer que le frame reste au premier plan
        progress_bar.after(interval, diminuer_progression, progress_bar, label, frame, valeur_progress, decrement, interval)
    else:
        frame.destroy() 
def history():
    global database_python, page_actuelle, elements_in_root2, panel, timeliste, first, element_positions
    element_positions = {}  # Dictionnaire pour stocker les positions des éléments visibles
    root.unbind("<Alt_L>")
    root.unbind("<Control-s>")
    root.unbind("<Control-n>")
    root.bind("<Control-i>")

    mise_a_jour_index(1)
    page_actuelle = 3

    background = CTkLabel(root, width=750, height=800, fg_color="#202020", text="")
    background.place(x=275, y=80)
    background_panel = CTkLabel(panel, width=750, height=500, fg_color="#202020", text="")
    background_panel.place(x=275, y=0)

    cache_panel = CTkLabel(panel, width=300, height=330, fg_color="#292929", text="")
    cache_panel.place(x=0, y=190)

    main_button = CTkButton(panel, text="Accueil", corner_radius=10, text_color="white", 
                            bg_color="#292929", hover_color="gray", fg_color="#202020", 
                            width=150, height=40, font=("Arial", 17), command=lambda: intermediaire(2))
    main_button.place(x=70, y=150)
    main_button_image = CTkLabel(panel, text="", width=40, height=40, image=home_photo)
    main_button_image.place(x=20, y=150)

    first = CTkScrollableFrame(root, width=350, height=585, fg_color="#292929", bg_color="#202020")
    first.place(x=300, y=70)

    hide_panel()

    elements_in_root2.extend([cache_panel, background_panel, main_button_image, background, main_button, first])

    if not database_python:
        label_empty = CTkLabel(root, width=60, height=20, text="Historique vide.",
                               font=("Arial", 15), bg_color="#292929", fg_color="#292929")
        label_empty.place(x=425, y=330)
        elements_in_root2.append(label_empty)
    else:
        # Barre de recherche
        search_var = StringVar()
        placeholder_text = "Rechercher..."
        search_entry = CTkEntry(first, width=300, height=30, corner_radius=12.5, 
                                textvariable=search_var, fg_color="#292929", font=("Arial", 15))
        search_entry.pack(pady=10, padx=10, anchor="center")

        def on_focus_in(event):
            if search_entry.get() == placeholder_text:
                search_entry.delete(0, "end")
                search_entry.configure(text_color="white")

        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, placeholder_text)
                search_entry.configure(text_color="gray")

        search_entry.insert(0, placeholder_text)
        search_entry.configure(text_color="gray")
        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)

        def update_display(*args):
            """Filtre l'affichage des boutons en fonction du texte entré dans la barre de recherche."""
            search_text = search_var.get().lower()

            # Supprime tous les boutons existants
            for btn in elements_in_root2:
                btn.pack_forget()

            element_positions.clear()
            visible_index = 0  # Indice des éléments visibles pour recalculer correctement y
            for i, element in enumerate(database_python):
                text = f"{element[0][1]} - {element[0][16]} - {element[0][17]} - {element[0][18]}"

                if search_text in text.lower() or search_text == placeholder_text.lower():
                    tabel_filled = CTkButton(first, width=300, command=lambda i=i: refound(i),
                                             height=40, corner_radius=12.5, text=text,
                                             bg_color="#292929", fg_color="#292929",
                                             font=("Arial", 15), hover=False,
                                             border_color='white', border_width=3)
                    tabel_filled.pack(pady=10, padx=10, anchor="center")
                    elements_in_root2.append(tabel_filled)

                    element_positions[i] = visible_index  # Stocke la position visible correcte
                    visible_index += 1
            for element in choix_apply_only : 
                try :
                    element.destroy()
                except : 
                    pass
        search_var.trace_add("write", update_display)
        update_display()  # Affichage initial
def refonte(x):
    global entrys, database_python, index_actuelle, enregistrer_button
    x = int(x)
    clear(1)
    dernier_elements = entrys[-8:] + entrys[:7]  
    mise_a_jour_index(1)

    # 🔴 EXTRACTION DU TUPLE DIRECTEMENT
    ligne = database_python[x][0]  # Suppression de la liste intermédiaire
    for i, j in zip(range(1, len(ligne) - 2), range(len(dernier_elements))):  
        try:
            if ligne[i] != "":  
                try:
                    try : 
                        dernier_elements[j].insert(0, int(ligne[i]))
                    except : 
                        dernier_elements[j].insert(0, ligne[i])
                except:
                    dernier_elements[j].insert(1.0, ligne[i])
        except AttributeError:
            try:
                if ligne[i] != "":
                    dernier_elements[j].set(ligne[i])
            except AttributeError:
                if ligne[i] != "":
                    dernier_elements[j].configure(text=ligne[i])

    index_actuelle.configure(text=ligne[0])
    enregistrer_button.configure(text="Nouveau")
    frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
    frame_flot.place(x=225, y=10)

    label = CTkLabel(frame_flot, text="Page actualisée avec succès", text_color="green",
                          width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                          font=("Verdana", 14))
    label.pack(padx=10, pady=(5, 2))
    # Barre de progression dans le frame

    progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                      width=200, height=5)
    progress_bar.pack(padx=10, pady=(0, 5))
    progress_bar.set(1.0)  # Définition de la valeur initiale
    # Assurer que le frame reste au-dessus
    frame_flot.lift()
    # Lancer la diminution après 1 seconde
    diminuer_progression(progress_bar, label, frame_flot)
def trynavalidate(event=None):
    global information, mot_de_passe1, identifiant1, identifiant_de_connexion, mot_de_passe_de_connexion, try_validate1

    if mot_de_passe1.get() == mot_de_passe_de_connexion and identifiant1.get() == identifiant_de_connexion:
        try_validate1.configure(hover=False, border_color='green', text="Validé!") 
        root.after(600, lambda: try_validate1.configure(fg_color="#202020")) 
        try_validate1.configure(command=validatevalidated)
        root.bind("<Return>",validatevalidated)

        information.configure(text="Entrez les nouveaux identifiants")
        information.place(x = 320)



        # 🔹 **Mise à jour des champs avec une pause forcée**
        def update_fields():
            mot_de_passe1.delete(0, "end")
            identifiant1.delete(0, "end")
            root.update_idletasks()  # 🔴 Force la mise à jour graphique immédiatement
            
            mot_de_passe1.configure(placeholder_text="Nouveau Mot de passe")
            identifiant1.configure(placeholder_text="Nouvel Identifiant")
            try_validate1.configure(hover=True, border_color='orange', text="Valider")
            root.focus()
        root.after(800, update_fields)

    elif mot_de_passe1.get() == "" and identifiant1.get() == "":
        mot_de_passe1.delete(0, "end")
        identifiant1.delete(0, "end")
        mot_de_passe1.configure(placeholder_text="*requis", placeholder_text_color="red")
        identifiant1.configure(placeholder_text="*requis", placeholder_text_color="red")
        root.after(500, lambda: identifiant1.configure(placeholder_text_color="grey"))  
        root.after(500, lambda: mot_de_passe1.configure(placeholder_text_color="grey"))  
        mot_de_passe1.configure(show="•")  
        root.focus()
    else:
        mot_de_passe1.delete(0, "end")
        identifiant1.delete(0, "end")
        mot_de_passe1.configure(placeholder_text="*incorrect", placeholder_text_color="red")
        identifiant1.configure(placeholder_text="*incorrect", placeholder_text_color="red")
        root.after(500, lambda: identifiant1.configure(placeholder_text_color="grey"))  
        root.after(500, lambda: mot_de_passe1.configure(placeholder_text_color="grey"))  
        mot_de_passe1.configure(show="•")  
        root.focus()
    root.focus()
def validatevalidated(event =None):
    global information, mot_de_passe1, identifiant1, identifiant_de_connexion, mot_de_passe_de_connexion, try_validate1

    # Vérifier si les champs sont vides
    if mot_de_passe1.get() == "" or identifiant1.get() == "":
        mot_de_passe1.delete(0, "end")
        identifiant1.delete(0, "end")
        mot_de_passe1.configure(placeholder_text="*requis", placeholder_text_color="red") 
        identifiant1.configure(placeholder_text="*requis", placeholder_text_color="red") 
        root.after(500, lambda: identifiant1.configure(placeholder_text_color="grey")) 
        root.after(500, lambda: mot_de_passe1.configure(placeholder_text_color="grey"))  
        mot_de_passe1.configure(show="•") 
        return  

    # Mettre à jour la base de données
    gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "identifiant", identifiant_de_connexion, 2, str(identifiant1.get()))
    gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA2", "motdepasse", mot_de_passe_de_connexion, 2, str(mot_de_passe1.get()))

    # Mettre à jour l'affichage et les variables globales
    information.configure(text="Nouveaux identifiants enregistrés")
    try_validate1.configure(hover=False, border_color='green', text="Validé!") 
    root.after(1500, lambda: try_validate1.configure(fg_color="#202020")) 

    mot_de_passe_de_connexion = mot_de_passe1.get()
    identifiant_de_connexion = identifiant1.get()

    root.after(2000, lambda: intermediaire(4))  # Rediriger après 2 secondes

    # Affichage d'une confirmation flottante
    frame_flot = CTkFrame(root, fg_color="#202020", bg_color="#202020", corner_radius=10)
    frame_flot.place(x=225, y=10)

    label = CTkLabel(frame_flot, text="Identifiants enregistrés", text_color="white",
                     width=200, height=18, fg_color="#292929", corner_radius=10, bg_color="#202020",
                     font=("Verdana", 14))
    label.pack(padx=10, pady=(5, 2))

    # Barre de progression
    progress_bar = CTkProgressBar(frame_flot, progress_color="green", width=200, height=5)
    progress_bar.pack(padx=10, pady=(0, 5))
    progress_bar.set(1.0)  

    frame_flot.lift()
    diminuer_progression(progress_bar, label, frame_flot)
def imprimation(x = 0,y = 0,z = 0):
    global index_actuelle,entrys
    if x == 1 : 
        system_name = platform.system()

        try:
            # Vérifie si le fichier existe
            if not os.path.isfile(getressources("CONDITIONS-GENERALES-DE-VENTE-PHONE-ADDICT.pdf")):
                raise FileNotFoundError(f"Fichier introuvable : {getressources("CONDITIONS-GENERALES-DE-VENTE-PHONE-ADDICT.pdf")}")
            
            if system_name == "Windows":
                win32api.ShellExecute(0, "print", getressources("CONDITIONS-GENERALES-DE-VENTE-PHONE-ADDICT.pdf"), None, ".", 0)
                print("Le fichier PDF a ete envoye au gestionnaire d'impression sous Windows.")

            elif system_name == "Darwin":  # macOS
                subprocess.run(["open", "-a", "Preview", getressources("CONDITIONS-GENERALES-DE-VENTE-PHONE-ADDICT.pdf")], check=True)
                frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
                frame_flot.place(x=225, y=10)

                label = CTkLabel(frame_flot, text="CGV imprimés", text_color="white",
                                  width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                                  font=("Verdana", 14))
                label.pack(padx=10, pady=(5, 2))
                # Barre de progression dans le frame

                progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                              width=200, height=5)
                progress_bar.pack(padx=10, pady=(0, 5))
                progress_bar.set(1.0)  # Définition de la valeur initiale
                # Assurer que le frame reste au-dessus
                frame_flot.lift()
                # Lancer la diminution après 1 seconde
                diminuer_progression(progress_bar, label, frame_flot)
                print("Le fichier PDF a ete envoye au gestionnaire d'impression sous macOS.")
            else:
                frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
                frame_flot.place(x=225, y=10)

                label = CTkLabel(frame_flot, text="erreur : Systeme d'exploitation", text_color="white",
                                  width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                                  font=("Verdana", 14))
                label.pack(padx=10, pady=(5, 2))
                # Barre de progression dans le frame

                progress_bar = CTkProgressBar(frame_flot, progress_color="red",
                                              width=200, height=5)
                progress_bar.pack(padx=10, pady=(0, 5))
                progress_bar.set(1.0)  # Définition de la valeur initiale
                # Assurer que le frame reste au-dessus
                frame_flot.lift()
                # Lancer la diminution après 1 seconde
                diminuer_progression(progress_bar, label, frame_flot)
                print("Système d'exploitation non pris en charge pour l'impression.")
        except Exception as e:
            frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
            frame_flot.place(x=225, y=10)

            label = CTkLabel(frame_flot, text="erreur : Imprimante non connectée", text_color="white",
                              width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                              font=("Verdana", 14))
            label.pack(padx=10, pady=(5, 2))
            # Barre de progression dans le frame

            progress_bar = CTkProgressBar(frame_flot, progress_color="red",
                                          width=260, height=5)
            progress_bar.pack(padx=10, pady=(0, 5))
            progress_bar.set(1.0)  # Définition de la valeur initiale
            # Assurer que le frame reste au-dessus
            frame_flot.lift()
            # Lancer la diminution après 1 seconde
            diminuer_progression(progress_bar, label, frame_flot)
            print(f"Erreur imprévue : {e}")
    else :
        system_name = platform.system()
        try:
            # Vérifie si le fichier existe
            if not os.path.isfile(getressources(f"PDFs\\{entrys[8].get()}-{entrys[9].get()}-{date_aujourdhui}.pdf")):
                raise FileNotFoundError(f" fichier inexistant: {getressources(f"PDFs\\{entrys[8].get()}-{entrys[9].get()}-{date_aujourdhui}.pdf")}")
            
            if system_name == "Windows":
                win32api.ShellExecute(0, "print", getressources(f"PDFs\\{entrys[8].get()}-{entrys[9].get()}-{date_aujourdhui}.pdf"), None, ".", 0)
                frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
                frame_flot.place(x=225, y=10)

                label = CTkLabel(frame_flot, text="Fichier imprimé", text_color="white",
                                  width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                                  font=("Verdana", 14))
                label.pack(padx=10, pady=(5, 2))
                # Barre de progression dans le frame

                progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                              width=200, height=5)
                progress_bar.pack(padx=10, pady=(0, 5))
                progress_bar.set(1.0)  # Définition de la valeur initiale
                # Assurer que le frame reste au-dessus
                frame_flot.lift()
                # Lancer la diminution après 1 seconde
                diminuer_progression(progress_bar, label, frame_flot)
                print("Le fichier PDF a été envoyé au gestionnaire d'impression sous Windows.")

            elif system_name == "Darwin":  # macOS
                subprocess.run(["open", "-a", "Preview", getressources(f"PDFs\\{entrys[8].get()}-{entrys[9].get()}-{date_aujourdhui}.pdf")], check=True)
                print("Le fichier PDF a été envoyé au gestionnaire d'impression sous macOS.")
            else:
                print("Système d'exploitation non pris en charge pour l'impression.")
                frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
                frame_flot.place(x=225, y=10)

                label = CTkLabel(frame_flot, text="erreur : Systeme d'exploitation", text_color="white",
                                  width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                                  font=("Verdana", 14))
                label.pack(padx=10, pady=(5, 2))
                # Barre de progression dans le frame

                progress_bar = CTkProgressBar(frame_flot, progress_color="red",
                                              width=200, height=5)
                progress_bar.pack(padx=10, pady=(0, 5))
                progress_bar.set(1.0)  # Définition de la valeur initiale
                # Assurer que le frame reste au-dessus
                frame_flot.lift()
                # Lancer la diminution après 1 seconde
                diminuer_progression(progress_bar, label, frame_flot)
        except Exception as e:
            print(f"Erreur imprévue : {e}")
            frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
            frame_flot.place(x=225, y=10)

            label = CTkLabel(frame_flot, text="Imprimante non connectée", text_color="white",
                              width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                              font=("Verdana", 14))
            label.pack(padx=10, pady=(5, 2))
            # Barre de progression dans le frame

            progress_bar = CTkProgressBar(frame_flot, progress_color="red",
                                          width=260, height=5)
            progress_bar.pack(padx=10, pady=(0, 5))
            progress_bar.set(1.0)  # Définition de la valeur initiale
            # Assurer que le frame reste au-dessus
            frame_flot.lift()
            # Lancer la diminution après 1 seconde
            diminuer_progression(progress_bar, label, frame_flot)
            
    hide_panel()
def boutons_root():
    global elements_in_root,label_hour_calendar,main_button,cal,marque_button,couleur_button,entrys,next_bouton,values_color,values_modele
    

    cache = CTkLabel(root,text ="",bg_color="#202020",fg_color="#202020",width = 360,height = 485,corner_radius=10)
    cache.place(x=316,y=90)
    
    Nom_image = CTkLabel(root, image = photo_name,text ="",bg_color="#202020",width = 60,height = 40,corner_radius=10)
    Nom_image.place(x=325,y=90)
    Nom_button = CTkEntry(root, placeholder_text="Nom",corner_radius=10,text_color="white",fg_color="#292929",width = 250,height = 40,placeholder_text_color='grey')
    Nom_button.place(x=385, y=90)
    Prénom_image = CTkLabel(root, image = photo_username,text ="",bg_color="#202020",width = 60,height = 40,corner_radius=10)
    Prénom_image.place(x=325,y=150)
    Prénom_button = CTkEntry(root, placeholder_text="Prénom",corner_radius=10,text_color="white",fg_color="#292929",width = 250,height = 40,placeholder_text_color='grey')
    Prénom_button.place(x=385, y=150)

    tel_image = CTkLabel(root, image = photo_phone,text ="",bg_color="#202020",width = 60,height = 40,corner_radius=10)
    tel_image.place(x=325,y=210)
    tel_button = CTkEntry(root, placeholder_text="Num. Télephone",corner_radius=10,text_color="white",fg_color="#292929",width = 250,height = 40,placeholder_text_color='grey')
    tel_button.configure(validate="key", validatecommand=(root.register(lambda v: v.isdigit() and len(v) <= 10 or v == ""), "%P"))

    tel_button.place(x=385, y=210)
    mail_image = CTkLabel(root, image = photo_mail,text ="",bg_color="#202020",width = 60,height = 40,corner_radius=10)
    mail_image.place(x=325,y=270)
    mail_button = CTkEntry(root, placeholder_text="E-Mail",corner_radius=10,text_color="white",fg_color="#292929",width = 250,height = 40,placeholder_text_color='grey')
    mail_button.place(x=385, y=270)
    elements_in_root.append(cache)
    
    elements_in_root.append(Nom_button)
    elements_in_root.append(Nom_image)
    elements_in_root.append(Prénom_button)
    elements_in_root.append(Prénom_image)
    elements_in_root.append(tel_button)
    elements_in_root.append(tel_image)
    elements_in_root.append(mail_button)
    elements_in_root.append(mail_image)
    


    marque_image = CTkLabel(root, image = photo_marque,text ="",bg_color="#202020",width = 60,height = 40,corner_radius=10)
    marque_image.place(x=325,y=330)
    marque_button = CTkOptionMenu(root,values = values_modele,corner_radius=10,text_color="white",fg_color="#292929",width = 250,height = 40,button_color='gray',button_hover_color="gray40")
    marque_button.place(x=385, y=330)
    

    modèle_image = CTkLabel(root, image = photo_modele,text ="",bg_color="#202020",width = 60,height = 40,corner_radius=10)
    modèle_image.place(x=325,y=390)
    modèle_button = CTkEntry(root,corner_radius=10,text_color="white",fg_color="#292929",width = 250,height = 40,placeholder_text="Modèle",placeholder_text_color='grey')
    modèle_button.place(x=385, y=390)

    couleur_image = CTkLabel(root, image = photo_couleur,text ="",bg_color="#202020",width = 60,height = 40,corner_radius=10)
    couleur_image.place(x=325,y=450)
    couleur_button = CTkOptionMenu(root,values =values_color,corner_radius=10,text_color="white",fg_color="#292929",width = 250,height = 40,button_color='gray',button_hover_color="gray40")
    couleur_button.place(x=385, y=450)
    

    imei_image = CTkLabel(root, image = photo_imei,text ="",bg_color="#202020",width = 60,height = 40,corner_radius=10)
    imei_image.place(x=325,y=510)
    imei_button = CTkEntry(root,corner_radius=10,text_color="white",fg_color="#292929",width = 250,height = 40,placeholder_text="Numéro IMEI",placeholder_text_color='grey')
    imei_button.place(x=385, y=510)
    imei_button.configure(validate="key", validatecommand=(root.register(lambda v: v.isdigit() and len(v) <= 17 or v == ""), "%P"))


    

    next_bouton = CTkButton(root, image = photo_next,text="",corner_radius=10,text_color="white",hover_color="grey40",fg_color="#202020",width = 80,height = 40,font = ("Arial",20),bg_color = "#202020",command = page2)
    next_bouton.place(x=585, y=615)
    petit_cache = CTkLabel(root,text ="",bg_color="#202020",fg_color="#202020",width = 80,height = 60,corner_radius=10)
    petit_cache.place(x=505,y=615)
    elements_in_root.append(marque_button)
    elements_in_root.append(marque_image)
    elements_in_root.append(modèle_button)
    elements_in_root.append(modèle_image)
    elements_in_root.append(couleur_button)
    elements_in_root.append(couleur_image)
    elements_in_root.append(imei_button)
    elements_in_root.append(imei_image)
    elements_in_root.append(next_bouton)
    elements_in_root.append(petit_cache)
    entrys.append(Nom_button)
    entrys.append(Prénom_button)
    entrys.append(tel_button)
    entrys.append(mail_button)
    entrys.append(marque_button)
    entrys.append(modèle_button)
    entrys.append(couleur_button)
    entrys.append(imei_button)
def update_total():
    try:
        total = (
            float(reparation20_button.get() or 0) +  
            float(reparation0_button.get() or 0) +  
            float(reparation10_button.get() or 0)
        )
    except ValueError:
        print("Erreur : Vérifie que toutes les entrées contiennent des nombres valides.")

    total_button.configure(text=total)
def boutons_root2():
    global elements_in_root1,timeliste,entrys,back_bouton,total_button,reparation0_button,reparation10_button,reparation20_button,values_reparations_possibles
    cache = CTkLabel(root,text ="",bg_color="#202020",fg_color="#202020",width = 360,height = 485,corner_radius=10)
    cache.place(x=316,y=90)
    
    reparation_image = CTkLabel(root, image = photo_reparation,text ="",bg_color="#202020",width = 60,height = 40,corner_radius=10)
    reparation_image.place(x=300,y=100)
    reparation_button = CTkComboBox(root,corner_radius=10,values=values_reparations_possibles,text_color="white",fg_color="#292929",width = 200,height = 40)
    reparation_button.place(x=365, y=100)
    reparation0_button = CTkEntry(root,corner_radius=10,placeholder_text="Prix €",text_color="white",fg_color="#292929",width = 80,height = 40)
    reparation0_button.configure(validate="key", validatecommand=(root.register(lambda v: v.isdigit() and len(v) <= 3 or v == ""), "%P"))
    reparation0_button.place(x=585, y=100)

    reparation1_image = CTkLabel(root, image = photo_reparation,text ="",bg_color="#202020",width = 60,height = 40,corner_radius=10)
    reparation1_image.place(x=300,y=150)
    reparation1_button = CTkComboBox(root,corner_radius=10,values=values_reparations_possibles,text_color="white",fg_color="#292929",width = 200,height = 40)
    reparation1_button.place(x=365, y=150)
    reparation10_button = CTkEntry(root,corner_radius=10,placeholder_text="Prix €",text_color="white",fg_color="#292929",width = 80,height = 40)
    reparation10_button.configure(validate="key", validatecommand=(root.register(lambda v: v.isdigit() and len(v) <= 3 or v == ""), "%P"))
    reparation10_button.place(x=585, y=150)

    reparation2_image = CTkLabel(root, image = photo_reparation,text ="",bg_color="#202020",width = 60,height = 40,corner_radius=10)
    reparation2_image.place(x=300,y=200)
    reparation2_button = CTkComboBox(root,corner_radius=10,values=values_reparations_possibles,text_color="white",fg_color="#292929",width = 200,height = 40)
    reparation2_button.place(x=365, y=200)
    reparation20_button = CTkEntry(root,corner_radius=10,placeholder_text="Prix €",text_color="white",fg_color="#292929",width = 80,height = 40)
    reparation20_button.configure(validate="key", validatecommand=(root.register(lambda v: v.isdigit() and len(v) <= 3 or v == ""), "%P"))
    reparation20_button.place(x=585, y=200)

    reparation_button.set(" ")
    reparation1_button.set(" ")
    reparation2_button.set(" ")
    back_bouton = CTkButton(root, image = photo_back,text="",corner_radius=10,text_color="white",hover_color="grey40",fg_color="#202020",width = 80,height = 40,font = ("Arial",20),bg_color = "#202020",command = page1)
    back_bouton.place(x=505, y=615)
    elements_in_root1.append(cache)
    
    elements_in_root1.append(back_bouton)
    elements_in_root1.append(reparation_image)
    elements_in_root1.append(reparation_button)
    elements_in_root1.append(reparation0_button)
    elements_in_root1.append(reparation1_image)
    elements_in_root1.append(reparation1_button)
    elements_in_root1.append(reparation10_button)
    elements_in_root1.append(reparation2_image)
    elements_in_root1.append(reparation2_button)
    elements_in_root1.append(reparation20_button)
    

    textbox_image = CTkLabel(root, image = photo_commentaire,text ="",bg_color="#202020",width = 60,height = 40,corner_radius=10)
    textbox_image.place(x=300,y=300)
    textbox_button = CTkTextbox(root,corner_radius=10,text_color="white",fg_color="#292929",width = 300,height = 200,border_color="grey",border_width=2)
    textbox_button.place(x=365, y=300)

    total_image = CTkLabel(root, image = photo_total,text ="",bg_color="#202020",width = 60,height = 40,corner_radius=10)
    total_image.place(x=390,y=530)
    total_button = CTkLabel(root,text = "0.0",corner_radius=10,text_color="white",fg_color="#292929",bg_color="#202020",width = 120,height = 50,font=("arial",20))
    total_button.place(x=455, y=525)
    root.bind("<KeyRelease>", lambda event: update_total()) 

    

    euro_label = CTkLabel(root,text = "€",corner_radius=10,text_color="white",fg_color="#202020",bg_color="#202020",width = 120,height = 50,font=("arial",20))
    euro_label.place(x=575, y=525)
    petit_cache = CTkLabel(root,text ="",bg_color="#202020",fg_color="#202020",width = 80,height = 60,corner_radius=10)
    petit_cache.place(x=585,y=615)


    elements_in_root1.append(textbox_button)
    elements_in_root1.append(textbox_image)
    elements_in_root1.append(total_button)
    elements_in_root1.append(total_image)
    elements_in_root1.append(euro_label)
    elements_in_root1.append(petit_cache)
    entrys.append(reparation_button)
    entrys.append(reparation0_button)
    entrys.append(reparation1_button)
    entrys.append(reparation10_button)
    entrys.append(reparation2_button)
    entrys.append(reparation20_button)
    entrys.append(textbox_button)
    entrys.append(total_button)
def page2():
    global elements_in_root1,récupérationpage1,page_actuelle
    for elements in elements_in_root1 : 
        elements.lift()
    page_actuelle = 2
def page1():
    global elements_in_root,récupérationpage2,page_actuelle
    try :
        root.bind("<Escape>",on_tab)
        root.bind("<Alt_L>",on_space)
        root.bind("<Control-s>", database_link_1)
        root.bind("<Control-n>", clear)
        root.bind("<Control-i>", print_to_pdf)

    
    except : 
        pass
    for elements in elements_in_root :
        elements.lift()
    page_actuelle = 1
def intermediaire(x,y=None):
    global page_actuelle,main_button,elements_in_root2,choix_apply_only,trash_admin,values_modele,values_modele
    compteuroptionmenu = 0
    
    if x == 1 : 
        if page_actuelle == 2 : 
            page1()
            clear()
            hide_panel()
        else : 
            clear()
            hide_panel()
    elif x == 2 : 
        elements_in_root2[5].place_forget()
        for element in elements_in_root2 :
            element.destroy()
        elements_in_root2.clear()
        page1()
        hide_panel()
        choix_apply_only.clear()

    elif x == 3 : 
        intermediaire(2)
        refonte(y)
        hide_panel()
    elif x == 4 : 
        try : 
            root.unbind("<Return>")
        except : 
            pass
        try :
            trash_admin[0].place_forget()
        except : 
            pass
        intermediaire(5)
        try :
            elements_in_root2[5].place_forget()
            for element in elements_in_root2 :
                element.destroy()
        except :
            pass
        elements_in_root2.clear()

        page1()
        for element in elements_in_root1 :
            if isinstance(element, CTkComboBox):
                element.configure(values = values_reparations_possibles)
                element.set(" ")

        for element in elements_in_root : 
            if isinstance(element, CTkOptionMenu):
                if compteuroptionmenu == 0 :
                    element.configure(values = values_modele)
                    element.set(values_modele[0])
                    compteuroptionmenu +=1
                else : 
                    element.configure(values = values_color)
                    element.set(values_color[0])
        hide_panel()
        
    elif x == 5:
        for element in elements_in_root3 :
            element.destroy()
        elements_in_root3.clear()
def clear(x = None,event = None):
    global elements_in_root, elements_in_root1,total_button,index_actuelle,database_python,values_reparations_possibles,values_modele,values_color
    compteur_entries = 1
    compteuroptionmenu = 0
    for element in elements_in_root:
        if isinstance(element, CTkEntry):
            element.delete(0, "end")  # Efface tout le texte actuel
            
            # Ajouter un placeholder en fonction du compteur
            placeholders = [
                "Nom", "Prénom", "Num. Téléphone", "E-Mail", 
                "Modèle", "Numéro IMEI"
            ]
            
            if compteur_entries <= len(placeholders):
                element.delete(0,"end")
                if compteur_entries == 3 :
                    element.configure(validate="none")
                    element.configure(placeholder_text = placeholders[compteur_entries - 1])
                    compteur_entries += 1
                    element.configure(validate="key", validatecommand=(root.register(lambda v: v.isdigit() and len(v) <= 10 or v == ""), "%P"))
                else : 
                    element.configure(placeholder_text = placeholders[compteur_entries - 1])
                    compteur_entries += 1
        if isinstance(element,CTkOptionMenu) : 
            if compteuroptionmenu == 0 :
                element.configure(values = values_modele)
                element.set(values_modele[0])
                compteuroptionmenu +=1
            else : 
                element.configure(values = values_color)
                element.set(values_color[0])

        else : 
            pass
    for element in elements_in_root1:
        if isinstance(element, CTkEntry):
            element.delete(0, "end")
            element.configure(validate="none")
            element.configure(placeholder_text="Prix €", placeholder_text_color="grey")
            element.configure(validate="key", validatecommand=(root.register(lambda v: v.isdigit() and len(v) <= 3 or v == ""), "%P"))  

        elif isinstance(element, CTkComboBox):
            element.configure(values = values_reparations_possibles)
            element.set(" ")
        else:
            try : 
                element.delete(1.0,"end")
            except :
                pass
    mise_a_jour_index()
    root.focus()
    if x == 1 : 
        return
    frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
    frame_flot.place(x=225, y=10)
    label = CTkLabel(frame_flot, text="Page vidée", text_color="white",
                      width=200, height=
                      30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                      font=("Verdana", 14))
    label.pack(padx=10, pady=(5, 2))
    # Barre de progression dans le frame
    progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                  width=200, height=5)
    progress_bar.pack(padx=10, pady=(0, 5))
    progress_bar.set(1.0)  # Définition de la valeur initiale
    # Assurer que le frame reste au-dessus
    frame_flot.lift()
    # Lancer la diminution après 1 seconde
    diminuer_progression(progress_bar, label, frame_flot)
def refound(x):
    global first, page_actuelle, elements_in_root2, choix_apply_only

    if x not in element_positions:
        print(f"⚠️ x={x} n'existe pas dans element_positions")  # Debugging
        return  # Empêche les erreurs si l'élément n'est pas visible

    y_position = 88 + (element_positions[x] * 60)  # Ajustement du placement vertical (+12px)

    if not choix_apply_only:
        print(f"Ajout du bouton 'Appliquer' pour x={x} à y={y_position}")  # Debugging
        choix = CTkButton(first, width=90, height=10, text="Appliquer",
                          bg_color="#292929", fg_color="orange",
                          text_color="black", font=("Arial", 15),
                          corner_radius=90, hover_color='yellow',
                          command=lambda: intermediaire(3, x))
        choix.place(x=12, y=y_position)
        

        elements_in_root2.append(choix)
        choix_apply_only = [choix, x]


    elif choix_apply_only[1] == x:
        print(f"Suppression du bouton 'Appliquer' pour x={x}")  # Debugging
        for i in choix_apply_only:
            try:
                i.destroy()
            except:
                pass
        choix_apply_only.clear()

    else:
        print(f"Suppression et recréation du bouton pour x={x}")  # Debugging
        for i in choix_apply_only:
            try:
                i.destroy()
            except:
                pass
        choix_apply_only.clear()

        choix = CTkButton(first, width=90, height=10, text="Appliquer",
                          bg_color="#292929", fg_color="orange",
                          text_color="black", font=("Arial", 15),
                          corner_radius=90, hover_color='yellow',
                          command=lambda: intermediaire(3, x))
        choix.place(x=12, y=y_position)
        elements_in_root2.append(choix)
        choix_apply_only = [choix, x]
def delete_pages():
    global elements_in_root,elements_in_root1
    for element in elements_in_root : 
        try : 
            element.destroy()
        except : 
            element.forget()
    for element in elements_in_root1 : 
        try : 
            element.destroy()
        except : 
            element.forget()
    elements_in_root.clear()
    elements_in_root1.clear()
def database_link_1(event = None):
    global database_python, elements_in_root, elements_in_root1, index_actuelle
    global label_date_calendar, label_hour_calendar, total_button, enregistrer_button, entrys

    if enregistrer_button.cget("text") != "Enregistrer":

        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)

        label = CTkLabel(frame_flot, text="Page vidée.", text_color="white",
                          width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                          font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame

        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                      width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)

        enregistrer_button.configure(text="Enregistrer")
        mise_a_jour_index(1)
        root.focus()
        clear(1)
        hide_panel()
        return

    database_temporaire_locale = []
    database_temporaire_locale1 = []

    # Récupérer les données des entrées et menus
    for entrée in elements_in_root + elements_in_root1:
        if isinstance(entrée, (CTkEntry, CTkOptionMenu, CTkComboBox)):
            database_temporaire_locale.append(entrée.get())
        elif isinstance(entrée, CTkTextbox):
            database_temporaire_locale.append(entrée.get("0.0", "end").strip())

    # Ajouter les infos supplémentaires
    database_temporaire_locale.extend([
        total_button.cget("text"),
        label_hour_calendar.cget("text"),
        label_date_calendar.cget("text")
    ])

    colonnes = [
        "name", "username", "phonenumber", "email", "marque", "model", "color",
        "imei", "reparation1", "prix1", "reparation2", "prix2", "reparation3", "prix3",
        "commentaire", "total", "date", "heure"
    ]

    # Vérifier si le nom existe déjà
    for element in database_python:
        if element[0][1] == database_temporaire_locale[0]:  
            afficher_message("Nom déjà existant!", "orange")
            mise_a_jour_index(1)
            root.focus()
            hide_panel()
            return

    # Vérifier si le champ name est vide
    if database_temporaire_locale[0] == "":
        afficher_message("Nom Vide !", "orange")
        hide_panel( )
        return

    # Convertir les données en une liste de tuples (format SQL correct)
    database_temporaire_locale1.append(tuple(database_temporaire_locale))

    if isinstance(database_temporaire_locale1[0], tuple):
        valeurs_a_inserer = list(database_temporaire_locale1[0])
    else:
        valeurs_a_inserer = database_temporaire_locale1

    # Insérer dans la base de données
    gestion_bdd(getressources("Database\DatabaseLink2.db"), "DATA", colonnes, None, 6, valeurs_a_inserer)

    # Ajouter dans la base locale
    database_python.append(tuple(database_temporaire_locale))

    afficher_message("Enregistré avec succès", "green")

    database_temporaire_locale.clear()
    database_temporaire_locale1.clear()
    mise_a_jour_index(1)
    root.after(2500,clear)
    
    root.focus()
    hide_panel()
def afficher_message(texte, couleur):
    """ Affiche un message temporaire avec un label et une progress bar """
    frame_flot = CTkFrame(root, fg_color="#202020", bg_color="#202020", corner_radius=10)
    frame_flot.place(x=245, y=10)

    label = CTkLabel(frame_flot, text=texte, text_color="white",
                     width=200, height=30, fg_color="#292929", corner_radius=10, bg_color="#202020",
                     font=("Verdana", 15))
    label.pack(padx=10, pady=(5, 2))

    progress_bar = CTkProgressBar(frame_flot, progress_color=couleur,
                                  width=200, height=5)
    progress_bar.pack(padx=10, pady=(0, 5))
    progress_bar.set(1.0)

    # Assurer que la frame reste toujours au-dessus
    frame_flot.lift()
    frame_flot.after(100, lambda: frame_flot.lift())

    # Lancer la diminution après 1 seconde
    diminuer_progression(progress_bar, label, frame_flot)
def split_text(text, max_chars_per_line):
    lines = text.split("\n")  # Séparer le texte en lignes
    formatted_lines = []
    
    for line in lines:
        # Découper chaque ligne en segments de max_chars_per_line
        formatted_lines.extend([line[i:i + max_chars_per_line] for i in range(0, len(line), max_chars_per_line)])

    return formatted_lines  # Retourne une liste de lignes bien formatées
def open_file_manager():
    system_name = platform.system()
    file_path = getressources("PDFs")
    
    if system_name == "Windows":
        os.system(f'start {file_path}')
        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)

        label = CTkLabel(frame_flot, text="PDFs ouverts", text_color="white",
                          width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                          font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame

        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                      width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)  # Utilise 'start' pour Windows
        print("Fichier ouvert sous Windows.")
    elif system_name == "Darwin":  # macOS
        os.system(f'open {file_path}')  # Utilise 'open' pour macOS
        print("Fichier ouvert sous macOS.")
    else:
        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)

        label = CTkLabel(frame_flot, text="erreur : Système d'exploitation ", text_color="white",
                          width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                          font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame

        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                      width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)
        print("Ce système d'exploitation n'est pas pris en charge pour l'ouverture du fichier.")
    hide_panel()
def print_to_pdf(xx = 0):
    global date_aujourdhui, entrys
    # Définition des fichiers de référence et de sortie
    reference_file = getressources("PDFs\\FILENODELETE.pdf")
    output_file = getressources(f"{entrys[8].get()}-{entrys[9].get()}-{date_aujourdhui}.pdf")

    # Création d'un PDF temporaire en mémoire
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.setFont("Helvetica", 15)
    










    # Nouvelle distribution des coordonnées
    positions_premiers = [593+27, 563+19, 533+9, 503+2, 473-3, 443-10, 413-17, 383-25]
    positions_derniers = [348-45, 348-45, 298-25,298-25 , 238, 238, 280, 150]
    y_positions = positions_derniers + positions_premiers  # Échange des coordonnées
    max_chars_per_line = 70

    verif = 0
    for i, entry in enumerate(entrys):
        y_position = y_positions[i]

        if isinstance(entry, CTkTextbox):
            text = entry.get("1.0", "end").strip()
            lines = split_text(text, max_chars_per_line)
            for line in lines:
                c.drawString(45, y_position-107, line)
                y_position -= 15
                if y_position <= 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = 800

        elif isinstance(entry, CTkLabel):
            text = entry.cget("text")
            c.drawString(270, y_position-120, str(text))
            c.drawString(345, y_position-120, '€')

        elif isinstance(entry, (CTkEntry, CTkOptionMenu, CTkComboBox)):
            text = entry.get()

            y_position = y_positions[i]  # Récupère la position y pour chaque entrée
            text = entry.get()  # Récupère le texte de l'entrée

            # Si i est inférieur à 6, place à la position x=110
            if i > 5:
                x = 210
                c.drawString(x, y_position, text)
            else:
                # Initialisation de la position x par défaut
                x = 50  # Position par défaut pour les entrées après le premier groupe

                # Si la position y actuelle est la même que la précédente, on avance la position x
                if y_position == verif:
                    x = 510  # Déplacer x à 450 si la position y est la même que la précédente

                # Afficher le texte à la position (x, y_position)
                c.drawString(x, y_position, text)
                c.drawString(582, y_position, '€')
                # Réinitialiser la position x à sa valeur de départ après l'affichage
                if y_position == verif:
                    x = 110  # Revenir à la position de base après affichage

            # Mettre à jour verif avec la valeur de la position y actuelle
            verif = y_position

    c.drawString(10, 775, str(date_aujourdhui))
    c.drawString(525, 775, str(label_hour_calendar.cget("text")))

























    c.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)


























    original_pdf = PdfReader(reference_file)
    output = PdfWriter()
    for page in original_pdf.pages:
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)




























    # Vérifier si le fichier existe et le supprimer
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"Ancien fichier {output_file} supprimé.")























    # Sauvegarde du PDF final
    with open(output_file, "wb") as output_stream:
        output.write(output_stream)













    print(f"PDF généré et sauvegardé sous : {output_file}")




















    # Déplacement du fichier généré
    destination_folder = getressources("PDFs")
    new_location = os.path.join(destination_folder, os.path.basename(output_file))
















    try:
        shutil.move(output_file, new_location)
        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)

        label = CTkLabel(frame_flot, text="Fichier créé et déplacé", text_color="white",
                          width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                          font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame

        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                      width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)
        print(f"Fichier déplacé vers {new_location}")
    except Exception as e:
        frame_flot = CTkFrame(root, fg_color="#202020",bg_color="#202020", corner_radius=10)
        frame_flot.place(x=225, y=10)

        label = CTkLabel(frame_flot, text="fichier Créé", text_color="white",
                          width=200, height=30, fg_color="#292929", corner_radius=10,bg_color="#202020",
                          font=("Verdana", 14))
        label.pack(padx=10, pady=(5, 2))
        # Barre de progression dans le frame

        progress_bar = CTkProgressBar(frame_flot, progress_color="green",
                                      width=200, height=5)
        progress_bar.pack(padx=10, pady=(0, 5))
        progress_bar.set(1.0)  # Définition de la valeur initiale
        # Assurer que le frame reste au-dessus
        frame_flot.lift()
        # Lancer la diminution après 1 seconde
        diminuer_progression(progress_bar, label, frame_flot)
        print(f"Erreur lors du déplacement du fichier : {e}")
        os.remove(output_file)  # Supprime le dernier fichier créé si le déplacement échoue
        print(f"Le fichier {output_file} a été supprimé suite à une erreur.")

    # Masquer le panneau si nécessaire
    mise_a_jour_index(1)

    hide_panel()
    print("voici xx",xx)
    if xx == 0 : 
        root.after(2500,imprimation)
    else :
        return

root = CTk()
root.geometry("700x700")
root.title("HomeX V.2.2")
root.resizable(False, False) 
root.iconbitmap(getressources("images\\cropped-logo-phoneaddict-1.ico"))


dark_color = "#202020"
dark_color2 = '#292929'
identifiant_de_connexion = ""
mot_de_passe_de_connexion = ""

#listes
timeliste = []
elements_in_root = []
elements_in_root1 = []
elements_in_root2 = []
elements_in_root3 = []
récupérationpage1 = ['','','','','','','','',]
récupérationpage2 = ['','','','','','','',]
database_python = []
entrys = []
choix_apply_only = []
choix_interaction_only = []
values_color = []
values_modele = []
values_reparations_possibles = []
etat = 0
etat_modifier_list = []




#values
page_actuelle = 1
background = CTkLabel(root,width = 1000,height = 1000,fg_color = "#202020",text = "")
background.place(x = 0,y = 0)
panel_width = 225
panel = CTkFrame(root, width=panel_width, height=600,bg_color="#202020",corner_radius=10,fg_color = '#292929')
panel.place(x=-panel_width, y=5)
photo_1 = CTkImage(Image.open(getressources("images/menu_image.png")), size=(30, 30))
photo_2 = CTkImage(Image.open(getressources("images/quit_image.png")), size=(25, 25))
photo_3 = CTkImage(Image.open(getressources("images/fermer_image.png")), size=(25, 25))
photo_41= CTkImage(Image.open(getressources("images/logo_image.png")), size=(300,250))
photo_3 = CTkImage(Image.open(getressources("images/fermer_image.png")), size=(25, 25))
photo_name = CTkImage(Image.open(getressources("images/user_image.png")), size=(25, 25))
photo_username = CTkImage(Image.open(getressources("images/user_image.png")), size=(25, 25))
photo_mail = CTkImage(Image.open(getressources("images/mail_image.png")), size=(28, 28))
photo_phone = CTkImage(Image.open(getressources("images/phone_image.png")), size=(25, 25))
photo_imei = CTkImage(Image.open(getressources("images/imei_image.png")), size=(25, 25))
photo_modele = CTkImage(Image.open(getressources("images/modele_image.png")), size=(25, 25))
photo_marque = CTkImage(Image.open(getressources("images/marque_image.png")), size=(25, 25))
photo_couleur = CTkImage(Image.open(getressources("images/color_image.png")), size=(25, 25))
photo_next = CTkImage(Image.open(getressources("images/arrow_image.png")), size=(50, 50))
photo_back = CTkImage(Image.open(getressources("images/back-arrow_image.png")), size=(50, 50))
photo_reparation = CTkImage(Image.open(getressources("images/reparation_image.png")), size=(25, 25))
photo_commentaire = CTkImage(Image.open(getressources("images/commentaire_image.png")), size=(25, 25))
photo_total= CTkImage(Image.open(getressources("images/total_image.png")), size=(40, 40))
photo_qr_code = CTkImage(Image.open(getressources("images/qr_code_image.png")), size=(140, 140))
photo_menu = CTkImage(Image.open(getressources("images/logo_image.png")), size=(170, 170))


photo_admin = CTkImage(Image.open(getressources("images/image_admin.png")), size=(25, 25))
photo_cgv = CTkImage(Image.open(getressources("images/image_cgv.png")), size=(25, 25))
photo_folder = CTkImage(Image.open(getressources("images/image_pdf.png")), size=(25, 25))
photo_save = CTkImage(Image.open(getressources("images/image_save.png")), size=(25, 25))
photo_clear = CTkImage(Image.open(getressources("images/image_clear.png")), size=(25, 25))
photo_print = CTkImage(Image.open(getressources("images/image_print.png")), size=(25, 25))
photo_history = CTkImage(Image.open(getressources("images/image_history.png")), size=(25, 25))
home_photo   = CTkImage(Image.open(getressources("images/home_image.png")), size=(30, 30))
photo_options  = CTkImage(Image.open(getressources("images/options_image.png")), size=(30, 30))





date_aujourdhui = date.today()
date_fr =list(str(date_aujourdhui).split("-"))
current_date_for_label = str(date_fr[2]) +" / " + str(date_fr[1]) + " / " + str(2000+int(date_fr[2]))

logo_entreprise = CTkLabel(root, text="",fg_color = "#202020",bg_color="#292929",image= photo_41,width = 250,height = 150)
logo_entreprise.place(y=0, x=0)
main_button = CTkButton(root, text="Menu",command=show_panel,corner_radius=4,text_color="white",hover_color="gray",fg_color="#292929",width = 165,height = 40,font = ("Arial",20))
main_button.place(x=60, y=610)
menu_image = CTkLabel(root, image = photo_1,text ="",bg_color="#292929",width = 60,height = 40)
menu_image.place(y=610, x=5)
leave_button = CTkButton(root, text="Quitter",command=root.destroy,corner_radius=4,text_color="white",hover_color="gray",fg_color="#292929",width = 165,height = 40,font = ("Arial",20))
leave_button.place(x=60, y=655)
leave_image = CTkLabel(root, image = photo_2,text ="",bg_color="#292929",width = 60,height = 40)
leave_image.place(y=655, x=5)
label_hour_calendar = CTkLabel(root, text="", width=100, height=35,fg_color = "#202020", bg_color="#202020", corner_radius=10, text_color="white",font = ("Arial",18))
label_hour_calendar.place(x=595, y=5)
label_date_calendar = CTkLabel(root,text=current_date_for_label, width=100, height=35,fg_color = "#202020", bg_color="#202020", corner_radius=10, text_color="white",font = ("Arial",18))
label_date_calendar.place(x = 455,y = 5)

qr_code_image = CTkLabel(root, text="",fg_color = "#202020",image= photo_qr_code,width = 175,height = 175)
qr_code_image.place(y=410, x=35)
version_label = CTkLabel(root, text="Version 2.2",bg_color = "#202020",fg_color = "#202020",width = 100,height = 25)
version_label.place( x=5,y=585)
timeliste.append(label_date_calendar)
timeliste.append(label_hour_calendar)
timeliste.append(current_date_for_label)
timeliste.append(leave_button)
timeliste.append(leave_image)
timeliste.append(main_button)
timeliste.append(menu_image)

cal = Calendar(
    root,
    selectmode="day",
    year=datetime.now().year,
    month=datetime.now().month,
    day=datetime.now().day,
    background="#1a1a1a",        # Fond principal très sombre
    foreground="#f0f0f0",        # Texte clair
    bordercolor="#3d3d3d",       # Bordure gris foncé
    headersbackground="#2b2b2b", # Fond des en-têtes (jours/semaine)
    headersforeground="#f0f0f0", # Texte des en-têtes en blanc/gris clair
    selectbackground="#3d3d3d",  # Fond de la date sélectionnée (gris foncé)
    selectforeground="#ffffff",  # Texte blanc pour la date sélectionnée
    normalbackground="#262626",  # Fond des jours normaux
    normalforeground="#f0f0f0",  # Texte des jours normaux
    weekendbackground="#2b2b2b", # Fond des week-ends
    weekendforeground="#e0e0e0", # Texte des week-ends en gris clair
    othermonthbackground="#1f1f1f",  # Jours hors mois courant
    othermonthforeground="#555555",  # Texte des jours hors mois courant
    disabledbackground="#2a2a2a",    # Fond des jours désactivés
    disabledforeground="#777777",    # Texte des jours désactivés
    borderwidth=2,
    date_pattern='dd/mm/yyyy',   
    locale='fr_FR'              
    )
cal.place(x=4,y=230)
today = datetime.today()
cal.calevent_create(today, 'Aujourd\'hui', 'today')
cal.tag_config('today', foreground="#ff0000",background = "#202020")
index_actuelle = CTkLabel(root, text="0",fg_color = "#202020",width = 50,height = 25)
index_actuelle.place(y=680, x=650)
index_actuelle_texte = CTkLabel(root, text="Index :",fg_color = "#202020",width = 50,height = 25)
index_actuelle_texte.place(y=680, x=610)
timeliste.append(index_actuelle)
timeliste.append(index_actuelle_texte)

mise_a_jour_index(1)
mise_a_jour_parameters()
boutons_root2()
boutons_root()
boutons_panel()
update_time()
background1 = CTkLabel(root,width = 700,height = 700,fg_color = "#202020",text = "")
background1.place(x = 0,y = 0)
background2 = CTkLabel(root,width = 300,height = 50,fg_color = "#292929",text = "Bienvenue",font =("verdana",30),bg_color="#202020",corner_radius=10)
background2.place(x = 210,y = 120)
background3 = CTkButton(root,width = 60,height = 60,corner_radius= 90 ,fg_color = "#292929",text = "Commencer",command = start,text_color = "white",bg_color = "#202020",border_color='orange',border_width=1,font =("verdana",15),hover_color= "orange")
background3.place(x = 280,y = 320)

print(database_python)

root.mainloop()
#13/03/2025/00h31 - 24/03/2025/1h19#