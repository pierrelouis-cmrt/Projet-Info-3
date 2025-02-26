from enum import Enum
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk, font

# 1. Énumération Day avec les sept jours de la semaine
class Day(Enum):
    Monday    = 0
    Tuesday   = 1
    Wednesday = 2
    Thursday  = 3
    Friday    = 4
    Saturday  = 5
    Sunday    = 6

# 2. Classe DeliveryInfo
class DeliveryInfo:
    def __init__(self, name="", first_name="", date_str=""):
        self._name = name
        self._first_name = first_name
        self._date = date_str
        ## compute_day permet d'obtenir le jour à partir de la date
        self._day = self.compute_day(date_str) if date_str else None

    def compute_day(self, date_str):
        """
        Transforme une date au format 'dd/mm/yyyy' en un élément de Day.
        """
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            # weekday() retourne 0 pour Monday, 6 pour Sunday
            weekday = date_obj.weekday()
            for day in Day:
                if day.value == weekday:
                    return day
        except ValueError:
            return None

    # Getters / Setters et méthode __str__
    def get_name(self):
        return self._name
    def set_name(self, name):
        self._name = name

    def get_first_name(self):
        return self._first_name
    def set_first_name(self, first_name):
        self._first_name = first_name

    def get_date(self):
        return self._date
    def set_date(self, date_str):
        self._date = date_str
        self._day = self.compute_day(date_str)

    def get_day(self):
        return self._day

    def __str__(self):
        day_str = self._day.name if self._day else "Inconnu"
        return f"{self._first_name} {self._name} - Date: {self._date} ({day_str})"

# 3. Classe Medicine
class Medicine:
    def __init__(self, name, description, price):
        self._name = name
        self._description = description
        self._price = price

    def get_name(self):
        return self._name
    def get_description(self):
        return self._description
    def get_price(self):
        return self._price

    def __str__(self):
        return f"{self._name} : {self._description} - {self._price} €"

# 4. Classe Pharmacy
class Pharmacy:
    def __init__(self, name, description, open_days=None, catalog=None):
        self._name = name
        self._description = description
        self._open_days = open_days if open_days else []   # liste d'éléments Day
        self._catalog = catalog if catalog else []          # liste de Medicine

    def get_name(self):
        return self._name
    def get_description(self):
        return self._description
    def get_open_days(self):
        return self._open_days
    def set_open_days(self, open_days):
        self._open_days = open_days
    def get_catalog(self):
        return self._catalog
    def add_medicine(self, med):
        self._catalog.append(med)

    def __str__(self):
        days = ', '.join(day.name for day in self._open_days)
        return f"Pharmacie {self._name} (Ouverte: {days})"

# 5. Classe PartnersSet
class PartnersSet:
    def __init__(self, existing_partners=None):
        self._existing_partners = existing_partners if existing_partners else []  # Liste de Pharmacy
        self._available_partners = []  # Filtrée par jour d'ouverture
        self._active_partner = None

    def get_existing_partners(self):
        return self._existing_partners
    def get_available_partners(self):
        return self._available_partners
    def get_active_partner(self):
        return self._active_partner
    def set_active_partner(self, partner):
        self._active_partner = partner

    def update_available_by_day(self, day):
        """
        Met à jour la liste des partenaires disponibles en fonction du jour passé.
        """
        self._available_partners = [
            p for p in self._existing_partners if day in p.get_open_days()
        ]

    def __str__(self):
        partners = ', '.join(p.get_name() for p in self._available_partners)
        return f"Partenaires disponibles: {partners}"

# 6. Classe Cart
class Cart:
    def __init__(self):
        self._order = []       # Liste de Medicine
        self._nb_med = 0       # Nombre total de médicaments
        self._total_price = 0.0

    def add_to_cart(self, med):
        self._order.append(med)
        self._nb_med += 1
        self._total_price += med.get_price()

    def get_nb_med(self):
        return self._nb_med
    def get_total_price(self):
        return self._total_price
    def get_order(self):
        return self._order

    def __str__(self):
        meds = ', '.join(med.get_name() for med in self._order)
        return f"{self._nb_med} médicaments ({meds}) - Total: {self._total_price} €"

# 7. Classe MyPharmApp (Interface et orchestration)
class MyPharmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de commande de médicaments")
        
        # Configuration de base de la fenêtre
        self.root.geometry("1100x600")
        self.root.configure(bg="#f0f0f0")
        
        # Configuration des styles
        self.setup_styles()

        # Instanciation des objets métier
        self._deliv_info = DeliveryInfo()
        self._cart = Cart()
        self._partner_set = PartnersSet()

        # Création de données fictives pour la démonstration
        self.initialize_dummy_data()

        # Mise en place de l'interface graphique
        self.setup_ui()

    def setup_styles(self):
        """Configure les styles pour l'interface utilisateur"""
        # Configurer la police par défaut
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica", size=10)
        self.root.option_add("*Font", default_font)
        
        # Style pour ttk
        self.style = ttk.Style()
        self.style.configure("TLabel", background="#f0f0f0", foreground="#333333", padding=5)
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", background="#4a7abc", foreground="#000000", padding=5, font=("Helvetica", 10))
        self.style.map("TButton",
            background=[("active", "#5a8adc"), ("disabled", "#7FA1B7")],
            foreground=[("active", "#4a7abc"), ("disabled", "#999999")])
        
        # Style pour les radiobuttons
        self.style.configure("TRadiobutton", background="#f0f0f0", foreground="#4a7abc", padding=3)
        
        # Style pour le cart
        self.style.configure("Cart.TLabel", background="#ACC4E7", foreground="#333333", padding=8, font=("Helvetica", 11, "bold"))

    def initialize_dummy_data(self):
        # Création de quelques médicaments avec des noms réalistes et amusants
        med1 = Medicine("Dolomax 500", "Antidouleur puissant à base de paracétamol.", 8.5)
        med2 = Medicine("Grippofast", "Traitement contre les symptômes de la grippe.", 12.0)
        med3 = Medicine("NoToux", "Sirop antitussif à action rapide.", 7.5)
        med4 = Medicine("DigestoZen", "Facilite la digestion et réduit les ballonnements.", 9.0)
        med5 = Medicine("Calmoprax", "Anxiolytique léger pour le stress quotidien.", 14.0)
        med6 = Medicine("Somnidor", "Favorise l'endormissement en douceur.", 11.0)
        med7 = Medicine("Nezclair", "Spray nasal décongestionnant.", 6.5)
        med8 = Medicine("Energik+", "Complément vitaminé pour réduire la fatigue.", 13.5)

        # Création de quelques pharmacies avec leurs jours d'ouverture et leur catalogue
        pharm1 = Pharmacy("Pharmacie Saint-Rémi", "Pharmacie centrale",
                        open_days=[Day.Monday, Day.Tuesday, Day.Wednesday, Day.Thursday, Day.Friday],
                        catalog=[med1, med2, med7])
        
        pharm2 = Pharmacy("Pharmacie des Collines", "Pharmacie située en périphérie",
                        open_days=[Day.Wednesday, Day.Thursday, Day.Friday, Day.Saturday],
                        catalog=[med3, med4, med8])
        
        pharm3 = Pharmacy("Pharmacie du Soleil", "Petite pharmacie ouverte le week-end",
                        open_days=[Day.Saturday, Day.Sunday],
                        catalog=[med5, med6, med1])
        
        pharm4 = Pharmacy("Pharmacie Express", "Pharmacie de garde ouverte tous les jours",
                        open_days=[Day.Monday, Day.Tuesday, Day.Wednesday, Day.Thursday, Day.Friday, Day.Saturday, Day.Sunday],
                        catalog=[med2, med3, med5, med6, med7])
        
        # Ajout des pharmacies au PartnersSet
        self._partner_set._existing_partners.extend([pharm1, pharm2, pharm3, pharm4])

    def setup_ui(self):
        # Création des frames principales avec de meilleurs marges et séparations
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        left_frame = ttk.Frame(main_frame, padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_frame = ttk.Frame(main_frame, padding=5)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # --- Zone supérieure gauche : Informations patient ---
        frame_info = ttk.LabelFrame(left_frame, text="Informations patient", padding=10)
        frame_info.pack(fill=tk.X, pady=5)

        # Affichage de la date de commande
        date_frame = ttk.Frame(frame_info)
        date_frame.pack(fill=tk.X, pady=5)
        ttk.Label(date_frame, text="Date de commande:").pack(side=tk.LEFT, padx=5)
        self.date_label = ttk.Label(date_frame, text=datetime.now().strftime("%d/%m/%Y"), 
                                    style="TLabel", borderwidth=1, relief="solid", padding=5)
        self.date_label.pack(side=tk.LEFT, padx=10)

        # Champ Nom
        nom_frame = ttk.Frame(frame_info)
        nom_frame.pack(fill=tk.X, pady=5)
        ttk.Label(nom_frame, text="Nom:", width=10).pack(side=tk.LEFT, padx=5, anchor="w")
        self.entry_nom = ttk.Entry(nom_frame, width=30)
        self.entry_nom.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Champ Prénom
        prenom_frame = ttk.Frame(frame_info)
        prenom_frame.pack(fill=tk.X, pady=5)
        ttk.Label(prenom_frame, text="Prénom:", width=10).pack(side=tk.LEFT, padx=5, anchor="w")
        self.entry_prenom = ttk.Entry(prenom_frame, width=30)
        self.entry_prenom.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Bouton de validation avec meilleur style
        save_frame = ttk.Frame(frame_info)
        save_frame.pack(fill=tk.X, pady=10)
        self.btn_save = ttk.Button(save_frame, text="Enregistrer", command=self.save_delivery_info)
        self.btn_save.pack(padx=10, pady=5, anchor="center")

        # --- Zone inférieure gauche : Choix de pharmacie ---
        self.frame_pharma = ttk.LabelFrame(left_frame, text="Choix de pharmacie", padding=10)
        self.frame_pharma.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.pharmacy_var = tk.IntVar(value=-1)        
        self.radio_buttons = []
        
        # Création d'un cadre défilant pour les pharmacies
        self.pharma_canvas = tk.Canvas(self.frame_pharma, bg="#f0f0f0", highlightthickness=0)
        self.pharma_scrollbar = ttk.Scrollbar(self.frame_pharma, orient=tk.VERTICAL, command=self.pharma_canvas.yview)
        self.pharma_canvas.configure(yscrollcommand=self.pharma_scrollbar.set)
        
        self.pharma_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.pharma_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.pharma_list_frame = ttk.Frame(self.pharma_canvas)
        self.pharma_canvas.create_window((0, 0), window=self.pharma_list_frame, anchor="nw")
        self.pharma_list_frame.bind("<Configure>", lambda e: self.pharma_canvas.configure(scrollregion=self.pharma_canvas.bbox("all")))
        
        # Pour initialiser, on déduit le jour actuel depuis la date affichée
        current_day = self._deliv_info.compute_day(self.date_label.cget("text"))
        self._partner_set.update_available_by_day(current_day)
        self.create_pharmacy_radio_buttons()

        # --- Zone supérieure droite : Panier ---
        frame_cart = ttk.LabelFrame(right_frame, text="Panier", padding=10)
        frame_cart.pack(fill=tk.X, pady=5)
        
        # Amélioration de l'affichage du panier
        self.cart_frame = ttk.Frame(frame_cart, padding=5)
        self.cart_frame.pack(fill=tk.X, pady=5)
        
        self.cart_icon = ttk.Label(self.cart_frame, text="🛒", font=("Helvetica", 14))
        self.cart_icon.pack(side=tk.LEFT, padx=5)
        
        self.cart_info = ttk.Label(self.cart_frame, 
                                  text="0 médicaments - Total: 0.0 €", 
                                  style="Cart.TLabel")
        self.cart_info.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # --- Zone principale à droite : Médicaments disponibles ---
        frame_meds = ttk.LabelFrame(right_frame, text="Médicaments disponibles", padding=10)
        frame_meds.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Création d'un canvas avec scrollbar pour les médicaments
        self.meds_canvas = tk.Canvas(frame_meds, bg="#f0f0f0", highlightthickness=0)
        self.meds_scrollbar = ttk.Scrollbar(frame_meds, orient=tk.VERTICAL, command=self.meds_canvas.yview)
        self.meds_canvas.configure(yscrollcommand=self.meds_scrollbar.set)
        
        self.meds_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.meds_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.med_list_frame = ttk.Frame(self.meds_canvas)
        self.meds_canvas.create_window((0, 0), window=self.med_list_frame, anchor="nw")
        self.med_list_frame.bind("<Configure>", lambda e: self.meds_canvas.configure(scrollregion=self.meds_canvas.bbox("all")))

    def create_pharmacy_radio_buttons(self):
        # Supprime les anciens boutons s'il y en a
        for widget in self.pharma_list_frame.winfo_children():
            widget.destroy()
        self.radio_buttons.clear()

        # Récupère la liste des pharmacies disponibles
        self.available_partners = self._partner_set.get_available_partners()

        # Crée un bouton radio pour chaque pharmacie disponible
        for index, pharm in enumerate(self.available_partners):
            # Création d'un cadre pour chaque pharmacie avec description
            pharm_frame = ttk.Frame(self.pharma_list_frame, padding=5)
            pharm_frame.pack(fill=tk.X, pady=2)
            
            rb = ttk.Radiobutton(
                pharm_frame,
                text=pharm.get_name(),
                variable=self.pharmacy_var,
                value=index,
                command=self.select_pharmacy
            )
            rb.pack(side=tk.LEFT, anchor="w")
            self.radio_buttons.append(rb)
            
            # Ajout de la description en dessous
            desc_label = ttk.Label(self.pharma_list_frame, 
                                  text=f"  {pharm.get_description()}", 
                                  foreground="#666666", 
                                  font=("Helvetica", 9, "italic"))
            desc_label.pack(fill=tk.X, padx=25, pady=(0, 5))
            
            # Ajouter une ligne séparatrice sauf pour le dernier élément
            if index < len(self.available_partners) - 1:
                separator = ttk.Separator(self.pharma_list_frame, orient='horizontal')
                separator.pack(fill=tk.X, padx=5, pady=5)

    def save_delivery_info(self):
        """
        Récupère les informations saisies et les sauvegarde dans l'objet DeliveryInfo.
        Puis, met à jour la liste des pharmacies disponibles en fonction du jour.
        """
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        date_str = self.date_label.cget("text")
        
        # Vérification des champs
        if not nom or not prenom:
            messagebox.showwarning("Informations incomplètes", "Veuillez remplir tous les champs.")
            return
            
        self._deliv_info.set_date(date_str)
        self._deliv_info.set_name(nom)
        self._deliv_info.set_first_name(prenom)
        messagebox.showinfo("Informations enregistrées", f"Infos enregistrées : {self._deliv_info}")

        # Mise à jour des pharmacies disponibles selon le jour de livraison
        current_day = self._deliv_info.get_day()
        if current_day:
            self._partner_set.update_available_by_day(current_day)
            self.create_pharmacy_radio_buttons()
        else:
            messagebox.showerror("Erreur", "Date invalide, impossible de déterminer le jour.")

    def select_pharmacy(self):
        """
        Lorsqu'une pharmacie est sélectionnée, on enregistre la pharmacie active
        et on met à jour l'affichage des médicaments disponibles.
        """
        index = self.pharmacy_var.get()
        if 0 <= index < len(self.available_partners):
            selected_pharmacy = self.available_partners[index]
            self._partner_set.set_active_partner(selected_pharmacy)
            self.update_medicines_display(selected_pharmacy)

    def update_medicines_display(self, pharmacy):
        """
        Affiche la liste des médicaments disponibles de la pharmacie sélectionnée.
        Pour chaque médicament, un bouton 'Ajouter' permet de l'ajouter au panier.
        """
        # Effacer l'ancienne liste
        for widget in self.med_list_frame.winfo_children():
            widget.destroy()

        # Créer l'affichage pour chaque médicament
        for i, med in enumerate(pharmacy.get_catalog()):
            # Création d'un cadre pour chaque médicament
            med_frame = ttk.Frame(self.med_list_frame, padding=5)
            med_frame.pack(fill=tk.X, pady=5)
            
            # Icône de médicament
            med_icon = ttk.Label(med_frame, text="💊", font=("Helvetica", 12))
            med_icon.pack(side=tk.LEFT, padx=5)
            
            # Informations du médicament
            info_frame = ttk.Frame(med_frame)
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            name_label = ttk.Label(info_frame, text=med.get_name(), font=("Helvetica", 10, "bold"))
            name_label.pack(anchor="w")
            
            desc_label = ttk.Label(info_frame, text=med.get_description(), wraplength=300)
            desc_label.pack(anchor="w")
            
            price_label = ttk.Label(info_frame, text=f"{med.get_price()} €", foreground="#2c5282", font=("Helvetica", 10, "bold"))
            price_label.pack(anchor="w")
            
            # Bouton d'ajout au panier
            btn_frame = ttk.Frame(med_frame)
            btn_frame.pack(side=tk.RIGHT, padx=5)
            
            btn_add = ttk.Button(btn_frame, text="Ajouter au panier", command=lambda m=med: self.add_medicine_to_cart(m))
            btn_add.pack()
            
            # Ajout d'un séparateur entre les médicaments
            if i < len(pharmacy.get_catalog()) - 1:
                separator = ttk.Separator(self.med_list_frame, orient='horizontal')
                separator.pack(fill=tk.X, padx=5, pady=5)

    def add_medicine_to_cart(self, med):
        """
        Ajoute le médicament sélectionné au panier et met à jour l'affichage du panier.
        """
        self._cart.add_to_cart(med)
        total_price = self._cart.get_total_price()
        nb_med = self._cart.get_nb_med()
        
        # Affichage amélioré du panier
        cart_text = f"{nb_med} médicament{'s' if nb_med > 1 else ''} - Total: {total_price:.2f} €"
        self.cart_info.config(text=cart_text)
        
        # Animation d'ajout
        self.cart_info.configure(foreground="#4a7abc")
        self.root.after(300, lambda: self.cart_info.configure(foreground="#333333"))
        
        # Notification d'ajout
        messagebox.showinfo("Panier mis à jour", f"'{med.get_name()}' ajouté au panier.")

# --- Point d'entrée de l'application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MyPharmApp(root)
    root.mainloop()