import json

devices = {
            "komputery": [
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia")
            ],
            "drukarki": [
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia")
            ],
            "serwerownia": [
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia"),
                ("Nazwa_urzadzenia", "Adres_IP", "Imie_i_Nazwisko", "Pokoj", "Typ_polaczenia")
            ]
        }

# Zapisz słownik do pliku JSON
with open('devices.json', 'w') as file:
    json.dump(devices, file, indent=4)