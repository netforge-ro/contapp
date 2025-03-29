from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Produs, MiscareStoc, CategorieProdusCheltuiala, Furnizor
from app.models import Depozit, Stoc, Comanda, ProduseComandate, Plata
from app import db

bp = Blueprint('stocuri', __name__, url_prefix='/stocuri')

@bp.route('/')
def index():
    produse = Produs.query.order_by(Produs.nume).all()
    return render_template('stocuri/index.html', produse=produse)

@bp.route('/adauga', methods=['GET', 'POST'])
def adauga():
    if request.method == 'POST':
        cod = request.form.get('cod')
        nume = request.form.get('nume')
        unitate_masura = request.form.get('unitate_masura')
        stoc = request.form.get('stoc', 0, type=int)
        categorie_id = request.form.get('categorie_id')
        pret_achizitie = request.form.get('pret_achizitie')
        pret_vanzare = request.form.get('pret_vanzare')
        tva = request.form.get('tva', 19, type=int)
        furnizor_id = request.form.get('furnizor_id')
        activ = True if request.form.get('activ') else False
        
        # Ensure categorie_id is None if empty string
        categorie_id = None if not categorie_id else int(categorie_id)
        # Ensure furnizor_id is None if empty string
        furnizor_id = None if not furnizor_id else int(furnizor_id)
        
        # Convert prices to float
        pret_achizitie = float(pret_achizitie) if pret_achizitie else 0
        pret_vanzare = float(pret_vanzare) if pret_vanzare else 0
        
        # Create new product
        produs = Produs(
            cod=cod,
            nume=nume,
            unitate_masura=unitate_masura,
            stoc=stoc,
            categorie_id=categorie_id,
            pret_achizitie=pret_achizitie,
            pret_vanzare=pret_vanzare,
            pret=pret_vanzare, # Also set the new 'pret' field from diagrams
            tva=tva,
            furnizor_id=furnizor_id,
            activ=activ
        )
        
        db.session.add(produs)
        
        # If initial stock is > 0, create a stock movement record
        if stoc > 0:
            miscare = MiscareStoc(
                produs_id=produs.id,
                tip='intrare',
                cantitate=stoc,
                motiv='Stoc inițial'
            )
            db.session.add(miscare)
        
        db.session.commit()
        
        flash(f'Produsul "{nume}" a fost adăugat cu succes!', 'success')
        return redirect(url_for('stocuri.index'))
    
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
        cod = request.form.get('cod')
        nume = request.form.get('nume')
        unitate_masura = request.form.get('unitate_masura')
        categorie_id = request.form.get('categorie_id')
        pret_achizitie = request.form.get('pret_achizitie')
        pret_vanzare = request.form.get('pret_vanzare')
        tva = request.form.get('tva', 19, type=int)
        furnizor_id = request.form.get('furnizor_id')
        activ = True if request.form.get('activ') else False
        
        # Ensure categorie_id is None if empty string
        categorie_id = None if not categorie_id else int(categorie_id)
        # Ensure furnizor_id is None if empty string
        furnizor_id = None if not furnizor_id else int(furnizor_id)
        
        # Convert prices to float
        pret_achizitie = float(pret_achizitie) if pret_achizitie else 0
        pret_vanzare = float(pret_vanzare) if pret_vanzare else 0
        
        # Update product
        produs.cod = cod
        produs.nume = nume
        produs.unitate_masura = unitate_masura
        produs.categorie_id = categorie_id
        produs.pret_achizitie = pret_achizitie
        produs.pret_vanzare = pret_vanzare
        produs.pret = pret_vanzare  # Also update the new 'pret' field from diagrams
        produs.tva = tva
        produs.furnizor_id = furnizor_id
        produs.activ = activ
        
        db.session.commit()
        
        flash(f'Produsul "{nume}" a fost actualizat cu succes!', 'success')
        return redirect(url_for('stocuri.index'))
    
    categorii = CategorieProdusCheltuiala.query.all()
    furnizori = Furnizor.query.filter_by(activ=True).all()
    
    return render_template('stocuri/editeaza.html', produs=produs, categorii=categorii, furnizori=furnizori)

@bp.route('/categorii')
def categorii():
    categorii = CategorieProdusCheltuiala.query.all()
    return render_template('stocuri/categorii.html', categorii=categorii)

@bp.route('/adauga_categorie', methods=['POST'])
def adauga_categorie():
    nume = request.form.get('nume')
    descriere = request.form.get('descriere')
    
    if not nume:
        flash('Numele categoriei este obligatoriu!', 'danger')
        return redirect(url_for('stocuri.categorii'))
    
    categorie = CategorieProdusCheltuiala(nume=nume, descriere=descriere)
    db.session.add(categorie)
    db.session.commit()
    
    flash(f'Categoria "{nume}" a fost adăugată cu succes!', 'success')
    return redirect(url_for('stocuri.categorii'))

@bp.route('/editeaza_categorie', methods=['POST'])
def editeaza_categorie():
    id = request.form.get('id')
    nume = request.form.get('nume')
    descriere = request.form.get('descriere')
    
    categorie = CategorieProdusCheltuiala.query.get_or_404(id)
    
    categorie.nume = nume
    categorie.descriere = descriere
    
    db.session.commit()
    
    flash(f'Categoria "{nume}" a fost actualizată cu succes!', 'success')
    return redirect(url_for('stocuri.categorii'))

@bp.route('/sterge_categorie', methods=['POST'])
def sterge_categorie():
    id = request.form.get('id')
    categorie = CategorieProdusCheltuiala.query.get_or_404(id)
    
    # Verifică dacă categoria are produse asociate
    if categorie.produse:
        flash('Categoria nu poate fi ștearsă deoarece are produse asociate!', 'danger')
        return redirect(url_for('stocuri.categorii'))
    
    nume = categorie.nume
    db.session.delete(categorie)
    db.session.commit()
    
    flash(f'Categoria "{nume}" a fost ștearsă cu succes!', 'success')
    return redirect(url_for('stocuri.categorii'))

@bp.route('/ajustare', methods=['GET', 'POST'])
def ajustare():
    if request.method == 'POST':
        produs_id = request.form.get('produs_id')
        tip_ajustare = request.form.get('tip_ajustare')
        cantitate = int(request.form.get('cantitate', 0))
        motiv = request.form.get('motiv')
        observatii = request.form.get('observatii')
        
        # Verifică datele introduse
        if not produs_id or not cantitate or cantitate <= 0 or not motiv:
            flash('Toate câmpurile sunt obligatorii și cantitatea trebuie să fie pozitivă!', 'danger')
            return redirect(url_for('stocuri.ajustare'))
        
        produs = Produs.query.get_or_404(produs_id)
        
        # Determină tipul de ajustare și cantitatea efectivă
        tip_miscare = 'ajustare'
        if tip_ajustare == 'plus':
            # Adaugă la stoc
            produs.stoc += cantitate
            cantitate_finala = cantitate
        else:
            # Scade din stoc
            if cantitate > produs.stoc:
                flash(f'Cantitatea de scăzut ({cantitate}) este mai mare decât stocul actual ({produs.stoc})!', 'danger')
                return redirect(url_for('stocuri.ajustare'))
            
            produs.stoc -= cantitate
            cantitate_finala = -cantitate  # Marcăm ca o cantitate negativă pentru mișcarea de stoc
        
        # Creează înregistrarea de mișcare stoc
        motiv_complet = f"{motiv}" + (f": {observatii}" if observatii else "")
        miscare = MiscareStoc(
            produs_id=produs.id,
            tip=tip_miscare,
            cantitate=cantitate_finala,
            motiv=motiv_complet
        )
        
        db.session.add(miscare)
        db.session.commit()
        
        # Mesaj de confirmare
        operatie = "adăugată" if tip_ajustare == 'plus' else "scăzută"
        flash(f'Ajustare efectuată cu succes! Cantitate {operatie}: {abs(cantitate_finala)} {produs.unitate_masura}.', 'success')
        return redirect(url_for('stocuri.index'))
    
    produse = Produs.query.filter_by(activ=True).all()
    return render_template('stocuri/ajustare.html', produse=produse)

# Gestionare depozite
@bp.route('/depozite')
def depozite():
    depozite = Depozit.query.all()
    return render_template('stocuri/depozite/index.html', depozite=depozite)

@bp.route('/depozite/adauga', methods=['GET', 'POST'])
def adauga_depozit():
    if request.method == 'POST':
        nume_depozit = request.form.get('nume_depozit')
        adresa = request.form.get('adresa')
        observatii = request.form.get('observatii')
        
        if not nume_depozit:
            flash('Numele depozitului este obligatoriu!', 'danger')
            return redirect(url_for('stocuri.depozite'))
        
        depozit = Depozit(
            nume_depozit=nume_depozit,
            adresa=adresa,
            observatii=observatii
        )
        
        db.session.add(depozit)
        db.session.commit()
        
        flash(f'Depozitul "{nume_depozit}" a fost adăugat cu succes!', 'success')
        return redirect(url_for('stocuri.depozite'))
    
    return render_template('stocuri/depozite/adauga.html')

@bp.route('/depozite/<int:id>')
def vezi_depozit(id):
    depozit = Depozit.query.get_or_404(id)
    stocuri = Stoc.query.filter_by(depozit_id=id).all()
    return render_template('stocuri/depozite/vezi.html', depozit=depozit, stocuri=stocuri)

@bp.route('/depozite/<int:id>/editeaza', methods=['GET', 'POST'])
def editeaza_depozit(id):
    depozit = Depozit.query.get_or_404(id)
    
    if request.method == 'POST':
        nume_depozit = request.form.get('nume_depozit')
        adresa = request.form.get('adresa')
        observatii = request.form.get('observatii')
        
        if not nume_depozit:
            flash('Numele depozitului este obligatoriu!', 'danger')
            return redirect(url_for('stocuri.editeaza_depozit', id=id))
        
        depozit.nume_depozit = nume_depozit
        depozit.adresa = adresa
        depozit.observatii = observatii
        
        db.session.commit()
        
        flash(f'Depozitul "{nume_depozit}" a fost actualizat cu succes!', 'success')
        return redirect(url_for('stocuri.depozite'))
    
    return render_template('stocuri/depozite/editeaza.html', depozit=depozit)

@bp.route('/depozite/<int:id>/sterge', methods=['POST'])
def sterge_depozit(id):
    depozit = Depozit.query.get_or_404(id)
    
    # Verifică dacă există stocuri în acest depozit
    stocuri = Stoc.query.filter_by(depozit_id=id).first()
    if stocuri:
        flash('Depozitul nu poate fi șters deoarece conține produse!', 'danger')
        return redirect(url_for('stocuri.depozite'))
    
    nume_depozit = depozit.nume_depozit
    db.session.delete(depozit)
    db.session.commit()
    
    flash(f'Depozitul "{nume_depozit}" a fost șters cu succes!', 'success')
    return redirect(url_for('stocuri.depozite'))

# Gestionare comenzi
@bp.route('/comenzi')
def comenzi():
    comenzi = Comanda.query.order_by(Comanda.data_comanda.desc()).all()
    return render_template('stocuri/comenzi/index.html', comenzi=comenzi)

@bp.route('/comenzi/adauga', methods=['GET', 'POST'])
def adauga_comanda():
    if request.method == 'POST':
        furnizor_id = request.form.get('furnizor_id')
        data_comanda = request.form.get('data_comanda')
        data_livrare = request.form.get('data_livrare')
        stare_comanda = request.form.get('stare_comanda', 'Nouă')
        observatii = request.form.get('observatii')
        
        if not furnizor_id or not data_comanda:
            flash('Furnizorul și data comenzii sunt obligatorii!', 'danger')
            return redirect(url_for('stocuri.adauga_comanda'))
        
        comanda = Comanda(
            furnizor_id=furnizor_id,
            data_comanda=data_comanda,
            data_livrare=data_livrare,
            stare_comanda=stare_comanda,
            observatii=observatii
        )
        
        db.session.add(comanda)
        db.session.commit()
        
        # Adaugă produsele la comandă
        produse_ids = request.form.getlist('produs_id[]')
        cantitati = request.form.getlist('cantitate[]')
        
        for i in range(len(produse_ids)):
            if produse_ids[i] and cantitati[i] and int(cantitati[i]) > 0:
                produs_comandat = ProduseComandate(
                    produs_id=produse_ids[i],
                    comanda_id=comanda.id,
                    cantitate_comandata=cantitati[i]
                )
                db.session.add(produs_comandat)
        
        db.session.commit()
        
        flash(f'Comanda către furnizorul nr. {comanda.id} a fost adăugată cu succes!', 'success')
        return redirect(url_for('stocuri.comenzi'))
    
    from datetime import date
    furnizori = Furnizor.query.filter_by(activ=True).all()
    produse = Produs.query.filter_by(activ=True).all()
    today = date.today().isoformat()
    return render_template('stocuri/comenzi/adauga.html', furnizori=furnizori, produse=produse, today=today)

@bp.route('/comenzi/<int:id>')
def vezi_comanda(id):
    comanda = Comanda.query.get_or_404(id)
    produse_comandate = ProduseComandate.query.filter_by(comanda_id=id).all()
    return render_template('stocuri/comenzi/vezi.html', comanda=comanda, produse_comandate=produse_comandate)

@bp.route('/comenzi/<int:id>/editeaza', methods=['GET', 'POST'])
def editeaza_comanda(id):
    comanda = Comanda.query.get_or_404(id)
    
    if request.method == 'POST':
        furnizor_id = request.form.get('furnizor_id')
        data_comanda = request.form.get('data_comanda')
        data_livrare = request.form.get('data_livrare')
        stare_comanda = request.form.get('stare_comanda')
        observatii = request.form.get('observatii')
        
        if not furnizor_id or not data_comanda:
            flash('Furnizorul și data comenzii sunt obligatorii!', 'danger')
            return redirect(url_for('stocuri.editeaza_comanda', id=id))
        
        comanda.furnizor_id = furnizor_id
        comanda.data_comanda = data_comanda
        comanda.data_livrare = data_livrare
        comanda.stare_comanda = stare_comanda
        comanda.observatii = observatii
        
        db.session.commit()
        
        flash(f'Comanda nr. {comanda.id} a fost actualizată cu succes!', 'success')
        return redirect(url_for('stocuri.comenzi'))
    
    furnizori = Furnizor.query.filter_by(activ=True).all()
    produse_comandate = ProduseComandate.query.filter_by(comanda_id=id).all()
    return render_template('stocuri/comenzi/editeaza.html', comanda=comanda, furnizori=furnizori, produse_comandate=produse_comandate)

@bp.route('/comenzi/<int:id>/sterge', methods=['POST'])
def sterge_comanda(id):
    comanda = Comanda.query.get_or_404(id)
    
    # Șterge toate produsele comandate asociate
    ProduseComandate.query.filter_by(comanda_id=id).delete()
    
    # Șterge comanda
    db.session.delete(comanda)
    db.session.commit()
    
    flash(f'Comanda nr. {id} a fost ștearsă cu succes!', 'success')
    return redirect(url_for('stocuri.comenzi'))

# Gestionare plăți
@bp.route('/plati')
def plati():
    plati = Plata.query.order_by(Plata.data_platii.desc()).all()
    return render_template('stocuri/plati/index.html', plati=plati)

@bp.route('/plati/adauga', methods=['GET', 'POST'])
def adauga_plata():
    if request.method == 'POST':
        comanda_id = request.form.get('comanda_id')
        data_platii = request.form.get('data_platii')
        valoare = request.form.get('valoare')
        modalitate_plata = request.form.get('modalitate_plata')
        observatii = request.form.get('observatii')
        
        if not comanda_id or not data_platii or not valoare:
            flash('Comanda, data plății și valoarea sunt obligatorii!', 'danger')
            return redirect(url_for('stocuri.adauga_plata'))
        
        plata = Plata(
            comanda_id=comanda_id,
            data_platii=data_platii,
            valoare=valoare,
            modalitate_plata=modalitate_plata,
            observatii=observatii
        )
        
        db.session.add(plata)
        db.session.commit()
        
        flash(f'Plata pentru comanda nr. {comanda_id} a fost adăugată cu succes!', 'success')
        return redirect(url_for('stocuri.plati'))
    
    comenzi = Comanda.query.all()
    return render_template('stocuri/plati/adauga.html', comenzi=comenzi)

@bp.route('/plati/<int:id>')
def vezi_plata(id):
    plata = Plata.query.get_or_404(id)
    return render_template('stocuri/plati/vezi.html', plata=plata)

@bp.route('/plati/<int:id>/editeaza', methods=['GET', 'POST'])
def editeaza_plata(id):
    plata = Plata.query.get_or_404(id)
    
    if request.method == 'POST':
        comanda_id = request.form.get('comanda_id')
        data_platii = request.form.get('data_platii')
        valoare = request.form.get('valoare')
        modalitate_plata = request.form.get('modalitate_plata')
        observatii = request.form.get('observatii')
        
        if not comanda_id or not data_platii or not valoare:
            flash('Comanda, data plății și valoarea sunt obligatorii!', 'danger')
            return redirect(url_for('stocuri.editeaza_plata', id=id))
        
        plata.comanda_id = comanda_id
        plata.data_platii = data_platii
        plata.valoare = valoare
        plata.modalitate_plata = modalitate_plata
        plata.observatii = observatii
        
        db.session.commit()
        
        flash(f'Plata nr. {id} a fost actualizată cu succes!', 'success')
        return redirect(url_for('stocuri.plati'))
    
    comenzi = Comanda.query.all()
    return render_template('stocuri/plati/editeaza.html', plata=plata, comenzi=comenzi)

@bp.route('/plati/<int:id>/sterge', methods=['POST'])
def sterge_plata(id):
    plata = Plata.query.get_or_404(id)
    db.session.delete(plata)
    db.session.commit()
    
    flash(f'Plata nr. {id} a fost ștearsă cu succes!', 'success')
    return redirect(url_for('stocuri.plati'))

@bp.route('/<int:id>/sterge', methods=['POST'])
def sterge(id):
    produs = Produs.query.get_or_404(id)
    nume = produs.nume
    
    # Delete product
    db.session.delete(produs)
    db.session.commit()
    
    flash(f'Produsul "{nume}" a fost șters cu succes!', 'success')
    return redirect(url_for('stocuri.index'))
