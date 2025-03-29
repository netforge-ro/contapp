from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Furnizor, FacturaPrimita
from app import db
from datetime import datetime

bp = Blueprint('furnizori', __name__, url_prefix='/furnizori')

@bp.route('/')
def index():
    furnizori = Furnizor.query.order_by(Furnizor.nume).all()
    return render_template('furnizori/index.html', furnizori=furnizori)

@bp.route('/adauga', methods=['GET', 'POST'])
def adauga():
    if request.method == 'POST':
        nume = request.form.get('nume')
        cui = request.form.get('cui')
        cod_fiscal = request.form.get('cod_fiscal')
        adresa = request.form.get('adresa')
        telefon = request.form.get('telefon')
        cont_bancar = request.form.get('cont_bancar')
        sold_furnizor = request.form.get('sold_furnizor')
        activ = True if request.form.get('activ') else False
        
        # Convert sold_furnizor to float if not empty
        sold_furnizor = float(sold_furnizor) if sold_furnizor else 0
        
        furnizor = Furnizor(
            nume=nume,
            cui=cui,
            cod_fiscal=cod_fiscal,
            adresa=adresa,
            telefon=telefon,
            cont_bancar=cont_bancar,
            sold_furnizor=sold_furnizor,
            data_adaugare=datetime.utcnow(),
            activ=activ
        )
        
        db.session.add(furnizor)
        db.session.commit()
        
        flash('Furnizorul a fost adăugat cu succes!', 'success')
        return redirect(url_for('furnizori.index'))
    
    return render_template('furnizori/adauga.html')

@bp.route('/<int:id>')
def vezi(id):
    furnizor = Furnizor.query.get_or_404(id)
    facturi = FacturaPrimita.query.filter_by(furnizor_id=furnizor.id).order_by(FacturaPrimita.data_emitere.desc()).all()
    return render_template('furnizori/vezi.html', furnizor=furnizor, facturi=facturi, now=datetime.utcnow().date())

@bp.route('/<int:id>/editeaza', methods=['GET', 'POST'])
def editeaza(id):
    furnizor = Furnizor.query.get_or_404(id)
    
    if request.method == 'POST':
        furnizor.nume = request.form.get('nume')
        furnizor.cui = request.form.get('cui')
        furnizor.cod_fiscal = request.form.get('cod_fiscal')
        furnizor.adresa = request.form.get('adresa')
        furnizor.telefon = request.form.get('telefon')
        furnizor.cont_bancar = request.form.get('cont_bancar')
        furnizor.sold_furnizor = float(request.form.get('sold_furnizor')) if request.form.get('sold_furnizor') else 0
        furnizor.activ = True if request.form.get('activ') else False
        
        db.session.commit()
        
        flash('Furnizorul a fost actualizat cu succes!', 'success')
        return redirect(url_for('furnizori.index'))
    
    return render_template('furnizori/editeaza.html', furnizor=furnizor)

@bp.route('/<int:id>/sterge', methods=['POST'])
def sterge(id):
    furnizor = Furnizor.query.get_or_404(id)
    
    # Delete furnizor
    db.session.delete(furnizor)
    db.session.commit()
    
    flash('Furnizorul a fost șters cu succes!', 'success')
    return redirect(url_for('furnizori.index'))
