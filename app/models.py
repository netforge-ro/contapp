from app import db
from datetime import datetime

class Client(db.Model):
    __tablename__ = 'clienti'
    
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100), nullable=False)
    cui = db.Column(db.String(20), unique=True)
    adresa = db.Column(db.String(255))
    oras = db.Column(db.String(100))
    judet = db.Column(db.String(100))
    telefon = db.Column(db.String(20))
    email = db.Column(db.String(100))
    data_adaugare = db.Column(db.DateTime, default=datetime.utcnow)
    activ = db.Column(db.Boolean, default=True)
    
    facturi = db.relationship('Factura', backref='client', lazy=True)
    
    def __repr__(self):
        return f'<Client {self.nume}>'

class Furnizor(db.Model):
    __tablename__ = 'furnizori'
    
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100), nullable=False)
    cui = db.Column(db.String(20), unique=True)
    adresa = db.Column(db.String(255))
    oras = db.Column(db.String(100))
    judet = db.Column(db.String(100))
    telefon = db.Column(db.String(20))
    email = db.Column(db.String(100))
    data_adaugare = db.Column(db.DateTime, default=datetime.utcnow)
    activ = db.Column(db.Boolean, default=True)
    
    facturi_primite = db.relationship('FacturaPrimita', backref='furnizor', lazy=True)
    produse = db.relationship('Produs', backref='furnizor', lazy=True)
    
    def __repr__(self):
        return f'<Furnizor {self.nume}>'

class CategorieProdusCheltuiala(db.Model):
    __tablename__ = 'categorii_produse_cheltuieli'
    
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100), nullable=False)
    descriere = db.Column(db.Text)
    
    produse = db.relationship('Produs', backref='categorie', lazy=True)
    
    def __repr__(self):
        return f'<Categorie {self.nume}>'

class Produs(db.Model):
    __tablename__ = 'produse'
    
    id = db.Column(db.Integer, primary_key=True)
    cod = db.Column(db.String(20), unique=True)
    nume = db.Column(db.String(100), nullable=False)
    descriere = db.Column(db.Text)
    pret_achizitie = db.Column(db.Numeric(10, 2), nullable=False)
    pret_vanzare = db.Column(db.Numeric(10, 2), nullable=False)
    stoc = db.Column(db.Integer, default=0)
    unitate_masura = db.Column(db.String(20), default='buc')
    tva = db.Column(db.Integer, default=19)
    data_adaugare = db.Column(db.DateTime, default=datetime.utcnow)
    activ = db.Column(db.Boolean, default=True)
    
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorii_produse_cheltuieli.id'))
    furnizor_id = db.Column(db.Integer, db.ForeignKey('furnizori.id'))
    
    detalii_facturi = db.relationship('DetaliiFactura', backref='produs', lazy=True)
    
    def __repr__(self):
        return f'<Produs {self.nume}>'

class Factura(db.Model):
    __tablename__ = 'facturi'
    
    id = db.Column(db.Integer, primary_key=True)
    serie = db.Column(db.String(10), nullable=False)
    numar = db.Column(db.Integer, nullable=False)
    data_emitere = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    data_scadenta = db.Column(db.Date, nullable=False)
    valoare_totala = db.Column(db.Numeric(10, 2), nullable=False)
    valoare_tva = db.Column(db.Numeric(10, 2), nullable=False)
    achitata = db.Column(db.Boolean, default=False)
    metoda_plata = db.Column(db.String(50), default='Transfer bancar')
    observatii = db.Column(db.Text)
    
    client_id = db.Column(db.Integer, db.ForeignKey('clienti.id'), nullable=False)
    
    detalii = db.relationship('DetaliiFactura', backref='factura', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.UniqueConstraint('serie', 'numar', name='uix_serie_numar'),
    )
    
    def __repr__(self):
        return f'<Factura {self.serie}{self.numar}>'

class DetaliiFactura(db.Model):
    __tablename__ = 'detalii_facturi'
    
    id = db.Column(db.Integer, primary_key=True)
    cantitate = db.Column(db.Integer, nullable=False)
    pret_unitar = db.Column(db.Numeric(10, 2), nullable=False)
    valoare = db.Column(db.Numeric(10, 2), nullable=False)
    tva = db.Column(db.Integer, default=19)
    valoare_tva = db.Column(db.Numeric(10, 2), nullable=False)
    
    factura_id = db.Column(db.Integer, db.ForeignKey('facturi.id'), nullable=False)
    produs_id = db.Column(db.Integer, db.ForeignKey('produse.id'), nullable=False)
    
    def __repr__(self):
        return f'<DetaliiFactura {self.id}>'

class FacturaPrimita(db.Model):
    __tablename__ = 'facturi_primite'
    
    id = db.Column(db.Integer, primary_key=True)
    serie = db.Column(db.String(10), nullable=False)
    numar = db.Column(db.String(20), nullable=False)
    data_emitere = db.Column(db.Date, nullable=False)
    data_scadenta = db.Column(db.Date, nullable=False)
    valoare_totala = db.Column(db.Numeric(10, 2), nullable=False)
    valoare_tva = db.Column(db.Numeric(10, 2), nullable=False)
    achitata = db.Column(db.Boolean, default=False)
    metoda_plata = db.Column(db.String(50), default='Transfer bancar')
    observatii = db.Column(db.Text)
    
    furnizor_id = db.Column(db.Integer, db.ForeignKey('furnizori.id'), nullable=False)
    
    def __repr__(self):
        return f'<FacturaPrimita {self.serie}{self.numar}>'

class MiscareStoc(db.Model):
    __tablename__ = 'miscari_stoc'
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tip = db.Column(db.String(20), nullable=False)  # intrare, iesire, ajustare
    cantitate = db.Column(db.Integer, nullable=False)
    motiv = db.Column(db.String(255))
    
    produs_id = db.Column(db.Integer, db.ForeignKey('produse.id'), nullable=False)
    factura_id = db.Column(db.Integer, db.ForeignKey('facturi.id'))
    factura_primita_id = db.Column(db.Integer, db.ForeignKey('facturi_primite.id'))
    
    produs = db.relationship('Produs')
    
    def __repr__(self):
        return f'<MiscareStoc {self.tip} {self.cantitate} {self.produs.nume}>'