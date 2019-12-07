from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app.forms import LoginForm, RegistrationForm, NewBandForm
from app.models import *
from app import app, db
import pandas as pd
from app.utilities import encode, decode


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

#adding encoding
@app.route('/artists')
def artists():
    band_list = Band.query.all()
    return render_template('artists.html', title='Artists', bands=band_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")

    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()
    df = pd.read_csv('app/2019PerformerSchedule.csv', index_col=0, sep=',')
    #add porches first
    porches = df['Porch Address'].unique()
    print(porches[0])
    for i in range(porches.shape[0]):
        porch = Porch(porches[i], 0, 0) #dummy long and lat for now
        db.session.add(porch)
        db.session.commit()
    #Then artists
    for i in range(df.shape[0]):
        row = df.iloc[i]
        artist = Band(row['Name'], row['Description'], 'test' + str(i), row['URL'])
        db.session.add(artist)
        db.session.commit()
    #Then events
    for i in range(df.shape[0]):
        row = df.iloc[i]
        artist = db.session.query(Band).filter_by(name = row['Name']).first()
        porch = db.session.query(Porch).filter_by(address = row['Porch Address']).first()
        timing = int(row['Assigned Timeslot'].split('-')[0])
        if not timing == 12:
            timing += 12
        time = datetime(2019, 9, 22, timing)
        event = Event(time, artist.id, porch.id)
        db.session.add(event)
        db.session.commit()
    return render_template('index.html', title='Home')


@app.route('/artist/<name>')
def artist(name):
        band = db.session.query(Band).filter_by(name=name).first()
        events = db.session.query(Event).join(Band, Band.id == Event.bandID).filter(Band.name == name).all()
        porches = db.session.query(Porch).join(Event, Event.porchID == Porch.id).join(Band, Band.id == Event.bandID).filter(Band.name == name).all()

        return render_template('artistPage.html', title=name, band=band, events=events, porches=porches)


@app.route('/signUpBand', methods = ['GET', 'POST'])
def createNewBand():
    form = NewBandForm()
    if form.validate_on_submit():
        if (db.session.query(Band).filter_by(name = form.bandName.data).first()):
            flash("Band name already in use")
            return render_template('signUpBand.html', title = "Sign Up For Porchfest", form = form)
        flash('New Band Created: {}, '.format(
            form.bandName.data))
        band = Band(form.bandName.data, form.bio.data, form.image.data, form.link.data)
        db.session.add(band)
        db.session.commit()
        if not db.session.query(Porch).filter_by(address = form.address.data).first():
            porch = Porch(form.address.data, 0, 0)
            db.session.add(porch)
            db.session.commit()
        else:
            porch = db.session.query(Porch).filter_by(address = form.address.data).first()
        timing = datetime(2019, 9, 22, form.time.data.hour, form.time.data.minute)
        event = Event(timing, band.id, porch.id)
        userToBand = UserToBand(current_user.get_id(), band.id, 0, 1)
        db.session.add(event)
        db.session.add(userToBand)
        db.session.commit()

        list = db.session.query(Band).all()

        return render_template('artists.html', title="Artists", bands=list)

    return render_template('signUpBand.html', title = "Sign Up For Porchfest", form = form)


@app.route('/favoriteArtists')
def favoriteArtists():
    u2bs = db.session.query(UserToBand).filter_by(userID=current_user.get_id(), favorite=True).all()
    favorite_list = []
    for u2b in u2bs:
        band = db.session.query(Band).filter_by(id=u2b.bandID).first()
        favorite_list.append(band)
    return render_template('favoriteArtists.html', title='Favorite Artists', bands=favorite_list)


@app.route('/maps')
def maps():
    return render_template('map.html', title='Maps')

