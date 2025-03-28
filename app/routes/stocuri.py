from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Produs, MiscareStoc, CategorieProdusCheltuiala, Furnizor
from app import db

bp = Blueprint('stocuri', __name__, url_prefix='/stocuri')

@bp.route('/')
def index():
    produse = Produs.query.order_by(Produs.nume).all()
    return render_template('stocuri/index.html', produse=produse)

@bp.route('/adauga', methods=['GET', 'POST'])
def adauga():
    if request.method == 'POST':
        # Process form data here
        pass
    
    categorii = CategorieProdusCheltuiala.query.all()
    furnizori = Furnizor.query.filter_by(activ=True).all()
    
    return render_template('stocuri/adauga.html', categorii=categorii, furnizori=furnizori)

@bp.route('/<int:id>')
def vezi(id):
    produs = Produs.query.get_or_404(id)
    miscari = MiscareStoc.query.filter_by(produs_id=produs.id).order_by(MiscareStoc.data.desc()).all()
    return render_template('stocuri/vezi.html', produs=produs, miscari=miscari)

@bp.route('/<int:id>/editeaza', methods=['GET', 'POST'])
def editeaza(id):
    produs = Produs.query.get_or_404(id)
    
    if request.method == 'POST':
        # Process form data here
        pass
    
    categorii = CategorieProdusCheltuiala.query.all()
    furnizori = Furnizor.query.filter_by(activ=True).all()
    
    return render_template('stocuri/editeaza.html', produs=produs, categorii=categorii, furnizori=furnizori)

@bp.route('/categorii')
def categorii():
    categorii = CategorieProdusCheltuiala.query.all()
    return render_template('stocuri/categorii.html', categorii=categorii)

@bp.route('/ajustare', methods=['GET', 'POST'])
def ajustare():
    if request.method == 'POST':
        # Process form data here
        pass
    
    produse = Produs.query.filter_by(activ=True).all()
    return render_template('stocuri/ajustare.html', produse=produse)
