#!/usr/bin/env python3
import os
from flask_migrate import Migrate
from flask.cli import FlaskGroup

from app import create_app, db
from app.models import Client, Furnizor, CategorieProdusCheltuiala, Produs, Factura, DetaliiFactura, FacturaPrimita, MiscareStoc

app = create_app()
cli = FlaskGroup(app)

@cli.command("create_tables")
def create_tables():
    """Create database tables"""
    db.create_all()
    print("Database tables created!")

@cli.command("add_sample_data")
def add_sample_data():
    """Add sample data to the database"""
    # Add categories
    categorii = [
        CategorieProdusCheltuiala(nume="Electronice", descriere="Produse electronice și electrocasnice"),
        CategorieProdusCheltuiala(nume="Mobilă", descriere="Mobilier și decorațiuni"),
        CategorieProdusCheltuiala(nume="Birotică", descriere="Articole de birou și papetărie"),
        CategorieProdusCheltuiala(nume="IT", descriere="Echipamente și servicii IT"),
        CategorieProdusCheltuiala(nume="Software", descriere="Licențe și servicii software"),
        CategorieProdusCheltuiala(nume="Marketing", descriere="Materiale și servicii de marketing")
    ]
    db.session.add_all(categorii)
    
    # Add clients
    clienti = [
        Client(nume="SC Example SRL", cui="RO12345678", adresa="Str. Exemplu nr. 1", oras="București", judet="București", telefon="0712345678", email="contact@example.ro"),
        Client(nume="SC Demo SA", cui="RO87654321", adresa="Bd. Test nr. 10", oras="Cluj-Napoca", judet="Cluj", telefon="0723456789", email="office@demo.ro"),
        Client(nume="SC TechSolutions SRL", cui="RO22334455", adresa="Str. Tehnologiei nr. 42", oras="Timișoara", judet="Timiș", telefon="0734567891", email="office@techsolutions.ro"),
        Client(nume="SC InnovateCorp SA", cui="RO55443322", adresa="Bd. Inovației nr. 15", oras="Brașov", judet="Brașov", telefon="0745678902", email="contact@innovate.ro"),
        Client(nume="SC SmartDesign SRL", cui="RO98765432", adresa="Piața Unirii nr. 7", oras="Iași", judet="Iași", telefon="0756789012", email="office@smartdesign.ro"),
        Client(nume="SC EcoSystems SA", cui="RO13579246", adresa="Str. Verde nr. 25", oras="Constanța", judet="Constanța", telefon="0767890123", email="contact@ecosystems.ro"),
        Client(nume="SC BuildPro SRL", cui="RO24681357", adresa="Bd. Constructorilor nr. 35", oras="Galați", judet="Galați", telefon="0778901234", email="office@buildpro.ro")
    ]
    db.session.add_all(clienti)
    
    # Add suppliers
    furnizori = [
        Furnizor(nume="SC Furnizor SRL", cui="RO11223344", adresa="Str. Furnizorilor nr. 5", oras="Timișoara", judet="Timiș", telefon="0734567890", email="office@furnizor.ro"),
        Furnizor(nume="SC Distribuție SA", cui="RO44332211", adresa="Str. Distribuției nr. 15", oras="Iași", judet="Iași", telefon="0745678901", email="contact@distributie.ro"),
        Furnizor(nume="SC TechSupplier SRL", cui="RO33445566", adresa="Str. Componentelor nr. 12", oras="București", judet="București", telefon="0756789013", email="office@techsupplier.ro"),
        Furnizor(nume="SC OfficeDepot SA", cui="RO66554433", adresa="Bd. Birotică nr. 22", oras="Cluj-Napoca", judet="Cluj", telefon="0767890124", email="contact@officedepot.ro"),
        Furnizor(nume="SC SoftwareSolutions SRL", cui="RO11335577", adresa="Str. Digitală nr. 50", oras="Brașov", judet="Brașov", telefon="0778901235", email="office@softwaresolutions.ro")
    ]
    db.session.add_all(furnizori)
    
    # Commit to get IDs for relationships
    db.session.commit()
    
    # Add products
    produse = [
        Produs(cod="P001", nume="Laptop Business", descriere="Laptop performant pentru mediul business", pret_achizitie=2000, pret_vanzare=2500, stoc=15, categorie_id=1, furnizor_id=1),
        Produs(cod="P002", nume="Scaun ergonomic", descriere="Scaun ergonomic pentru birou", pret_achizitie=300, pret_vanzare=450, stoc=20, categorie_id=2, furnizor_id=2),
        Produs(cod="P003", nume="Set pixuri premium", descriere="Set de 10 pixuri colorate premium", pret_achizitie=15, pret_vanzare=25, stoc=100, categorie_id=3, furnizor_id=1),
        Produs(cod="P004", nume="Monitor 27\"", descriere="Monitor 27 inch 4K pentru profesioniști", pret_achizitie=1200, pret_vanzare=1550, stoc=8, categorie_id=1, furnizor_id=3),
        Produs(cod="P005", nume="Birou ajustabil", descriere="Birou cu înălțime ajustabilă electric", pret_achizitie=1500, pret_vanzare=1900, stoc=5, categorie_id=2, furnizor_id=4),
        Produs(cod="P006", nume="Imprimantă laser", descriere="Imprimantă laser color multifuncțională", pret_achizitie=800, pret_vanzare=1100, stoc=10, categorie_id=1, furnizor_id=3),
        Produs(cod="P007", nume="Licență Windows 11 Pro", descriere="Licență Windows 11 Pro pentru business", pret_achizitie=550, pret_vanzare=650, stoc=25, categorie_id=5, furnizor_id=5),
        Produs(cod="P008", nume="Pachet Microsoft 365", descriere="Pachet Microsoft 365 Business - licență anuală", pret_achizitie=400, pret_vanzare=499, stoc=30, categorie_id=5, furnizor_id=5),
        Produs(cod="P009", nume="Router Wireless", descriere="Router wireless pentru rețele de business", pret_achizitie=180, pret_vanzare=250, stoc=12, categorie_id=4, furnizor_id=3),
        Produs(cod="P010", nume="Telefon mobil business", descriere="Smartphone pentru mediul de business", pret_achizitie=1800, pret_vanzare=2200, stoc=7, categorie_id=1, furnizor_id=1),
        Produs(cod="P011", nume="Cărți de vizită", descriere="Set 100 buc cărți de vizită personalizate", pret_achizitie=30, pret_vanzare=60, stoc=50, categorie_id=6, furnizor_id=4),
        Produs(cod="P012", nume="Broșuri prezentare", descriere="Broșuri prezentare firmă, tipar premium", pret_achizitie=120, pret_vanzare=200, stoc=100, categorie_id=6, furnizor_id=4)
    ]
    db.session.add_all(produse)
    
    # Create some invoices and stock movements
    from datetime import datetime, timedelta
    
    # Facturi pentru clienți
    facturi = []
    
    # Factura 1
    factura1 = Factura(
        serie="FAC", 
        numar=1,
        data_emitere=datetime.now() - timedelta(days=25),
        data_scadenta=datetime.now() - timedelta(days=10),
        valoare_totala=3050,
        valoare_tva=579.5,
        achitata=True,
        client_id=1,
        metoda_plata="Transfer bancar",
        observatii="Prima factură test"
    )
    facturi.append(factura1)
    
    # Factura 2
    factura2 = Factura(
        serie="FAC", 
        numar=2,
        data_emitere=datetime.now() - timedelta(days=20),
        data_scadenta=datetime.now() - timedelta(days=5),
        valoare_totala=1900,
        valoare_tva=361,
        achitata=True,
        client_id=2,
        metoda_plata="Card",
        observatii="A doua factură test"
    )
    facturi.append(factura2)
    
    # Factura 3
    factura3 = Factura(
        serie="FAC", 
        numar=3,
        data_emitere=datetime.now() - timedelta(days=15),
        data_scadenta=datetime.now() + timedelta(days=15),
        valoare_totala=2750,
        valoare_tva=522.5,
        achitata=False,
        client_id=3,
        metoda_plata="Transfer bancar",
        observatii="Factură neachitată"
    )
    facturi.append(factura3)
    
    # Factura 4
    factura4 = Factura(
        serie="FAC", 
        numar=4,
        data_emitere=datetime.now() - timedelta(days=10),
        data_scadenta=datetime.now() + timedelta(days=20),
        valoare_totala=4250,
        valoare_tva=807.5,
        achitata=False,
        client_id=4,
        metoda_plata="Transfer bancar",
        observatii="Factură parțial completă"
    )
    facturi.append(factura4)
    
    # Factura 5
    factura5 = Factura(
        serie="FAC", 
        numar=5,
        data_emitere=datetime.now() - timedelta(days=5),
        data_scadenta=datetime.now() + timedelta(days=25),
        valoare_totala=650,
        valoare_tva=123.5,
        achitata=False,
        client_id=5,
        metoda_plata="Numerar",
        observatii="Factură pentru licență"
    )
    facturi.append(factura5)
    
    db.session.add_all(facturi)
    db.session.commit()
    
    # Add invoice details
    detalii_facturi = [
        DetaliiFactura(factura_id=1, produs_id=1, cantitate=1, pret_unitar=2500, valoare=2500, tva=19, valoare_tva=475),
        DetaliiFactura(factura_id=1, produs_id=3, cantitate=2, pret_unitar=25, valoare=50, tva=19, valoare_tva=9.5),
        DetaliiFactura(factura_id=1, cantitate=5, produs_id=11, pret_unitar=60, valoare=300, tva=19, valoare_tva=57),
        DetaliiFactura(factura_id=2, produs_id=2, cantitate=1, pret_unitar=450, valoare=450, tva=19, valoare_tva=85.5),
        DetaliiFactura(factura_id=2, produs_id=8, cantitate=3, pret_unitar=499, valoare=1497, tva=19, valoare_tva=284.5),
        DetaliiFactura(factura_id=3, produs_id=4, cantitate=1, pret_unitar=1550, valoare=1550, tva=19, valoare_tva=294.5),
        DetaliiFactura(factura_id=3, produs_id=9, cantitate=2, pret_unitar=250, valoare=500, tva=19, valoare_tva=95),
        DetaliiFactura(factura_id=3, produs_id=12, cantitate=3, pret_unitar=200, valoare=600, tva=19, valoare_tva=114),
        DetaliiFactura(factura_id=4, produs_id=5, cantitate=1, pret_unitar=1900, valoare=1900, tva=19, valoare_tva=361),
        DetaliiFactura(factura_id=4, produs_id=6, cantitate=1, pret_unitar=1100, valoare=1100, tva=19, valoare_tva=209),
        DetaliiFactura(factura_id=4, produs_id=10, cantitate=1, pret_unitar=2200, valoare=2200, tva=19, valoare_tva=418),
        DetaliiFactura(factura_id=5, produs_id=7, cantitate=1, pret_unitar=650, valoare=650, tva=19, valoare_tva=123.5)
    ]
    db.session.add_all(detalii_facturi)
    
    # Create stock movements
    miscari_stoc = [
        MiscareStoc(produs_id=1, cantitate=-1, tip="iesire", data=datetime.now() - timedelta(days=25), factura_id=1, motiv="Vânzare factură FAC1"),
        MiscareStoc(produs_id=3, cantitate=-2, tip="iesire", data=datetime.now() - timedelta(days=25), factura_id=1, motiv="Vânzare factură FAC1"),
        MiscareStoc(produs_id=11, cantitate=-5, tip="iesire", data=datetime.now() - timedelta(days=25), factura_id=1, motiv="Vânzare factură FAC1"),
        MiscareStoc(produs_id=2, cantitate=-1, tip="iesire", data=datetime.now() - timedelta(days=20), factura_id=2, motiv="Vânzare factură FAC2"),
        MiscareStoc(produs_id=8, cantitate=-3, tip="iesire", data=datetime.now() - timedelta(days=20), factura_id=2, motiv="Vânzare factură FAC2"),
        MiscareStoc(produs_id=4, cantitate=-1, tip="iesire", data=datetime.now() - timedelta(days=15), factura_id=3, motiv="Vânzare factură FAC3"),
        MiscareStoc(produs_id=9, cantitate=-2, tip="iesire", data=datetime.now() - timedelta(days=15), factura_id=3, motiv="Vânzare factură FAC3"),
        MiscareStoc(produs_id=12, cantitate=-3, tip="iesire", data=datetime.now() - timedelta(days=15), factura_id=3, motiv="Vânzare factură FAC3"),
        MiscareStoc(produs_id=5, cantitate=-1, tip="iesire", data=datetime.now() - timedelta(days=10), factura_id=4, motiv="Vânzare factură FAC4"),
        MiscareStoc(produs_id=6, cantitate=-1, tip="iesire", data=datetime.now() - timedelta(days=10), factura_id=4, motiv="Vânzare factură FAC4"),
        MiscareStoc(produs_id=10, cantitate=-1, tip="iesire", data=datetime.now() - timedelta(days=10), factura_id=4, motiv="Vânzare factură FAC4"),
        MiscareStoc(produs_id=7, cantitate=-1, tip="iesire", data=datetime.now() - timedelta(days=5), factura_id=5, motiv="Vânzare factură FAC5"),
        
        # Intrări în stoc
        MiscareStoc(produs_id=1, cantitate=5, tip="intrare", data=datetime.now() - timedelta(days=40), motiv="Aprovizionare inițială"),
        MiscareStoc(produs_id=2, cantitate=10, tip="intrare", data=datetime.now() - timedelta(days=40), motiv="Aprovizionare inițială"),
        MiscareStoc(produs_id=3, cantitate=50, tip="intrare", data=datetime.now() - timedelta(days=40), motiv="Aprovizionare inițială"),
        MiscareStoc(produs_id=1, cantitate=10, tip="intrare", data=datetime.now() - timedelta(days=30), motiv="Reaprovizionare"),
        MiscareStoc(produs_id=4, cantitate=8, tip="intrare", data=datetime.now() - timedelta(days=30), motiv="Aprovizionare inițială"),
        MiscareStoc(produs_id=5, cantitate=5, tip="intrare", data=datetime.now() - timedelta(days=30), motiv="Aprovizionare inițială"),
        MiscareStoc(produs_id=6, cantitate=10, tip="intrare", data=datetime.now() - timedelta(days=30), motiv="Aprovizionare inițială"),
        MiscareStoc(produs_id=7, cantitate=25, tip="intrare", data=datetime.now() - timedelta(days=30), motiv="Aprovizionare inițială"),
        MiscareStoc(produs_id=8, cantitate=30, tip="intrare", data=datetime.now() - timedelta(days=30), motiv="Aprovizionare inițială"),
        MiscareStoc(produs_id=9, cantitate=12, tip="intrare", data=datetime.now() - timedelta(days=30), motiv="Aprovizionare inițială"),
        MiscareStoc(produs_id=10, cantitate=7, tip="intrare", data=datetime.now() - timedelta(days=30), motiv="Aprovizionare inițială"),
        MiscareStoc(produs_id=11, cantitate=50, tip="intrare", data=datetime.now() - timedelta(days=30), motiv="Aprovizionare inițială"),
        MiscareStoc(produs_id=12, cantitate=100, tip="intrare", data=datetime.now() - timedelta(days=30), motiv="Aprovizionare inițială"),
        MiscareStoc(produs_id=2, cantitate=10, tip="intrare", data=datetime.now() - timedelta(days=5), motiv="Reaprovizionare"),
        MiscareStoc(produs_id=3, cantitate=50, tip="intrare", data=datetime.now() - timedelta(days=5), motiv="Reaprovizionare"),
        
        # Ajustări
        MiscareStoc(produs_id=4, cantitate=1, tip="ajustare", data=datetime.now() - timedelta(days=7), motiv="Inventar - produse găsite")
    ]
    db.session.add_all(miscari_stoc)
    
    # Facturi de la furnizori
    facturi_primite = [
        FacturaPrimita(
            serie="FF", 
            numar="2023001",
            data_emitere=datetime.now() - timedelta(days=45),
            data_scadenta=datetime.now() - timedelta(days=15),
            valoare_totala=15000,
            valoare_tva=2850,
            achitata=True,
            furnizor_id=1,
            metoda_plata="Transfer bancar",
            observatii="Factura materiale electronice"
        ),
        FacturaPrimita(
            serie="FF", 
            numar="2023002",
            data_emitere=datetime.now() - timedelta(days=40),
            data_scadenta=datetime.now() - timedelta(days=10),
            valoare_totala=7500,
            valoare_tva=1425,
            achitata=True,
            furnizor_id=2,
            metoda_plata="Transfer bancar",
            observatii="Factura mobilier"
        ),
        FacturaPrimita(
            serie="FF", 
            numar="2023003",
            data_emitere=datetime.now() - timedelta(days=35),
            data_scadenta=datetime.now() - timedelta(days=5),
            valoare_totala=12000,
            valoare_tva=2280,
            achitata=True,
            furnizor_id=3,
            metoda_plata="Transfer bancar",
            observatii="Factura echipamente IT"
        ),
        FacturaPrimita(
            serie="FF", 
            numar="2023004",
            data_emitere=datetime.now() - timedelta(days=20),
            data_scadenta=datetime.now() + timedelta(days=10),
            valoare_totala=8500,
            valoare_tva=1615,
            achitata=False,
            furnizor_id=4,
            metoda_plata="Transfer bancar",
            observatii="Factura birotică și papetărie"
        ),
        FacturaPrimita(
            serie="FF", 
            numar="2023005",
            data_emitere=datetime.now() - timedelta(days=10),
            data_scadenta=datetime.now() + timedelta(days=20),
            valoare_totala=25000,
            valoare_tva=4750,
            achitata=False,
            furnizor_id=5,
            metoda_plata="Transfer bancar",
            observatii="Factura licențe software anuale"
        )
    ]
    db.session.add_all(facturi_primite)
    
    db.session.commit()
    print("Sample data added successfully!")

if __name__ == "__main__":
    cli()