from flask import Blueprint, render_template, request
from app.models import Factura, FacturaPrimita, Client, Furnizor, Produs
from sqlalchemy import func
import datetime

bp = Blueprint('rapoarte', __name__, url_prefix='/rapoarte')

@bp.route('/')
def index():
    return render_template('rapoarte/index.html')

@bp.route('/vanzari')
def vanzari():
    start_date = request.args.get('start_date', (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.datetime.now().strftime('%Y-%m-%d'))
    
    facturi = Factura.query.filter(
        Factura.data_emitere.between(start_date, end_date)
    ).order_by(Factura.data_emitere).all()
    
    total = sum(factura.valoare_totala for factura in facturi)
    total_tva = sum(factura.valoare_tva for factura in facturi)
    
    return render_template('rapoarte/vanzari.html', 
                           facturi=facturi, 
                           total=total, 
                           total_tva=total_tva,
                           start_date=start_date,
                           end_date=end_date)

@bp.route('/cheltuieli')
def cheltuieli():
    start_date = request.args.get('start_date', (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.datetime.now().strftime('%Y-%m-%d'))
    
    facturi = FacturaPrimita.query.filter(
        FacturaPrimita.data_emitere.between(start_date, end_date)
    ).order_by(FacturaPrimita.data_emitere).all()
    
    total = sum(factura.valoare_totala for factura in facturi)
    total_tva = sum(factura.valoare_tva for factura in facturi)
    
    return render_template('rapoarte/cheltuieli.html', 
                           facturi=facturi, 
                           total=total, 
                           total_tva=total_tva,
                           start_date=start_date,
                           end_date=end_date)

@bp.route('/stocuri')
def stocuri():
    produse = Produs.query.order_by(Produs.nume).all()
    valoare_totala = sum(produs.stoc * produs.pret_achizitie for produs in produse)
    
    return render_template('rapoarte/stocuri.html', 
                           produse=produse, 
                           valoare_totala=valoare_totala)

@bp.route('/clienti')
def clienti():
    clienti = Client.query.all()
    facturi_neachitate = {}
    
    for client in clienti:
        facturi = Factura.query.filter_by(client_id=client.id, achitata=False).all()
        suma_neachitata = sum(factura.valoare_totala for factura in facturi)
        facturi_neachitate[client.id] = suma_neachitata
    
    return render_template('rapoarte/clienti.html', 
                           clienti=clienti, 
                           facturi_neachitate=facturi_neachitate)

@bp.route('/furnizori')
def furnizori():
    furnizori = Furnizor.query.all()
    facturi_neachitate = {}
    
    for furnizor in furnizori:
        facturi = FacturaPrimita.query.filter_by(furnizor_id=furnizor.id, achitata=False).all()
        suma_neachitata = sum(factura.valoare_totala for factura in facturi)
        facturi_neachitate[furnizor.id] = suma_neachitata
    
    return render_template('rapoarte/furnizori.html', 
                           furnizori=furnizori, 
                           facturi_neachitate=facturi_neachitate)
