-- Création de la database "dialectes":

CREATE SCHEMA dialectes;

-- Création de 4 tables dans la database: 

CREATE TABLE dialectes.Texte (
  texteID INT NOT NULL AUTO_INCREMENT,
  texte VARCHAR(255) NULL,
  PRIMARY KEY (texteID));
  
CREATE TABLE dialectes.Transcription (
  transcriptionID INT NOT NULL AUTO_INCREMENT,
  transcription VARCHAR(255) NULL,
  PRIMARY KEY (transcriptionID));
  
CREATE TABLE dialectes.Classe (
  classeID INT NOT NULL AUTO_INCREMENT,
  dialecte VARCHAR(45) NULL,
  PRIMARY KEY (classeID));
  
CREATE TABLE dialectes.texteTransClasse (
  id INT NOT NULL AUTO_INCREMENT,
  texteID INT NOT NULL,
  transcriptionID INT NOT NULL,
  classeID INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (texteID) REFERENCES Texte (texteID),
  FOREIGN KEY (transcriptionID) REFERENCES Transcription (transcriptionID),
  FOREIGN KEY (classeID) REFERENCES Classe (classeID));

-- Remplissage des tables:

-- Table "Texte":

INSERT INTO dialectes.Texte (texteID, texte) VALUES (1, "Bon, je ne suis pas amer, c’est tout."), 
(2, "J’avais annoncé que j’étais pas pour les fusions."), (3, "Il faut être présent."), 
(4, "C’est une dynamique importante depuis le départ."), (5, "On partage une victoire en commun."), 
(6, "Chacun a fait ce qu’il a pu."), (7, "C’est quelqu’un pour qui j’ai beaucoup d’amitié."), 
(8, "Cette période nous a aussi permis d’ouvrir les yeux."), (9, "C’est un regard également neuf."), 
(10, "Donc j’aime le sport collectif pour cela."), (11, "Pendant trois ans j’ai fait une licence de sociologie."), 
(12, "C’est tendu, je trouve, pour elle."), (13, "C’est une agence spécialisée dans la construction de gares."), 
(14, "Aujourd’hui je me donne plus ce droit d’aller flâner."), (15, "Elle connaît bien les coutumes locales."), 
(16, "L’après-midi on faisait de la musique."), (17, "Ça sert dans la vie de tous les jours."), 
(18, "On va essayer de recycler les éléments qui sont sur place."), (19, "J’ai aimé le jeu de la dame."), 
(20, "Ma grand-mère, elle avait une maison dans l’Aveyron toujours.");

-- Table "Transcription":

INSERT INTO dialectes.Transcription (transcriptionID, transcription) VALUES (1, "bO~ Z@ n@ sHi pazamER se tu"), 
(2, "ZavE anO~se k@ ZetE pa puR le fyzjO~"), (3, "il fo EtR pRezA~"), (4, "setyn dinamik E~pORtA~t@ d@pHi l@ depaR "), 
(5, "O~ paRtaZ yn viktwaR A~ kOmE~"), (6, "SakE~ a fE s@ kil a py"), (7, "se kElkE~ puR ki ZE boku damitje"), 
(8, "sEt peRjOd nuza osi pERmi duvRiR lezj2"), (9, "setE~ R@gaR egalmA~ n9f"), (10, "dO~k ZEm l@ spOR kOlEktif puR s@la"), 
(11, "pA~dA~ tRwazA~ ZE fE yn lisA~s d@ sosjoloZi"), (12, "se tA~dy Z@ tRuv puR El"),
(13, "setynaZA~s spesjalize dA~ la kO~stRyksjO~ d@ gaR"), (14, "oZuRdHi Z@ m@ dOn ply s@ dRwa dale flane"), 
(15, "El kOnE bjE~ le kutym lokal"), (16, "lapREmidi O~ fezE d@ la myzik"), (17, "sa sER dA~ la vi d@ tu le ZuR"), 
(18, "O~ va eseje d@ R@sikle lezelemA~ ki sO~ syR plas"), (19, "ZE eme l@ Z2 d@ la dam"), 
(20, "ma gRA~mER El avE yn mezO~ dA~ laveRO~ tuZuR");

-- Table "Classe":

INSERT INTO dialectes.Classe (classeID, dialecte) VALUES (1, "français breton"), (2, "français 'standard'");

-- Table "texteTransClasse":

INSERT INTO dialectes.texteTransClasse (id, texteID, transcriptionID, classeID) VALUES (1, 1, 1, 1), (2, 2, 2, 1),
(3, 3, 3, 1), (4, 4, 4, 1), (5, 5, 5, 1), (6, 6, 6, 1), (7, 7, 7, 1), (8, 8, 8, 1), (9, 9, 9, 1), (10, 10, 10, 1),
(11, 11, 11, 2), (12, 12, 12, 2), (13, 13, 13, 2), (14, 14, 14, 2), (15, 15, 15, 2), (16, 16, 16, 2), (17, 17, 17, 2),
(18, 18, 18, 2), (19, 19, 19, 2), (20, 20, 20, 2);


-- fin
