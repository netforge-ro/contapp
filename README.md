# ContApp - Sistem de Contabilitate

```bash
sudo pkill -f "gunicorn.*contapp.*wsgi:application"
cd /var/www-tools/contapp && sudo -u nobody ./scripts/check_running.sh
```

ContApp este o aplicație web pentru gestionarea facturării, furnizorilor, stocurilor, clienților și rapoartelor financiare, dezvoltată integral în limba română pentru mediul universitar.

![ContApp Dashboard](screenshots/dashboard.png)

## Funcționalități principale

- **Dashboard**: Prezentare grafică a situației financiare, stocurilor și vânzărilor
- **Facturare**: Creare, editare și gestionare facturi client cu calculare automată TVA
- **Clienți**: Administrarea completă a bazei de date de clienți și istoricul facturilor
- **Furnizori**: Gestionarea furnizorilor și a facturilor primite
- **Stocuri**: Monitorizare și ajustare stocuri de produse, alerte pentru stoc minim
- **Rapoarte**: Generare rapoarte detaliate de vânzări, cheltuieli, stocuri, și statistici pentru clienți și furnizori

## Tehnologii utilizate

- **Backend**: Python 3.9, Flask, SQLAlchemy, Flask-Migrate
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Grafice**: Chart.js 4.4.1 pentru vizualizări interactive
- **Stilizare**: Material Design inspirat, interfață responsivă pentru desktop și dispozitive mobile
- **Bază de date**: PostgreSQL - relațional, robust și performant
- **Deployment**: Gunicorn (WSGI server), LiteSpeed Web Server ca proxy

## Avantaje

- **Interfață complet în limba română** - adaptată pentru piața din România
- **Calculare automată TVA** - conform legislației din România
- **Rapoarte detaliate** - exportabile și ușor de interpretat
- **Design responsive** - utilizabil pe orice dispozitiv
- **Grafice interactive** - pentru analiză financiară și de stocuri
- **Securitate îmbunătățită** - autentificare și autorizare robustă

## Instrucțiuni de instalare

### Cerințe sistem
- Python 3.9+
- PostgreSQL 13+
- LiteSpeed Web Server sau alt server web cu capacități de proxy

### Configurare bază de date

```bash
# Crearea utilizatorului PostgreSQL
sudo -u postgres psql -c "CREATE USER contapp_user WITH PASSWORD 'YOUR_PASSWORD_HERE';"

# Crearea bazei de date
sudo -u postgres psql -c "CREATE DATABASE contapp WITH OWNER contapp_user;"

# Acordare drepturi pentru utilizator
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE contapp TO contapp_user;"
```

### Instalare aplicație

```bash
# Clonare repository
git clone https://github.com/YOUR_USERNAME/contapp.git /var/www-tools/contapp

# Creare mediu virtual Python
cd /var/www-tools/contapp
python3 -m venv venv

# Activare mediu virtual
source venv/bin/activate

# Instalare dependințe
pip install -r requirements.txt

# Crearea tabelelor în baza de date
python manage.py create_tables

# Adăugare date de exemplu (opțional)
python manage.py add_sample_data

# Asigură-te că scriptul check_running.sh este executabil
chmod +x scripts/check_running.sh
```

### Configurarea pentru rulare automată

Adaugă următoarea intrare în crontab pentru a rula automat aplicația:

```bash
# Editare crontab
crontab -e

# Adaugă următoarea linie
*/5 * * * * nobody /var/www-tools/contapp/scripts/check_running.sh >/dev/null 2>&1
```

### Accesare aplicație

După configurare și pornire, aplicația va fi disponibilă la:

```
http://your-server:8086
```

Dacă LiteSpeed Web Server este configurat ca proxy, aplicația va fi disponibilă la URL-ul configurat în LiteSpeed.

## Structura proiectului

```
/contapp/
│
├── app/                      # Codul principal al aplicației
│   ├── __init__.py           # Inițializare aplicație Flask
│   ├── config.py             # Configurări aplicație
│   ├── models.py             # Modele SQLAlchemy
│   ├── routes/               # Blueprint-uri pentru rute
│       ├── dashboard.py      # Rute pentru dashboard
│       ├── facturi.py        # Rute pentru facturare
│       ├── clienti.py        # Rute pentru clienți
│       ├── furnizori.py      # Rute pentru furnizori
│       ├── stocuri.py        # Rute pentru stocuri
│       └── rapoarte.py       # Rute pentru rapoarte
│
├── templates/                # Șabloane Jinja2
│   ├── base.html            # Șablon de bază
│   ├── dashboard/           # Șabloane dashboard
│   ├── facturi/             # Șabloane facturi
│   ├── clienti/             # Șabloane clienți
│   ├── furnizori/           # Șabloane furnizori
│   ├── stocuri/             # Șabloane stocuri
│   └── rapoarte/            # Șabloane rapoarte
│
├── static/                   # Fișiere statice (CSS, JS, imagini)
│   ├── css/                 # Stiluri CSS
│   ├── js/                  # Scripturi JavaScript
│   └── img/                 # Imagini
│
├── scripts/                  # Scripturi pentru administrare
│   └── check_running.sh     # Script verificare și repornire aplicație
│
├── logs/                     # Directorul pentru log-uri
├── venv/                     # Mediul virtual Python (nu inclus în repo)
├── manage.py                 # Script pentru administrare
├── wsgi.py                   # Punct de intrare pentru WSGI
├── app.py                    # Punct de intrare pentru dezvoltare
├── reset_db.py               # Script pentru resetare bază de date
└── README.md                 # Acest fișier
```

## Dezvoltare și testare

Pentru dezvoltare și testare locală:

```bash
# Activare mediu virtual
cd /var/www-tools/contapp
source venv/bin/activate

# Pornire server de dezvoltare cu reîncărcare automată
python app.py
```

Pentru a reseta baza de date în timpul dezvoltării:

```bash
python reset_db.py
python manage.py add_sample_data
```

## Contacte

Pentru întrebări sau sugestii legate de acest proiect, vă rugăm să contactați:

- GitHub: https://github.com/YOUR_USERNAME/contapp

## Licență

Acest proiect este destinat exclusiv pentru utilizare educațională în mediul universitar. Toate drepturile sunt rezervate.
