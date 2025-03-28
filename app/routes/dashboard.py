from flask import Blueprint, render_template
from app.models import Factura, FacturaPrimita, Client, Furnizor, Produs
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    # Calculare venituri și cheltuieli lunare
    current_date = datetime.now()
    first_day_of_month = datetime(current_date.year, current_date.month, 1)
    last_day_of_month = first_day_of_month + timedelta(days=32)
    last_day_of_month = datetime(last_day_of_month.year, last_day_of_month.month, 1) - timedelta(days=1)
    
    # Venituri luna curentă
    venituri_luna = db.session.query(func.sum(Factura.valoare_totala)).filter(
        Factura.data_emitere.between(first_day_of_month, last_day_of_month)
    ).scalar() or 0
    
    # Cheltuieli luna curentă
    cheltuieli_luna = db.session.query(func.sum(FacturaPrimita.valoare_totala)).filter(
        FacturaPrimita.data_emitere.between(first_day_of_month, last_day_of_month)
    ).scalar() or 0
    
    # Profit luna curentă
    profit_luna = venituri_luna - cheltuieli_luna
    
    # Clienți cu facturi neachitate
    facturi_neachitate = Factura.query.filter_by(achitata=False).count()
    suma_facturi_neachitate = db.session.query(func.sum(Factura.valoare_totala)).filter(
        Factura.achitata == False
    ).scalar() or 0
    
    # Facturi către furnizori neachitate
    facturi_furnizori_neachitate = FacturaPrimita.query.filter_by(achitata=False).count()
    suma_facturi_furnizori_neachitate = db.session.query(func.sum(FacturaPrimita.valoare_totala)).filter(
        FacturaPrimita.achitata == False
    ).scalar() or 0
    
    # Produse cu stoc redus
    produse_stoc_redus = Produs.query.filter(Produs.stoc < 10).count()
    
    # Date pentru grafic - ultimele 6 luni
    labels = []
    venituri_data = []
    cheltuieli_data = []
    profit_data = []
    
    for i in range(5, -1, -1):
        date = current_date - timedelta(days=30*i)
        first_day = datetime(date.year, date.month, 1)
        next_month = first_day + timedelta(days=32)
        last_day = datetime(next_month.year, next_month.month, 1) - timedelta(days=1)
        
        labels.append(first_day.strftime('%b %Y'))
        
        venituri = db.session.query(func.sum(Factura.valoare_totala)).filter(
            Factura.data_emitere.between(first_day, last_day)
        ).scalar() or 0
        venituri_data.append(float(venituri))
        
        cheltuieli = db.session.query(func.sum(FacturaPrimita.valoare_totala)).filter(
            FacturaPrimita.data_emitere.between(first_day, last_day)
        ).scalar() or 0
        cheltuieli_data.append(float(cheltuieli))
        
        profit_data.append(float(venituri) - float(cheltuieli))
    
    return render_template('dashboard/index.html',
                           venituri_luna=venituri_luna,
                           cheltuieli_luna=cheltuieli_luna,
                           profit_luna=profit_luna,
                           facturi_neachitate=facturi_neachitate,
                           suma_facturi_neachitate=suma_facturi_neachitate,
                           facturi_furnizori_neachitate=facturi_furnizori_neachitate,
                           suma_facturi_furnizori_neachitate=suma_facturi_furnizori_neachitate,
                           produse_stoc_redus=produse_stoc_redus,
                           labels=labels,
                           venituri_data=venituri_data,
                           cheltuieli_data=cheltuieli_data,
                           profit_data=profit_data)
