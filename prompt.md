# Application de commande de médicaments

## Objectifs principaux  

- Utiliser la programmation orientée objet pour la modélisation d’une solution à un problème, en Python 
- Séparer les responsabilités entre les classes et en particulier entre le modèle conceptuel et l’interface graphique + interactions utilisateur 

## Modèle conceptuel à suivre :

1. **Énumération : `Day`**  
   - Il s’agit d’un type énuméré avec sept valeurs possibles :  
     - **Monday**, **Tuesday**, **Wednesday**, **Thursday**, **Friday**, **Saturday**, **Sunday**  
   - Le diagramme indique une relation entre l’énumération `Day` et plusieurs classes (par exemple, `Pharmacy` peut stocker des `Day` comme jours d’ouverture).

2. **Classe `DeliveryInfo`**  
   - Attributs privés :  
     - `_name : str` (nom)  
     - `_first_name : str` (prénom)  
     - `_date : str` (date, vraisemblablement la date de livraison)  
     - `_day : Day` (jour de la semaine correspondant à la date)  
   - Méthodes / Constructeur :  
     - Constructeur, getters, setters et `__str__()`.  
     - `compute_day(Date): Day` (une méthode permettant de déterminer le jour `Day` à partir d’une date).

   - Relation :  
     - `DeliveryInfo` est associé à l’énumération `Day` (indiqué par un attribut `_day`).  

3. **Classe `Pharmacy`**  
   - Attributs privés :  
     - `_name : str` (nom de la pharmacie)  
     - `_description : str` (description générale)  
     - `_open_days : Day[]` (liste ou tableau de jours d’ouverture)  
     - `_catalog : Medicine[]` (catalogue de médicaments disponibles)  
   - Méthodes / Constructeur :  
     - Constructeur, getters, setters et `__str__()`, etc.  

   - Relations :  
     - `Pharmacy` entretient une relation 1..* avec `Day` pour ses jours d’ouverture (via `_open_days`).  
     - `Pharmacy` entretient une relation 1..* avec `Medicine` pour les médicaments (`_catalog`).

4. **Classe `PartnersSet`**  
   - Attributs privés :  
     - `_existing_partners : Pharmacy[]` (liste des partenaires existants)  
     - `_available_partners : Pharmacy[]` (liste des partenaires disponibles, selon certains critères)  
     - `_active_partner : Pharmacy` (le partenaire actuellement sélectionné)  
   - Méthodes / Constructeur :  
     - Constructeur, getters, setters, `__str__()`.  
     - `update_available_by_day(Day): NoneType` (met à jour les partenaires disponibles en fonction du jour passé en paramètre).  

   - Relations :  
     - Il y a une multiplicité de 1..\*, 0..\* et 0..1 entre `PartnersSet` et `Pharmacy` (car un ensemble de partenaires gère potentiellement plusieurs pharmacies).  

5. **Classe `Medicine`**  
   - Attributs privés :  
     - `_name : str` (nom du médicament)  
     - `_description : str` (description)  
     - `_price : float` (prix)  
   - Méthodes / Constructeur :  
     - Constructeur, getters, setters et `__str__()`.  
   - Relation :  
     - `Medicine` est référencé par `Pharmacy` avec 1..* (via `_catalog`) et par `Cart` (via `_order`).  

6. **Classe `Cart`**  
   - Attributs privés :  
     - `_order : Medicine[]` (liste des médicaments ajoutés au panier)  
     - `_nb_med : int` (nombre total de médicaments dans le panier)  
     - `_total_price : float` (coût total du panier)  
   - Méthodes / Constructeur :  
     - Constructeur, getters, setters, `__str__()`.  
     - `add_to_cart(med: Medicine): NoneType` (permet d’ajouter un médicament dans la liste `_order`).  

   - Relations :  
     - Relation 0..* entre `Cart` et `Medicine` (puisque le panier peut contenir plusieurs médicaments).  

7. **Classe `MyPharmApp`**  
   - Attributs (instances des classes précédentes + éléments d’interface) :  
     - `_deliv_info : DeliveryInfo` (gestion des infos de livraison)  
     - `_parten_set : PartnersSet` (ensemble des partenaires)  
     - `_cart : Cart` (panier courant)  
     - `_labelXXX : Label etc.` (exemples d’objets d’interface graphique)  
     - `_buttonXXX : Button etc.` (exemples de boutons)  
   - Méthodes / Comportements :  
     - `on_clickXXX()`, etc. (fonctions de gestion d’événements)  
     - `update_xxx(...)` (méthodes de mise à jour)  

   - Relation :  
     - `MyPharmApp` détient en agrégation ou composition (1–1) un objet `DeliveryInfo`, un objet `PartnersSet` et un objet `Cart`.

---

**Récapitulatif des associations et multiplicités principales** :
- `DeliveryInfo` possède un seul `Day` (via l’attribut `_day`).
- `Pharmacy` a 1..* jours d’ouverture (`_open_days : Day[]`).
- `Pharmacy` possède 0..* `Medicine` dans son catalogue (`_catalog : Medicine[]`).
- `PartnersSet` gère 1..* `Pharmacy` (liste de partenaires existants et disponibles).
- `Cart` peut contenir 0..* `Medicine`.
- `MyPharmApp` regroupe :
  - 1 `DeliveryInfo`
  - 1 `PartnersSet`
  - 1 `Cart`
  - Divers composants d’interface (labels, boutons, etc.).

Ce diagramme illustre donc une application où l’on peut gérer :
- Un utilisateur (via `DeliveryInfo`),  
- Une liste de pharmacies partenaires (via `PartnersSet`),  
- Un panier de médicaments (via `Cart`)  
- Les différents jours de la semaine (via l’énumération `Day`)  
- Avec une interface (`MyPharmApp`) permettant d’orchestrer et d’afficher toutes ces entités."

## Interface simple à mettre en place 
 
1) L’idée est que tout d’abord la date de commande  soit  directement 
affichée puis le nom et prénom renseignés. 
Après validation sur le symbole disquette, cela affiche les pharmacies de 
l’application. 
 
2) Le  client  choisit  une  pharmacie  parmi  la  liste.  Cela  affiche  alors  à 
droite les médicaments disponibles. 
 
3) A  chaque  clic  sur  le  chariot  à côté d’un médicament,  cela  ajoute  le 
médicament dans le panier actuel. 
 
 Voici à quoi ressemble l’interface, telle qu’on peut l’imaginer en s’inspirant du mock-up fourni :

1. **Zone supérieure gauche (informations patient)**  
   - Un bloc affichant la date, puis deux champs :  
     - « Nom » (label + champ de saisie)  
     - « Prénom » (label + champ de saisie)  
   - À côté (ou en bas) de ces champs, on remarque une icône de disquette, probablement pour sauvegarder ces informations.

2. **Zone inférieure gauche (choix de pharmacie)**  
   - Un cadre (label frame ou frame) intitulé « Choix pharmacie »  
   - Trois boutons radio (xxxxx1, xxxx2, xxxx3), permettant de sélectionner une seule pharmacie à la fois.

3. **Zone supérieure droite (panier)**  
   - Un cadre indiquant « Panier », avec :  
     - Une partie texte montrant « XX médicaments » (le nombre total d’articles dans le panier)  
     - Le montant total « XX € » (le prix total)  

4. **Zone principale à droite (médicaments disponibles)**  
   - Un label indiquant « Médicaments disponibles »  
   - Une liste de médicaments du type « Médicament xxx », « Médicament xxx2 », etc.  
   - À côté de chaque médicament, une icône de panier (ou un bouton) pour ajouter ce médicament au panier.

Visuellement, l’écran est donc divisé en deux colonnes principales :
- **Colonne de droite** : en haut, un résumé du panier, et en dessous la liste des médicaments disponibles à l’achat.  

L’aspect global est assez simple : un grand cadre pour l’application, avec un titre ou des labels indiquant clairement chaque bloc fonctionnel (informations patient, choix de pharmacie, panier, liste des médicaments).

Infos supplémentaires :

Rappel : date est juste un str au format 17/12/2005 alors que day est un Day (enum), le jour de la semaine
