from enum import Enum
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

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

        # Instanciation des objets métier
        self._deliv_info = DeliveryInfo()
        self._cart = Cart()
        self._partner_set = PartnersSet()

        # Création de données fictives pour la démonstration
        self.initialize_dummy_data()

        # Mise en place de l'interface graphique
        self.setup_ui()

    def initialize_dummy_data(self):
        # Création de quelques médicaments
        med1 = Medicine("Médicament A", "Description A", 10.0)
        med2 = Medicine("Médicament B", "Description B", 15.0)
        med3 = Medicine("Médicament C", "Description C", 20.0)

        # Création de quelques pharmacies avec leurs jours d'ouverture et leur catalogue
        pharm1 = Pharmacy("Pharmacie 1", "Pharmacie centrale",
                          open_days=[Day.Monday, Day.Tuesday, Day.Wednesday, Day.Thursday],
                          catalog=[med1, med2])
        pharm2 = Pharmacy("Pharmacie 2", "Pharmacie sud",
                          open_days=[Day.Thursday, Day.Friday, Day.Saturday],
                          catalog=[med2, med3])
        pharm3 = Pharmacy("Pharmacie 3", "Pharmacie nord",
                          open_days=[Day.Sunday, Day.Monday],
                          catalog=[med1, med3])
        # Ajout des pharmacies au PartnersSet
        self._partner_set._existing_partners.extend([pharm1, pharm2, pharm3])

    def setup_ui(self):
        # --- Zone supérieure gauche : Informations patient ---
        frame_info = tk.Frame(self.root, padx=10, pady=10, borderwidth=2, relief=tk.GROOVE)
        frame_info.grid(row=0, column=0, sticky="nsew")

        # Affichage de la date de commande
        tk.Label(frame_info, text="Date de commande:").grid(row=0, column=0, sticky="w")
        self.date_label = tk.Label(frame_info, text=datetime.now().strftime("%d/%m/%Y"))
        self.date_label.grid(row=0, column=1, sticky="w")

        # Champ Nom
        tk.Label(frame_info, text="Nom:").grid(row=1, column=0, sticky="w")
        self.entry_nom = tk.Entry(frame_info)
        self.entry_nom.grid(row=1, column=1, sticky="w")

        # Champ Prénom
        tk.Label(frame_info, text="Prénom:").grid(row=2, column=0, sticky="w")
        self.entry_prenom = tk.Entry(frame_info)
        self.entry_prenom.grid(row=2, column=1, sticky="w")

        # Bouton de validation (icône disquette)
        self.btn_save = tk.Button(frame_info, text="💾", command=self.save_delivery_info)
        self.btn_save.grid(row=3, column=0, columnspan=2, pady=5)

        # --- Zone inférieure gauche : Choix de pharmacie ---
        self.frame_pharma = tk.LabelFrame(self.root, text="Choix pharmacie", padx=10, pady=10)
        self.frame_pharma.grid(row=1, column=0, sticky="nsew")
        self.pharmacy_var = tk.IntVar(value=-1)        
        self.radio_buttons = []
        # Pour initialiser, on déduit le jour actuel depuis la date affichée
        current_day = self._deliv_info.compute_day(self.date_label.cget("text"))
        self._partner_set.update_available_by_day(current_day)
        self.create_pharmacy_radio_buttons()

        # --- Zone supérieure droite : Panier ---
        frame_cart = tk.LabelFrame(self.root, text="Panier", padx=10, pady=10)
        frame_cart.grid(row=0, column=1, sticky="nsew")
        self.cart_info = tk.Label(frame_cart, text="0 médicaments - Total: 0.0 €")
        self.cart_info.pack()

        # --- Zone principale à droite : Médicaments disponibles ---
        frame_meds = tk.Frame(self.root, padx=10, pady=10, borderwidth=2, relief=tk.GROOVE)
        frame_meds.grid(row=1, column=1, sticky="nsew")
        tk.Label(frame_meds, text="Médicaments disponibles").pack()
        self.med_list_frame = tk.Frame(frame_meds)
        self.med_list_frame.pack()

    def create_pharmacy_radio_buttons(self):
        # Supprime les anciens boutons s'il y en a
        for rb in self.radio_buttons:
            rb.destroy()
        self.radio_buttons.clear()

        # Récupère la liste des pharmacies disponibles
        self.available_partners = self._partner_set.get_available_partners()

        # Crée un bouton radio pour chaque pharmacie disponible
        for index, pharm in enumerate(self.available_partners):
            rb = tk.Radiobutton(
                self.frame_pharma,
                text=pharm.get_name(),
                variable=self.pharmacy_var,
                value=index,  # Affectation d'une valeur entière unique
                command=self.select_pharmacy
            )
            rb.grid(row=index, column=0, sticky="w")
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
        for med in pharmacy.get_catalog():
            med_frame = tk.Frame(self.med_list_frame)
            med_frame.pack(fill="x", pady=2)
            label = tk.Label(med_frame, text=med.get_name())
            label.pack(side="left")
            btn_add = tk.Button(med_frame, text="Ajouter", command=lambda m=med: self.add_medicine_to_cart(m))
            btn_add.pack(side="right")

    def add_medicine_to_cart(self, med):
        """
        Ajoute le médicament sélectionné au panier et met à jour l'affichage du panier.
        """
        self._cart.add_to_cart(med)
        self.cart_info.config(
            text=f"{self._cart.get_nb_med()} médicaments - Total: {self._cart.get_total_price()} €"
        )

# --- Point d'entrée de l'application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MyPharmApp(root)
    root.mainloop()
