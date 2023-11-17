# Se connecter à la base de données "dialectes" et au serveur Flask
# Pouvoir voir tout le contenu de chaque table de la base de données: "texte", "transcription" et "classe". 
# Pouvoir voir tout le contenu de la base de données: texte, transcription et classe de toutes les entrée selon les relations notées
# dans la table de joincture.
# N.B.: variables "user_input" et "password" (lignes 15 et 16) sont à changer par les tiens, ici leurs valeurs sont des placeholders.

from flask import Flask, request
from flask import jsonify
import json
from mysql.connector import connect, Error


app = Flask(__name__, static_url_path='/static')

user_input = 'root'  # remplacer par votre login, par exemple, 'root'
password = 'root'  # remplacer par votre mot de passe, par exemple, 'root'
dbname = 'dialectes'


## Connexion à la base de données en même temps que l'on se connecte au serveur Flask:

try:
    # obtention d'une variable de connection de type MySQLConnection qui permettra l'intéraction avec le serveur Flask:
    connection = connect(
        host="localhost",   
        user = user_input,
        password = password,
        database=dbname
    )
    print(connection)
# afficher un message d'erreur de connection en cas de connexion non réussie:
except Error as e:
    print(e)


## Définition de la page de base pour la route, "/" (racine du chemin), et affichage d'un message sur la page web :

@app.route('/', methods=['GET'])
def home():
    """Affiche un message sur la page web route (racine du chemin)."""
    return '''<h1>Dialectes</h1>
<p>Une API pour associer des échantillons de parole à des dialectes 'français breton' et 'français standard'.</p>'''


## Fonction pour pouvoir voir tout le contenu de la base de données, toutes tables confondues selon
# les relations indiquées dans la table de joincture:

# Toutes les entrées de la base de données:
@app.route('/api/v1/dialectes/phrases/all', methods=['GET'])
def api_phrases_all():
    """Retourne le texte, transcription et classe dialectale de toutes les entrées de la base de données
    en récupérant les informations selon les relations indiquées dans la table de joincture."""

    # Requête pour sélectionner le texte, transcription et classe dialectale de toutes les entrées
    select_all_query = """
        SELECT texte.texte, transcription.transcription, classe.dialecte
        FROM textetransclasse LEFT JOIN texte ON textetransclasse.texteID=texte.texteID
        LEFT JOIN transcription ON textetransclasse.transcriptionID=transcription.transcriptionID
        LEFT JOIN classe ON textetransclasse.classeID=classe.classeID
        """
    # les résultats viendront dans une liste de dictionnaires (un par entrée), et lorsque cette liste est passée
    # au jsonify pour acquérir un format json, la sortie conserve les noms de colonnes de la base de données.
    
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(select_all_query)
        results = cursor.fetchall()
    return jsonify(results)



## Fonctions pour pouvoir voir tout le contenu d'une table:

# Toutes les entrées de la table "texte":
@app.route('/api/v1/dialectes/texte/all', methods=['GET'])
def api_texte_all():
    """Retourne le texte de toutes les entrées de la table 'texte' de la base de données."""

    # Requête pour sélectionner le texte de toutes les entrées:
    query = 'SELECT * FROM texte'
   
    # les résultats viendront dans une liste de dictionnaires (un par entrée), et lorsque cette liste est passée
    # au jsonify pour acquérir un format json, la sortie conserve les noms de colonnes de la base de données.
   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return jsonify(results)

# Toutes les entrées de la table "transcription":
@app.route('/api/v1/dialectes/transcription/all', methods=['GET'])
def api_transcription_all():
    """Retourne la transcription de toutes les entrées de la table 'texte' de la base de données."""

    # Requête pour sélectionner le transcription de toutes les entrées:
    query = 'SELECT * FROM transcription'
    # les résultats viendront dans une liste de dictionnaires (un par entrée), et lorsque cette liste est passée
    # au jsonify pour acquérir un format json, la sortie conserve les noms de colonnes de la base de données.
   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return jsonify(results)

# Toutes les entrées de la table "classe":
@app.route('/api/v1/dialectes/classe/all', methods=['GET'])
def api_classe_all():
    """Retourne la catégorie dialectale de toutes les entrées de la table 'dialecte' de la base de données."""

    # Requête pour sélectionner la classe dialectale de toutes les entrées:
    query = 'SELECT * FROM classe'
    # les résultats viendront dans une liste de dictionnaires (un par entrée), et lorsque cette liste est passée
    # au jsonify pour acquérir un format json, la sortie conserve les noms de colonnes de la base de données.
   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return jsonify(results)



## Fonctions pour pouvoir voir le contenu spécifique d'une table par l'identifiant des entrées:

# Entrées spécifiques de la table "texte":
@app.route('/api/v1/dialectes/texte', methods=['GET'])
def api_texte_id():
    """La fonction prend l'identifiant fourni par l'utilisateur dans l'URL de requête 
    pour récupérer le contenue textuel correspondant de l'entrée concernée. 
    Elle retourne une erreur si l'identifiant n'est pas fournie ou s'il
    est en dehors du rang de nombre d'entrées de la table.
    La requête commence par ? et a la forme '?texteID=x', où x est
    un entier correspondant à l'identifiant de l'entrée."""
    

    # Vérifier que l'identifiant de cette table a été donnée en argument de la requête dans l'URL:
    nom_table = "texte"
    label_identifiant = f"{nom_table}ID"
    if label_identifiant in request.args:
        id = int(request.args[label_identifiant])
    else:
        return f"Erreur: Argument {label_identifiant} absent. Fournissez un argument {label_identifiant} à l'URL."


    # Récuperer la totalité de la table dans une liste de dictionnaires où chaque dictionnaire correspond à une entrée:
    query = f'SELECT * FROM {nom_table}'
   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        table = cursor.fetchall()


    # Avertir l'utilisateur avec un message d'erreur si l'identifiant fourni n'est pas dans le rang allant de 1 à la taille maximale
    # (en nombre d'entrées) de la table:
    nb_entrees = len(table)

    if id not in list(range(1,nb_entrees+1)):
        return f"Erreur: Vous ne pouvez enquêter que les lignes dans le rang de 1 à {nb_entrees}, qui est la taille \
        maximale de la table. Fournissez un argument {label_identifiant} compris dans ce rang."


    # Étant donné une liste de dictionnaires ou chaque dictionnaire est une entrée de la table, la variable "entree"
    # gardera, du dictionnaire correspondant à l'entrée de la table sollicitée par l'utilisateur à travers de 
    # son identifiant, le string correspondant de la colonne textuelle de la table:

    # Parcourir la liste de dictionnaires mentionnée ci-dessus jusqu'à trouver celui contenant l'entrée sollicitée
    # par l'utilisateur à travers de son identifiant:
    for ligne in table:
        if ligne[label_identifiant] == id:
            entree = f'Entrée {id} : "{ligne[nom_table]}"'
            break

  
    # Afficher le contenu textuel correspondant à l'identifiant dans un string joli qui mentionne l'identifiant :
    return entree


# Entrées spécifiques de la table "transcription":
@app.route('/api/v1/dialectes/transcription', methods=['GET'])
def api_transcription_id():
    """La fonction prend l'identifiant fourni par l'utilisateur dans l'URL de requête 
    pour récupérer le contenue textuel correspondant de l'entrée concernée. 
    Elle retourne une erreur si l'identifiant n'est pas fournie ou s'il
    est en dehors du rang de nombre d'entrées de la table.
    La requête commence par ? et a la forme '?transcriptionID=x', où x est
    un entier correspondant à l'identifiant de l'entrée."""
    

    # Vérifier que l'identifiant de cette table a été donnée en argument de la requête dans l'URL:
    nom_table = "transcription"
    label_identifiant = f"{nom_table}ID"
    if label_identifiant in request.args:
        id = int(request.args[label_identifiant])
    else:
        return f"Erreur: Argument {label_identifiant} absent. Fournissez un argument {label_identifiant} à l'URL."


    # Récuperer la totalité de la table dans une liste de dictionnaires où chaque dictionnaire correspond à une entrée:
    query = f'SELECT * FROM {nom_table}'
   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        table = cursor.fetchall()


    # Avertir l'utilisateur avec un message d'erreur si l'identifiant fourni n'est pas dans le rang allant de 1 à la taille maximale
    # (en nombre d'entrées) de la table:
    nb_entrees = len(table)

    if id not in list(range(1,nb_entrees+1)):
        return f"Erreur: Vous ne pouvez enquêter que les lignes dans le rang de 1 à {nb_entrees}, qui est la taille \
        maximale de la table. Fournissez un argument {label_identifiant} compris dans ce rang."


    # Étant donné une liste de dictionnaires ou chaque dictionnaire est une entrée de la table, la variable "entree"
    # gardera, du dictionnaire correspondant à l'entrée de la table sollicitée par l'utilisateur à travers de 
    # son identifiant, le string correspondant de la colonne textuelle de la table:

    # Parcourir la liste de dictionnaires mentionnée ci-dessus jusqu'à trouver celui contenant l'entrée sollicitée
    # par l'utilisateur à travers de son identifiant:
    for ligne in table:
        if ligne[label_identifiant] == id:
            entree = f'Entrée {id} : "{ligne[nom_table]}"'
            break


    # Afficher le contenu textuel correspondant à l'identifiant dans un string joli qui mentionne l'identifiant :
    return entree


# Entrées spécifiques de la table "classe":
@app.route('/api/v1/dialectes/classe', methods=['GET'])
def api_classe_id():
    """La fonction prend l'identifiant fourni par l'utilisateur dans l'URL de requête 
    pour récupérer le contenue textuel correspondant de l'entrée concernée. 
    Elle retourne une erreur si l'identifiant n'est pas fournie.
    La requête commence par ? et a la forme '?classeID=x', où x est
    un entier correspondant à l'identifiant de l'entrée."""
    

    # Vérifier que l'identifiant de cette table a été donnée en argument de la requête dans l'URL:
    nom_table = "classe"
    label_identifiant = f"{nom_table}ID"
    if label_identifiant in request.args:
        id = int(request.args[label_identifiant])
    else:
        return f"Erreur: Argument {label_identifiant} absent. Fournissez un argument {label_identifiant} à l'URL."


    # Récuperer la totalité de la table dans une liste de dictionnaires où chaque dictionnaire correspond à une entrée:
    query = f'SELECT * FROM {nom_table}'
   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        table = cursor.fetchall()


    # Avertir l'utilisateur avec un message d'erreur si l'identifiant fourni n'est pas dans le rang allant de 1 à la taille maximale
    # (en nombre d'entrées) de la table:
    nb_entrees = len(table)

    if id not in list(range(1,nb_entrees+1)):
        return f"Erreur: Vous ne pouvez enquêter que les lignes dans le rang de 1 à {nb_entrees}, qui est la taille \
        maximale de la table. Fournissez un argument {label_identifiant} compris dans ce rang."


    # Étant donné une liste de dictionnaires ou chaque dictionnaire est une entrée de la table, la variable "entree"
    # gardera, du dictionnaire correspondant à l'entrée de la table sollicitée par l'utilisateur à travers de 
    # son identifiant, le string correspondant de la colonne textuelle de la table:

    # Parcourir la liste de dictionnaires mentionnée ci-dessus jusqu'à trouver celui contenant l'entrée sollicitée
    # par l'utilisateur à travers de son identifiant:
    for ligne in table:
        if ligne[label_identifiant] == id:
            entree = f'Entrée {id} : {ligne["dialecte"]}'
            break

    
    # Afficher le contenu textuel correspondant à l'identifiant dans un string joli qui mentionne l'identifiant :
    return entree



# Demander une phrase par son identifiant et recevoir le texte, la transcription et la classe (selon les 
# relations indiquées dans la table de joincture):

@app.route('/api/v1/dialectes/idphrase_classe', methods=['GET'])
def api_textetransclasse():
    """La fonction prend l'identifiant fourni par l'utilisateur dans l'URL de requête 
    pour récupérer le contenue textuel correspondant de l'entrée concernée,
    (texte, transcription et classe dialectale), à l'aide des identifiants notés comme 
    clé étrangère dans la table de joncture.
    Elle retourne une erreur si l'identifiant n'est pas fourni.
    La requête commence par ? et a la forme '?id=x', où x est
    un entier correspondant à l'identifiant de l'entrée."""

    # Avertir l'utilisateur du manque d'argument:

    label_identifiant = "id"
    if label_identifiant in request.args:
        id = int(request.args[label_identifiant])
    else:
        return f"Erreur: Argument {label_identifiant} absent. Fournissez un argument {label_identifiant} à l'URL."


    # Avertir l'utilisateur d'un argument hors range:
    # Récuperer la totalité de la table dans une liste de dictionnaires où chaque dictionnaire correspond à une entrée:
    query = 'SELECT * FROM textetransclasse'
   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        table = cursor.fetchall()

    # Avertir l'utilisateur avec un message d'erreur si l'identifiant fourni n'est pas dans le rang allant de 1 à la taille maximale
    # (en nombre d'entrées) de la table:
    nb_entrees = len(table)

    if id not in list(range(1,nb_entrees+1)):
        return f"Erreur: Vous ne pouvez enquêter que les lignes dans le rang de 1 à {nb_entrees}, qui est la taille \
        maximale de la table. Fournissez un argument {label_identifiant} compris dans ce rang."


    # Sélectionner texte, transcription et classe dans les tables respectives selon les relations notées dans la 
    # table de joincture pour l'entrée indiquée par l'utilisateur:
    select_id_query = f"""
        SELECT texte.texte, transcription.transcription, classe.dialecte
        FROM textetransclasse LEFT JOIN texte ON textetransclasse.texteID=texte.texteID
        LEFT JOIN transcription ON textetransclasse.transcriptionID=transcription.transcriptionID
        LEFT JOIN classe ON textetransclasse.classeID=classe.classeID WHERE textetransclasse.id={id}
        """

    with connection.cursor() as cursor:
        cursor.execute(select_id_query)
        entree = cursor.fetchall()
    

    # String de résultat avec texte, transcription et classe correspondante:
    resultat = f'Entrée {id} : "{entree[0][0]}" // {entree[0][1]} -> dialecte : {entree[0][2]}'
    
    # Afficher le contenu textuel correspondant à l'identifiant dans un string joli qui mentionne l'identifiant :
    return resultat



# Ajouter des données à la base de données (tables 'texte', 'transcription', joincture mises à jour par la même fonction):
# (Pour affichage uniquement. Le code d'insertion dans la base de données ne fonctionne pas, avec erreur
# de "Method Not Allowed" (exemple 1 pour l'insertion directement dans une seule table, 'texte', dans la 
# section "commentaires erreur", à la fin de ce document, pour référence)).
@app.route('/api/v1/dialectes/ajoute_phrase', methods=['POST'])
def ajoute_phrase():
    """Fonction pour ajouter une nouvelle entrée dans la base de données selon les relations
    notées dans la table de joincture. La nouvelle entrée est donnée sous la forme d'un dictionnaire
    dont les clés correspondent aux noms de colonnes de format string des tables ('texte','transcription',
    'dialecte') de la base de données."""

    # l'attribut data nous permet de récupérer les données postées
    phrase_dict = json.loads(request.data)
    texte = phrase_dict['texte']
    transcription = phrase_dict['transcription']
    nom_dialecte = phrase_dict['dialecte']

    
    # Récuperer la totalité de la table de joincture, la 'texte', la 'transcription' dans une liste (pour chacune) 
    # de dictionnaires où chaque dictionnaire correspond à une entrée:
    
    # joincture:
    query = 'SELECT * FROM textetransclasse'
   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        table_jonc = cursor.fetchall()
    
    # 'texte':
    query = 'SELECT * FROM texte'
   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        table_texte = cursor.fetchall()

    # 'transcription':
    query = 'SELECT * FROM transcription'
   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        table_trans = cursor.fetchall()

    # Calculer le nouvel identifiant comme le total d'entrées de la table de joincture + 1:
    nb_entrees = len(table_jonc)
    id = nb_entrees + 1

    # Découvrir l'identifiant qui correspond au dialecte dans la table 'classes':
    query = 'SELECT * FROM classe'
   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        table_classe = cursor.fetchall()

    for ligne in table_classe:
        if ligne['dialecte'] == nom_dialecte:
            classe_id = ligne["classeID"]
            break

    # Insertion de données dans chaque table (insertion dans multiples tables par l'intermédiaire de celle de joincture
    # n'est pas assurée par MySQL il me semble)

    # Table 'texte':
    # faire un dictionaire de la nouvelle entrée pour l'ajouter à la table 'texte':
    texte_dict = {}
    texte_dict['texteID'] = id
    texte_dict['texte'] = texte

    table_texte.append(texte_dict)


    # Table 'transcription':
    # faire un dictionaire de la nouvelle entrée pour l'ajouter à la table 'transcription':
    transcription_dict = {}
    transcription_dict['transcriptionID'] = id
    transcription_dict['transcription'] = transcription

    table_trans.append(transcription_dict)

    # Table 'textetransclasse':
    # faire un dictionaire de la nouvelle entrée pour l'ajouter à la table 'textetransclasse':
    jonc_dict = {}
    jonc_dict['id'] = id
    jonc_dict['texteID'] = id
    jonc_dict['transcriptionID'] = id
    jonc_dict['classeID'] = classe_id
    
    table_jonc.append(jonc_dict)


    # Afficher l'insertion de la nouvelle phrase dans les 3 tables ('texte', 'transcription', joincture):
    return {'table texte': table_texte, 'table transcription': table_trans, 'table de joincture': table_jonc}
    


# Fonction pour mettre à jour le dialecte d'une phrase identifiée par son id dans la table de joincture:
@app.route('/api/v1/dialectes/update_dialecte_phrase', methods=['PUT'])
def update_dialecte():
    """Fonction pour mettre à jour le dialecte d'une phrase identifiée par son id dans la table de joincture. 
    La nouvelle entrée est donnée sous la forme d'un dictionnaire dont les clés correspondent aux noms de colonnes 
    de format string des tables ('texte','transcription','dialecte') de la base de données. La clé 'id' du dictionnaire
    correspond à la colonne 'id' de la table de joincture."""

    # l'attribut data nous permet de récupérer les données postées
    updated_info_dict = json.loads(request.data)
    id = updated_info_dict['id']
    nom_dialecte = updated_info_dict['dialecte']


    # Découvrir l'identifiant qui correspond au dialecte dans la table 'classe':
    query = 'SELECT * FROM classe'
   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        table_classe = cursor.fetchall()

    for ligne in table_classe:
        if ligne['dialecte'] == nom_dialecte:
            #entree.append(f'Entrée {id} : "{ligne["dialecte"]}"')
            classe_id = ligne["classeID"]
            break
    
    
    # Mettre à jour la table de joincture:

    # Requête:
    update_classe_phrase_query = f"""
        UPDATE textetransclasse SET classeID={classe_id} WHERE id={id}
        """

    with connection.cursor() as cursor:
        cursor.execute(update_classe_phrase_query)
        connection.commit()
    

    # Ouvrir la version mise à jour de la table:
    query = 'SELECT * FROM textetransclasse'
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        table_jonc = cursor.fetchall()

    # Afficher la table de joincture mise à jour :
    return jsonify(table_jonc)


# Supprimer une entrée de la table de joincture:
@app.route('/api/v1/dialectes/delete_phrase_jonc', methods=['GET'])
def delete_phrase_jonc():
    """Fonction pour supprimer une entrée identifiée par son id de la table de joincture. 
    La nouvelle entrée est donnée sous la forme d'un dictionnaire dont la clé 'id' 
    correspond à la colonne 'id' de la table de joincture."""

    # Récupérer l'id informé par l'utilisateur dans l'URL:
    id = request.args.get('id')

    # Supprimer de la table de joincture une entrée identifiée par id :

    # Requête:
    delete_phrase_jonc_query = f"""
        DELETE FROM textetransclasse WHERE id={id}
        """

    with connection.cursor() as cursor:
        cursor.execute(delete_phrase_jonc_query)
        connection.commit()
    
    # Ouvrir la version mise à jour de la table:
    query = 'SELECT * FROM textetransclasse'
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        table_jonc = cursor.fetchall()

    # Retourner/afficher la table de joincture avec une entrée supprimée :
    return jsonify(table_jonc)




if __name__ == '__main__':
   
   app.secret_key = 'ddd'

   # debug = True - des éventuelles modifications du code sont intégrées par recharge de la page sans avoir à redémarrer le serveur
   app.run(debug = True)





#############################
#
# Commentaires erreur
#
#########################


# # Example 1 de code qui donne erreur pour insertion de données dans la base de données séparemment par table (ici la table 'texte'):
# # Erreur: <p class="errormsg">mysql.connector.errors.ProgrammingError: 1064 (42000): You have an error in your SQL syntax; 
# # check the manual that corresponds to your MySQL server version for the right syntax to use near &#39;tenu à apporter cet objet 
# # que j’aime beaucoup.)&#39; at line 1 </p>

# Erreur sur la page web: method not allowed

# # Appel via cellule du notebook 'DM-GenieLogiciel_Rodrigues_exercices1-2.ipynb', exemple table 'texte':
# import requests


# url = 'http://127.0.0.1:5000/api/v1/dialectes/ajoute_texte'

# maphrase = {'texte': 'J’ai tenu à apporter cet objet que j’aime beaucoup.'}

# x = requests.post(url, json = maphrase)

# print(x.text)

# Fonction dans explore_db.py:

# # Fonction pour insertion dans chaque table séparemment, ici table 'texte':
# @app.route('/api/v1/dialectes/ajoute_texte', methods=['POST'])
# def ajoute_texte():
#     """Fonction pour ajouter une nouvelle entrée dans la table 'texte' de base de données.
# La nouvelle entrée a la forme d'un dictionnaire."""
    
#     # l'attribut data nous permet de récupérer les données postées
#     phrase_dict = json.loads(request.data)
#     texte = phrase_dict['texte']


#     # Calculer le nouveau identifiant comme le total d'entrées de la table de joincture + 1:
#     # Récuperer la totalité de la table dans une liste de dictionnaires où chaque dictionnaire correspond à une entrée:
#     query = 'SELECT * FROM textetransclasse'
   
#     with connection.cursor(dictionary=True) as cursor:
#         cursor.execute(query)
#         table = cursor.fetchall()

#     nb_entrees = len(table)
#     id = nb_entrees + 1

#     # Insertion de données dans chaque table (insertion dans multiples tables n'est pas assurée par MySQL il me semble)
#     # Table 'texte':
#     insert_texte_query = f"""
#         INSERT INTO texte (texteID, texte) VALUES ({id}, {texte}) 
#         """
#     with connection.cursor() as cursor:
#         cursor.execute(insert_texte_query)
#         connection.commit()

