from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Client, Factura
from app import db
from datetime import datetime

bp = Blueprint('clienti', __name__, url_prefix='/clienti')

@bp.route('/')
def index():
    clienti = Client.query.order_by(Client.nume).all()
    return render_template('clienti/index.html', clienti=clienti)

@bp.route('/adauga', methods=['GET', 'POST'])
def adauga():
    if request.method == 'POST':
        nume = request.form.get('nume')
        cui = request.form.get('cui')
        adresa = request.form.get('adresa')
        oras = request.form.get('oras')
        judet = request.form.get('judet')
        telefon = request.form.get('telefon')
        email = request.form.get('email')
        activ = True if request.form.get('activ') else False
        
        client = Client(
            nume=nume,
            cui=cui,
            adresa=adresa,
            oras=oras,
            judet=judet,
            telefon=telefon,
            email=email,
            data_adaugare=datetime.utcnow(),
            activ=activ
        )
        
        db.session.add(client)
        db.session.commit()
        
        flash('Clientul a fost adăugat cu succes!', 'success')
        return redirect(url_for('clienti.index'))
    
    return render_template('clienti/adauga.html')

@bp.route('/<int:id>')
def vezi(id):
    client = Client.query.get_or_404(id)
    facturi = Factura.query.filter_by(client_id=client.id).order_by(Factura.data_emitere.desc()).all()
    return render_template('clienti/vezi.html', client=client, facturi=facturi, now=datetime.utcnow().date())

@bp.route('/<int:id>/editeaza', methods=['GET', 'POST'])
def editeaza(id):
    client = Client.query.get_or_404(id)
    
    if request.method == 'POST':
        client.nume = request.form.get('nume')
        client.cui = request.form.get('cui')
        client.adresa = request.form.get('adresa')
        client.oras = request.form.get('oras')
        client.judet = request.form.get('judet')
        client.telefon = request.form.get('telefon')
        client.email = request.form.get('email')
        client.activ = True if request.form.get('activ') else False
        
        db.session.commit()
        
        flash('Clientul a fost actualizat cu succes!', 'success')
        return redirect(url_for('clienti.index'))
    
    return render_template('clienti/editeaza.html', client=client)

@bp.route('/<int:id>/sterge', methods=['POST'])
def sterge(id):
    client = Client.query.get_or_404(id)
    
    # Delete client
    db.session.delete(client)
    db.session.commit()
    
    flash('Clientul a fost șters cu succes!', 'success')
    return redirect(url_for('clienti.index'))
