from enum import Enum
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import customtkinter

# Choix du thème par défaut

customtkinter.set_default_color_theme("farfelue.json")  # Thème de couleur (exemple : "blue", "green", etc.)

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
        # compute_day permet d'obtenir le jour à partir de la date
        self._day = self.compute_day(date_str) if date_str else None

    def compute_day(self, date_str):
        """
        Transforme une date au format 'dd/mm/yyyy' en un élément de Day.
        """
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            weekday = date_obj.weekday()  # 0 pour Monday, 6 pour Sunday
            for day in Day:
                if day.value == weekday:
                    return day
        except ValueError:
            return None

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

        # Instanciation des objets métier
        self._deliv_info = DeliveryInfo()
        self._cart = Cart()
        self._partner_set = PartnersSet()

        # Variable de thème pour la commutation
        self.theme_mode = customtkinter.get_appearance_mode()  # "Dark" ou "Light"

        # Création de données fictives pour la démonstration
        self.initialize_dummy_data()

        # Mise en place de l'interface graphique avec customtkinter
        self.setup_ui()

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
        # --- Barre de titre avec bouton de changement de thème ---
        self.top_frame = customtkinter.CTkFrame(self.root, corner_radius=10)
        self.top_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")
        self.top_frame.grid_columnconfigure(0, weight=1)
        title_label = customtkinter.CTkLabel(self.top_frame, text="Application de commande de médicaments", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.theme_switch_button = customtkinter.CTkButton(self.top_frame, text="Switch Theme", command=self.toggle_theme, width=120)
        self.theme_switch_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # Configuration de la grille principale pour les autres zones
        self.root.grid_columnconfigure((0,1), weight=1)
        self.root.grid_rowconfigure((1,2), weight=1)

        # --- Zone supérieure gauche : Informations patient ---
        self.frame_info = customtkinter.CTkFrame(self.root, corner_radius=10)
        self.frame_info.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        # Date de commande
        lbl_date_title = customtkinter.CTkLabel(self.frame_info, text="Date de commande:")
        lbl_date_title.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.date_label = customtkinter.CTkLabel(self.frame_info, text=datetime.now().strftime("%d/%m/%Y"))
        self.date_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        # Champ Nom
        lbl_nom = customtkinter.CTkLabel(self.frame_info, text="Nom:")
        lbl_nom.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_nom = customtkinter.CTkEntry(self.frame_info)
        self.entry_nom.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        # Champ Prénom
        lbl_prenom = customtkinter.CTkLabel(self.frame_info, text="Prénom:")
        lbl_prenom.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_prenom = customtkinter.CTkEntry(self.frame_info)
        self.entry_prenom.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        # Bouton de validation (icône disquette)
        self.btn_save = customtkinter.CTkButton(self.frame_info, text="💾 Sauvegarder", command=self.save_delivery_info)
        self.btn_save.grid(row=3, column=0, columnspan=2, pady=10)

        # --- Zone inférieure gauche : Choix de pharmacie ---
        self.frame_pharma = customtkinter.CTkFrame(self.root, corner_radius=10)
        self.frame_pharma.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        lbl_pharma_title = customtkinter.CTkLabel(self.frame_pharma, text="Choix pharmacie", font=("Arial", 14, "bold"))
        lbl_pharma_title.grid(row=0, column=0, padx=10, pady=(10,5), sticky="w")
        self.pharmacy_var = tk.IntVar(value=-1)        
        self.radio_buttons = []
        current_day = self._deliv_info.compute_day(self.date_label.cget("text"))
        self._partner_set.update_available_by_day(current_day)
        self.create_pharmacy_radio_buttons()

        # --- Zone supérieure droite : Panier ---
        self.frame_cart = customtkinter.CTkFrame(self.root, corner_radius=10)
        self.frame_cart.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        lbl_cart_title = customtkinter.CTkLabel(self.frame_cart, text="Panier", font=("Arial", 14, "bold"))
        lbl_cart_title.pack(padx=10, pady=(10,5))
        self.cart_info = customtkinter.CTkLabel(self.frame_cart, text="0 médicaments - Total: 0.0 €")
        self.cart_info.pack(padx=10, pady=5)

        # --- Zone principale inférieure droite : Médicaments disponibles ---
        self.frame_meds = customtkinter.CTkFrame(self.root, corner_radius=10)
        self.frame_meds.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        lbl_meds_title = customtkinter.CTkLabel(self.frame_meds, text="Médicaments disponibles", font=("Arial", 14, "bold"))
        lbl_meds_title.pack(padx=10, pady=(10,5))
        self.med_list_frame = customtkinter.CTkFrame(self.frame_meds, corner_radius=5)
        self.med_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def create_pharmacy_radio_buttons(self):
        # Supprime les anciens boutons s'il y en a
        for rb in self.radio_buttons:
            rb.destroy()
        self.radio_buttons.clear()

        self.available_partners = self._partner_set.get_available_partners()
        for index, pharm in enumerate(self.available_partners):
            rb = customtkinter.CTkRadioButton(
                master=self.frame_pharma,
                text=pharm.get_name(),
                variable=self.pharmacy_var,
                value=index,
                command=self.select_pharmacy
            )
            rb.grid(row=index+1, column=0, sticky="w", padx=15, pady=5)
            self.radio_buttons.append(rb)

    def save_delivery_info(self):
        """
        Récupère les informations saisies et les sauvegarde dans l'objet DeliveryInfo.
        Puis, met à jour la liste des pharmacies disponibles en fonction du jour.
        """
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        date_str = self.date_label.cget("text")
        self._deliv_info.set_date(date_str)
        self._deliv_info.set_name(nom)
        self._deliv_info.set_first_name(prenom)
        messagebox.showinfo("Infos", f"Infos enregistrées : {self._deliv_info}")

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
        """
        for widget in self.med_list_frame.winfo_children():
            widget.destroy()

        for med in pharmacy.get_catalog():
            med_frame = customtkinter.CTkFrame(self.med_list_frame, corner_radius=5)
            med_frame.pack(fill="x", padx=10, pady=5)
            lbl_med = customtkinter.CTkLabel(med_frame, text=med.get_name())
            lbl_med.pack(side="left", padx=10)
            btn_add = customtkinter.CTkButton(med_frame, text="Ajouter", command=lambda m=med: self.add_medicine_to_cart(m))
            btn_add.pack(side="right", padx=10)

    def add_medicine_to_cart(self, med):
        """
        Ajoute le médicament sélectionné au panier et met à jour l'affichage du panier.
        """
        self._cart.add_to_cart(med)
        self.cart_info.configure(
            text=f"{self._cart.get_nb_med()} médicaments - Total: {self._cart.get_total_price()} €"
        )

    def toggle_theme(self):
        """
        Change le thème entre Dark et Light.
        """
        # Bascule le mode d'apparence
        new_mode = "Light" if self.theme_mode == "Dark" else "Dark"
        customtkinter.set_appearance_mode(new_mode)
        self.theme_mode = new_mode

# --- Point d'entrée de l'application ---
if __name__ == "__main__":
    root = customtkinter.CTk()
    app = MyPharmApp(root)
    root.mainloop()
