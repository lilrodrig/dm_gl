# Se connecter à la base de données "dialectes" et au serveur Flask
# Pouvoir voir "texte", "transcription" et "classe" de toute la base ou d'une seule entrée, au choix de l'utilisateur.
# Affichage de ces informations en forme graphique et de tableau. 
# N.B.: variables "user_input" et "password" (lignes 19 et 20) sont à changer par les tiens, ici leurs valeurs sont des placeholders.

from flask import Flask, redirect, url_for, render_template, request 
from mysql.connector import connect, Error
import pandas as pd
from flask import Flask, render_template 
from bokeh.embed import components 
from bokeh.plotting import figure 
from bokeh.models import ColumnDataSource
from bokeh.models import BoxZoomTool, PanTool, ResetTool, LassoSelectTool, WheelZoomTool
from bokeh.models.widgets import DataTable, TableColumn


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


# Page comportant un champ texte pour que l'utilisateur interagisse avec la base de données
@app.route('/dialectes')
def dialectes():
   """Donne à l'utilisateur un formulaire (un champ texte) pour le choix entre afficher une entrée unique, 
    qu'il indiquera par la même occasion, ou la totalité de la base de données."""
   return render_template('dialectes.html')

@app.route('/dialectes_choix',methods = ['POST'])
def dialectes_choix():
    """Lire le choix de l'utilisateur, selon l'option fournie dans le champs texte, et redirectionner
    la page vers le mode d'affichage qui correspond (entrée unique ou totalité de la base de données)."""
    
    # Valeur entrée dans le formulaire récupérée sous forme de dictionnaire
    result = request.form
    value = int(result.get("Ecrivez un chifre entre 1-20 pour une seule phrase ou 21 pour toute la table."))
    
    # La redirection pour affichage dans chaque cas:

    # Valeur spécifique de la table, une seule entrée affichée sur la page web:
    if value in list(range(1,21)):

        # Sélectionner texte, transcription et classe dans les tables respectives selon les relations notées dans la 
        # table de joincture pour l'entrée indiquée par l'utilisateur:
        return redirect(url_for('api_textetransclasse', id=value))
 
    else:
        # Toute la table est prise et affichée avec un graphique et un tableau sur la page web:
        return redirect(url_for('api_phrases_all'))



## Fonction pour pouvoir voir tout le contenu de la base de données, toutes tables confondues selon
# les relations indiquées dans la table de joincture:

# Récupérer toutes les entrées de la base de données:
@app.route('/dialectes_choix/tout', methods=['GET'])
def api_phrases_all():
    """Affichage graphique et par tableau d'informations de toutes les entrées de la base de données
    récupérées selon les relations indiquées dans la table de joincture. L'utilisateur pourra effectuer 
    plusieurs manipulations avec les deux images."""

    # Requête pour sélectionner le texte, transcription et classe dialectale de toutes les entrées
    select_all_query = """
        SELECT texte.texte, transcription.transcription, classe.dialecte
        FROM textetransclasse LEFT JOIN texte ON textetransclasse.texteID=texte.texteID
        LEFT JOIN transcription ON textetransclasse.transcriptionID=transcription.transcriptionID
        LEFT JOIN classe ON textetransclasse.classeID=classe.classeID
        """
    
    # les résultats viendront dans une liste de dictionnaires (un par entrée), 
    # et le dictionnaire conserve les noms de colonnes de la base de données.
   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(select_all_query)
        results = cursor.fetchall()

    if results == []:
        return "Il n'y a pas de données dans cette database."
    else:
        # Préparer variables pour plot et tableau - conversion de la database récupérée en dataframe, 
        # puis en liste par variable (dialecte, texte et transcription):
        
        df = pd.json_normalize(results)
        dialecte = list(df['dialecte'])
        dialectex = list(set(dialecte))
        dialectecount = [dialecte.count('français breton'), dialecte.count("français 'standard'")]


        # Graphique et tableau:

        # Bar plot
        # Plot responsive pour la largeur de l'écran et intéractif avec des outils de manipulation:
        # glisser le plot latéralement, zoommer, sélectionner et remise à zéro.
                
        p1 = figure( 
            x_range=dialectex, 
            height=350, 
            title="Nombre d'entrées par dialecte", 
            sizing_mode="stretch_width",
            tools=[BoxZoomTool(), ResetTool(),WheelZoomTool(),PanTool(dimensions="width"),LassoSelectTool()]
        ) 
        p1.vbar(x=dialectex, top=dialectecount, color='yellow', width=0.9) 
        p1.xgrid.grid_line_color = None
        p1.y_range.start = 0

       
        # Tableau
        # Tableau dont les colonnes ont la largeur ajustable. Changement d'ordre d'entrées possible avec
        # des flèches dans les titres de colonnes. On peut aussi faire défiler le tableau: 
        colonnes = [TableColumn(field=i, title=i) for i in df.columns]
        table_jolie = DataTable(columns=colonnes, source=ColumnDataSource(df))
        
        # Créer code de contenu et d'affichage des images (graphique et tableau) pour le script html:
        script1, div1 = components(p1)
        script2, div2 = components(table_jolie) 
        
        # Envoyer le code pour l'affichage par le script html:
        return render_template( 
            template_name_or_list='chart.html', 
            script=[script1,script2], 
            div=[div1,div2], 
        ) 


## Fonction pour pouvoir voir le contenu spécifique de la base de données par l'identifiant d'une seule entrée:

# Demander une phrase par son identifiant et recevoir le texte, la transcription et la classe (selon les 
# relations indiquées dans la table de joincture) affichés dans un tableau :

@app.route('/dialectes_choix/<id>', methods=['GET'])
def api_textetransclasse(id):
    """La fonction prend l'identifiant fourni par l'utilisateur dans l'URL de requête 
    pour récupérer le contenue textuel correspondant de l'entrée concernée,
    (texte, transcription et classe dialectale), à l'aide des identifiants notés comme clé étrangère
    dans la table de joncture. L'information récupérée est affichée dans un tableau.
    """

    # Convertir l'identifiant en entier:
    id = int(id)
   
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
        maximale de la table. Fournissez un argument compris dans ce rang."


    # Sélectionner texte, transcription et classe dans les tables respectives selon les relations notées dans la 
    # table de joincture pour l'entrée indiquée par l'utilisateur:
    select_id_query = f"""
        SELECT texte.texte, transcription.transcription, classe.dialecte
        FROM textetransclasse LEFT JOIN texte ON textetransclasse.texteID=texte.texteID
        LEFT JOIN transcription ON textetransclasse.transcriptionID=transcription.transcriptionID
        LEFT JOIN classe ON textetransclasse.classeID=classe.classeID WHERE textetransclasse.id={id}
        """

    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(select_id_query)
        entree = cursor.fetchall()
    
    if entree == []:
        return "Cette entrée n'existe pas dans la table."
    else:
        # Afficher le contenu textuel correspondant à l'identifiant dans un tableau:
        return render_template("table_results.html",resultat = entree[0])



if __name__ == '__main__':
   
   app.secret_key = 'ddd'

   # debug = True - des éventuelles modifications du code sont intégrées par recharge de la page sans avoir à redémarrer le serveur
   app.run(debug = True)

