from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Factura, DetaliiFactura, Client, Produs
from app import db
from datetime import datetime, timedelta

bp = Blueprint('facturi', __name__, url_prefix='/facturi')

@bp.route('/')
def index():
    facturi = Factura.query.order_by(Factura.data_emitere.desc()).all()
    return render_template('facturi/index.html', facturi=facturi)

@bp.route('/adauga', methods=['GET', 'POST'])
def adauga():
    if request.method == 'POST':
        # Process form data here
        pass
    
    clienti = Client.query.filter_by(activ=True).all()
    produse = Produs.query.filter_by(activ=True).all()
    
    return render_template('facturi/adauga.html', clienti=clienti, produse=produse)

@bp.route('/<int:id>')
def vezi(id):
    factura = Factura.query.get_or_404(id)
    return render_template('facturi/vezi.html', factura=factura)

@bp.route('/<int:id>/editeaza', methods=['GET', 'POST'])
def editeaza(id):
    factura = Factura.query.get_or_404(id)
    
    if request.method == 'POST':
        # Process form data here
        pass
    
    clienti = Client.query.filter_by(activ=True).all()
    produse = Produs.query.filter_by(activ=True).all()
    
    return render_template('facturi/editeaza.html', factura=factura, clienti=clienti, produse=produse)

@bp.route('/<int:id>/sterge', methods=['POST'])
def sterge(id):
    factura = Factura.query.get_or_404(id)
    
    # Delete factura
    db.session.delete(factura)
    db.session.commit()
    
    flash('Factura a fost ștearsă cu succes!', 'success')
    return redirect(url_for('facturi.index'))
