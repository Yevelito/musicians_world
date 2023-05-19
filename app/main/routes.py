from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, current_app, g
from app.main.forms import SearchForm
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from sqlalchemy import desc
from flask_babel import _
from flask import g
from flask_babel import get_locale

from wtforms import SubmitField

from app import app, db
from app.main import bp
from app.main.forms import EditProfileForm, AddAlbumForm, EditAlbumForm
from app.models import User, Album


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    albums = current_user.followed_albums().paginate(page=page, per_page=current_app.config['ALBUMS_PER_PAGE'],
                                                     error_out=False)
    next_url = url_for('main.index', page=albums.next_num) \
        if albums.has_next else None
    prev_url = url_for('main.index', albums=albums.prev_num) \
        if albums.has_prev else None
    return render_template('index.html', title=_('Home'), albums=albums.items, next_url=next_url, prev_url=prev_url)


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    albums = Album.query.filter_by(artist_id=user.id).paginate(page=page,
                                                               per_page=current_app.config['ALBUMS_PER_PAGE'],
                                                               error_out=False)
    # songs = Song.query.filter_by()
    next_url = url_for('main.user', username=user.username, page=albums.next_num) \
        if albums.has_next else None
    prev_url = url_for('main.user', username=user.username, page=albums.prev_num) \
        if albums.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, albums=albums.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


@bp.route('/add_album', methods=['GET', 'POST'])
@login_required
def add_album():
    form = AddAlbumForm(current_user.id)
    if form.validate_on_submit():
        album = Album(artist_id=form.artist_id)
        album.title = form.title.data
        album.year = form.year.data
        album.link = form.link.data
        db.session.add(album)
        db.session.commit()
        flash(_('Your album  have been saved.'))
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':

        return render_template('add_album.html', title=_('Add new album'), form=form)


@bp.route('/edit_album/<album_id>', methods=['GET', 'POST'])
@login_required
def edit_album(album_id):
    album = Album.query.filter_by(id=album_id).first_or_404()
    form = EditAlbumForm(album.id)
    if form.validate_on_submit():
        album.title = form.title.data
        album.year = form.year.data
        album.link = form.link.data
        album.songs_count = form.songs_count.data
        db.session.add(album)
        db.session.commit()
        flash(_('Your album  have been changed.'))
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.title.data = album.title
        form.year.data = album.year
        form.link.data = album.link
        form.songs_count.data = album.songs_count
        return render_template('edit_album.html', title=_('Edit your album'), form=form)


@bp.route('/delete_album/<album_id>', methods=['GET', 'POST'])
@login_required
def delete_album(album_id):
    album = Album.query.filter_by(id=album_id).first_or_404()
    try:
        db.session.delete(album)
        db.session.commit()
        return redirect(url_for('main.user', username=current_user.username))

    except:
        return "Album was not exist"


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %(username)s.', username=username)
    return redirect(url_for('main.user', username=username))


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    albums = Album.query.order_by(desc(Album.year)).paginate(page=page, per_page=current_app.config['ALBUMS_PER_PAGE'],
                                                             error_out=False)
    next_url = url_for('main.explore', page=albums.next_num) \
        if albums.has_next else None
    prev_url = url_for('main.explore', page=albums.prev_num) \
        if albums.has_prev else None
    return render_template("index.html", title=_('Explore'), albums=albums.items, next_url=next_url, prev_url=prev_url)


@bp.route('/search')
@login_required
def search():
    # if not g.search_form.validate():
    #     return redirect(url_for('main.explore'))

    page = request.args.get('page', 1, type=int)
    albums, total = Album.search(g.search_form.q.data, page,
                                 current_app.config['ALBUMS_PER_PAGE'])

    #if we didnt find smth we redirect to explore page
    if total.get('value') == 0:
        return redirect(url_for('main.explore'))

    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total.get('value') > page * current_app.config['ALBUMS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), albums=albums,
                           next_url=next_url, prev_url=prev_url)
