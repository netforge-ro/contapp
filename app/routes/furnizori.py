from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Furnizor, FacturaPrimita
from app import db

bp = Blueprint('furnizori', __name__, url_prefix='/furnizori')

@bp.route('/')
def index():
    furnizori = Furnizor.query.order_by(Furnizor.nume).all()
    return render_template('furnizori/index.html', furnizori=furnizori)

@bp.route('/adauga', methods=['GET', 'POST'])
def adauga():
    if request.method == 'POST':
        # Process form data here
        pass
    
    return render_template('furnizori/adauga.html')

@bp.route('/<int:id>')
def vezi(id):
    furnizor = Furnizor.query.get_or_404(id)
    facturi = FacturaPrimita.query.filter_by(furnizor_id=furnizor.id).order_by(FacturaPrimita.data_emitere.desc()).all()
    return render_template('furnizori/vezi.html', furnizor=furnizor, facturi=facturi)

@bp.route('/<int:id>/editeaza', methods=['GET', 'POST'])
def editeaza(id):
    furnizor = Furnizor.query.get_or_404(id)
    
    if request.method == 'POST':
        # Process form data here
        pass
    
    return render_template('furnizori/editeaza.html', furnizor=furnizor)

@bp.route('/<int:id>/sterge', methods=['POST'])
def sterge(id):
    furnizor = Furnizor.query.get_or_404(id)
    
    # Delete furnizor
    db.session.delete(furnizor)
    db.session.commit()
    
    flash('Furnizorul a fost șters cu succes!', 'success')
    return redirect(url_for('furnizori.index'))
