from app import db
from datetime import datetime

class Furnizor(db.Model):
    __tablename__ = 'furnizori'
    
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100), nullable=False)
    cui = db.Column(db.String(20), unique=True)
    adresa = db.Column(db.String(255))
    telefon = db.Column(db.String(20))
    cod_fiscal = db.Column(db.String(20))
    cont_bancar = db.Column(db.String(50))
    sold_furnizor = db.Column(db.Numeric(10, 2), default=0)
    data_adaugare = db.Column(db.DateTime, default=datetime.utcnow)
    activ = db.Column(db.Boolean, default=True)
    
    facturi = db.relationship('Factura', backref='furnizor', lazy=True)
    comenzi = db.relationship('Comanda', backref='furnizor', lazy=True)
    
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

class Comanda(db.Model):
    __tablename__ = 'comenzi'
    
    id = db.Column(db.Integer, primary_key=True)
    data_comanda = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    data_livrare = db.Column(db.Date, nullable=True)
    stare_comanda = db.Column(db.String(50), default='Nouă')
    observatii = db.Column(db.Text)
    
    furnizor_id = db.Column(db.Integer, db.ForeignKey('furnizori.id'), nullable=False)
    
    plati = db.relationship('Plata', backref='comanda', lazy=True)
    produse_comandate = db.relationship('ProduseComandate', backref='comanda', lazy=True)
    miscari_stoc = db.relationship('MiscareStoc', backref='comanda', lazy=True)
    
    def __repr__(self):
        return f'<Comanda {self.id} - {self.data_comanda}>'

class Produs(db.Model):
    __tablename__ = 'produse'
    
    id = db.Column(db.Integer, primary_key=True)
    cod = db.Column(db.String(20), unique=True)
    nume = db.Column(db.String(100), nullable=False)
    unitate_masura = db.Column(db.String(20), default='buc')
    pret = db.Column(db.Numeric(10, 2), nullable=False)
    stoc = db.Column(db.Integer, default=0)
    cod_comanda = db.Column(db.Integer, db.ForeignKey('comenzi.id'), nullable=True)
    data_adaugare = db.Column(db.DateTime, default=datetime.utcnow)
    activ = db.Column(db.Boolean, default=True)
    
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorii_produse_cheltuieli.id'))
    
    detalii_facturi = db.relationship('DetaliiFactura', backref='produs', lazy=True)
    stocuri = db.relationship('Stoc', backref='produs', lazy=True)
    produse_comandate = db.relationship('ProduseComandate', backref='produs', lazy=True)
    miscari_stoc = db.relationship('MiscareStoc', backref='produs', lazy=True)
    
    def __repr__(self):
        return f'<Produs {self.nume}>'

class Factura(db.Model):
    __tablename__ = 'facturi'
    
    id = db.Column(db.Integer, primary_key=True)
    data_factura = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    serie_factura = db.Column(db.String(10), nullable=False)
    nr_factura = db.Column(db.Integer, nullable=False)
    data_scadenta = db.Column(db.Date, nullable=False)
    valoare = db.Column(db.Numeric(10, 2), nullable=False)
    modalitate_plata = db.Column(db.String(50), default='Transfer bancar')
    observatii = db.Column(db.Text)
    
    furnizor_id = db.Column(db.Integer, db.ForeignKey('furnizori.id'), nullable=False)
    
    detalii = db.relationship('DetaliiFactura', backref='factura', lazy=True, cascade='all, delete-orphan')
    miscari_stoc = db.relationship('MiscareStoc', backref='factura', lazy=True)
    
    __table_args__ = (
        db.UniqueConstraint('serie_factura', 'nr_factura', name='uix_serie_numar'),
    )
    
    def __repr__(self):
        return f'<Factura {self.serie_factura}{self.nr_factura}>'

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


class Plata(db.Model):
    __tablename__ = 'plati'
    
    id = db.Column(db.Integer, primary_key=True)
    data_platii = db.Column(db.Date, nullable=False)
    valoare = db.Column(db.Numeric(10, 2), nullable=False)
    modalitate_plata = db.Column(db.String(50), default='Transfer bancar')
    observatii = db.Column(db.Text)
    
    comanda_id = db.Column(db.Integer, db.ForeignKey('comenzi.id'), nullable=False)
    
    def __repr__(self):
        return f'<Plata {self.id} - {self.valoare}>'

class Depozit(db.Model):
    __tablename__ = 'depozite'
    
    id = db.Column(db.Integer, primary_key=True)
    nume_depozit = db.Column(db.String(100), nullable=False)
    adresa = db.Column(db.String(255))
    observatii = db.Column(db.Text)
    
    stocuri = db.relationship('Stoc', backref='depozit', lazy=True)
    
    def __repr__(self):
        return f'<Depozit {self.nume_depozit}>'

class Stoc(db.Model):
    __tablename__ = 'stocuri'
    
    id = db.Column(db.Integer, primary_key=True)
    depozit_id = db.Column(db.Integer, db.ForeignKey('depozite.id'), nullable=False)
    produs_id = db.Column(db.Integer, db.ForeignKey('produse.id'), nullable=False)
    stoc_curent = db.Column(db.Integer, default=0)
    observatii = db.Column(db.Text)
    
    __table_args__ = (
        db.UniqueConstraint('depozit_id', 'produs_id', name='uix_depozit_produs'),
    )
    
    def __repr__(self):
        return f'<Stoc {self.produs_id} în {self.depozit_id}: {self.stoc_curent}>'

class ProduseComandate(db.Model):
    __tablename__ = 'produse_comandate'
    
    id = db.Column(db.Integer, primary_key=True)
    produs_id = db.Column(db.Integer, db.ForeignKey('produse.id'), nullable=False)
    comanda_id = db.Column(db.Integer, db.ForeignKey('comenzi.id'), nullable=False)
    cantitate_comandata = db.Column(db.Integer, default=0)
    observatii = db.Column(db.Text)
    
    __table_args__ = (
        db.UniqueConstraint('produs_id', 'comanda_id', name='uix_produs_comanda'),
    )
    
    def __repr__(self):
        return f'<ProduseComandate {self.produs_id} în comanda {self.comanda_id}: {self.cantitate_comandata}>'

class MiscareStoc(db.Model):
    __tablename__ = 'miscari_stoc'
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tip = db.Column(db.String(20), nullable=False)  # intrare, iesire, ajustare
    cantitate = db.Column(db.Integer, nullable=False)
    motiv = db.Column(db.String(255))
    
    produs_id = db.Column(db.Integer, db.ForeignKey('produse.id'), nullable=False)
    factura_id = db.Column(db.Integer, db.ForeignKey('facturi.id'), nullable=True)
    comanda_id = db.Column(db.Integer, db.ForeignKey('comenzi.id'), nullable=True)
    
    def __repr__(self):
        return f'<MiscareStoc {self.tip} {self.cantitate} produs_id:{self.produs_id}>'