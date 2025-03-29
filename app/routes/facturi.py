from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from app.models import Factura, DetaliiFactura, Client, Produs, MiscareStoc
from app import db
from datetime import datetime, timedelta
import io
from xhtml2pdf import pisa

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
        
        # Create the invoice with both old and new fields
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
            valoare_tva=float(request.form.get('valoare_tva')),
            # New fields
            serie_factura=serie,
            nr_factura=numar,
            data_factura=data_emitere,
            valoare=float(request.form.get('valoare_totala')),
            modalitate_plata=metoda_plata
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
        # Get form data
        data_emitere = datetime.strptime(request.form.get('data_emitere'), '%Y-%m-%d')
        data_scadenta = datetime.strptime(request.form.get('data_scadenta'), '%Y-%m-%d')
        client_id = request.form.get('client_id')
        metoda_plata = request.form.get('metoda_plata')
        observatii = request.form.get('observatii')
        achitata = True if request.form.get('achitata') else False
        valoare_totala = float(request.form.get('valoare_totala'))
        valoare_tva = float(request.form.get('valoare_tva'))
        
        # Update the data
        factura.data_emitere = data_emitere
        factura.data_factura = data_emitere  # Update the new field too
        factura.data_scadenta = data_scadenta
        factura.client_id = client_id
        factura.metoda_plata = metoda_plata
        factura.modalitate_plata = metoda_plata  # Update the new field too
        factura.observatii = observatii
        factura.achitata = achitata
        factura.valoare_totala = valoare_totala
        factura.valoare_tva = valoare_tva
        factura.valoare = valoare_totala  # Update the new field too
        
        # Before updating details, we need to restore the stock
        for detaliu in factura.detalii:
            produs = Produs.query.get(detaliu.produs_id)
            produs.stoc += detaliu.cantitate
        
        # Delete existing details
        for detaliu in factura.detalii:
            db.session.delete(detaliu)
        
        # Get updated product information
        produse_ids = request.form.getlist('produse[]')
        cantitati = request.form.getlist('cantitati[]')
        preturi = request.form.getlist('preturi[]')
        tvs = request.form.getlist('tva[]')
        valori = request.form.getlist('valori[]')
        
        # Add updated invoice details
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
                
                # Update product stock
                produs = Produs.query.get(produs_id)
                produs.stoc -= cantitate
                db.session.add(produs)
        
        db.session.commit()
        flash('Factura a fost actualizată cu succes!', 'success')
        return redirect(url_for('facturi.index'))
    
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

@bp.route('/<int:id>/pdf')
def pdf(id):
    factura = Factura.query.get_or_404(id)
    
    # Render the HTML template
    html = render_template('facturi/pdf_template.html', factura=factura)
    
    # Create a file-like buffer to receive PDF data
    pdf_buffer = io.BytesIO()
    
    # Generate PDF from HTML
    try:
        # Convert HTML to PDF and write to buffer
        pisa_status = pisa.CreatePDF(
            html,                   # HTML source
            dest=pdf_buffer,        # Output file handle
            encoding='UTF-8'        # Encoding
        )
        
        # Rewind the buffer to the beginning
        pdf_buffer.seek(0)
        
        # Create a response with the PDF
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=Factura_{factura.serie}{factura.numar}.pdf'
        
        return response
    except Exception as e:
        flash(f'Eroare la generarea PDF-ului: {str(e)}', 'danger')
        return redirect(url_for('facturi.vezi', id=id))
