from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Client, Factura
from app import db

bp = Blueprint('clienti', __name__, url_prefix='/clienti')

@bp.route('/')
def index():
    clienti = Client.query.order_by(Client.nume).all()
    return render_template('clienti/index.html', clienti=clienti)

@bp.route('/adauga', methods=['GET', 'POST'])
def adauga():
    if request.method == 'POST':
        # Process form data here
        pass
    
    return render_template('clienti/adauga.html')

@bp.route('/<int:id>')
def vezi(id):
    client = Client.query.get_or_404(id)
    facturi = Factura.query.filter_by(client_id=client.id).order_by(Factura.data_emitere.desc()).all()
    return render_template('clienti/vezi.html', client=client, facturi=facturi)

@bp.route('/<int:id>/editeaza', methods=['GET', 'POST'])
def editeaza(id):
    client = Client.query.get_or_404(id)
    
    if request.method == 'POST':
        # Process form data here
        pass
    
    return render_template('clienti/editeaza.html', client=client)

@bp.route('/<int:id>/sterge', methods=['POST'])
def sterge(id):
    client = Client.query.get_or_404(id)
    
    # Delete client
    db.session.delete(client)
    db.session.commit()
    
    flash('Clientul a fost șters cu succes!', 'success')
    return redirect(url_for('clienti.index'))
