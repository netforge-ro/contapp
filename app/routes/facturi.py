from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Factura, DetaliiFactura, Client, Produs, MiscareStoc
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
        # Get the form data - always using the fixed series NET
        serie = "NET"
        # Auto-increment the invoice number
        ultima_factura = Factura.query.filter_by(serie=serie).order_by(Factura.numar.desc()).first()
        if ultima_factura:
            numar = ultima_factura.numar + 1
        else:
            # Start from 6 to account for the previous 5 invoices
            numar = 6
            
        data_emitere = datetime.strptime(request.form.get('data_emitere'), '%Y-%m-%d')
        data_scadenta = datetime.strptime(request.form.get('data_scadenta'), '%Y-%m-%d')
        client_id = request.form.get('client_id')
        metoda_plata = request.form.get('metoda_plata')
        observatii = request.form.get('observatii')
        achitata = True if request.form.get('achitata') else False
        
        # Create the invoice
        factura = Factura(
            serie=serie,
            numar=numar,
            data_emitere=data_emitere,
            data_scadenta=data_scadenta,
            client_id=client_id,
            metoda_plata=metoda_plata,
            observatii=observatii,
            achitata=achitata,
            valoare_totala=float(request.form.get('valoare_totala')),
            valoare_tva=float(request.form.get('valoare_tva'))
        )
        
        db.session.add(factura)
        db.session.commit()
        
        # Get product information
        produse_ids = request.form.getlist('produse[]')
        cantitati = request.form.getlist('cantitati[]')
        preturi = request.form.getlist('preturi[]')
        tvs = request.form.getlist('tva[]')
        valori = request.form.getlist('valori[]')
        
        # Add invoice details
        for i in range(len(produse_ids)):
            if produse_ids[i] and int(produse_ids[i]) > 0:
                produs_id = int(produse_ids[i])
                cantitate = int(cantitati[i])
                pret_unitar = float(preturi[i])
                tva_procent = int(tvs[i])
                valoare = float(valori[i])
                valoare_tva = valoare * tva_procent / 100
                
                detaliu = DetaliiFactura(
                    factura_id=factura.id,
                    produs_id=produs_id,
                    cantitate=cantitate,
                    pret_unitar=pret_unitar,
                    tva=tva_procent,
                    valoare=valoare,
                    valoare_tva=valoare_tva
                )
                db.session.add(detaliu)
                
                # Update stock
                miscare_stoc = MiscareStoc(
                    produs_id=produs_id,
                    cantitate=-cantitate,
                    tip='iesire',
                    data=datetime.now(),
                    factura_id=factura.id,
                    motiv=f"Vânzare factură {serie}{numar}"
                )
                db.session.add(miscare_stoc)
                
                # Update product stock
                produs = Produs.query.get(produs_id)
                produs.stoc -= cantitate
                
                db.session.add(produs)
        
        db.session.commit()
        flash('Factura a fost adăugată cu succes!', 'success')
        return redirect(url_for('facturi.index'))
    
    clienti = Client.query.filter_by(activ=True).all()
    produse = Produs.query.filter_by(activ=True).all()
    
    # Get the next invoice number for the default serie
    serie_default = "NET"
    ultima_factura = Factura.query.filter_by(serie=serie_default).order_by(Factura.numar.desc()).first()
    if ultima_factura:
        next_numar = ultima_factura.numar + 1
    else:
        # Start from 6 to account for the previous 5 invoices
        next_numar = 6
    
    return render_template('facturi/adauga.html', clienti=clienti, produse=produse, next_numar=next_numar)

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
