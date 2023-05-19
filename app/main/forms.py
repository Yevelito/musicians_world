from flask import current_app
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, NumberRange
from flask_babel import lazy_gettext as _l
from app.models import User


class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=250)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_l('Please use a different username.'))


class AddAlbumForm(FlaskForm):
    title = TextAreaField(_l('Album title'), validators=[DataRequired(), Length(min=1, max=240)])
    year = IntegerField(_l('Year'), validators=[NumberRange(min=0, max=current_app.config['CURRENT_YEAR'])])
    link = TextAreaField(_l('Streaming link'), validators=[DataRequired()])
    songs_count = IntegerField(_l('Count of songs'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def __init__(self, artist_id, *args, **kwargs):
        super(AddAlbumForm, self).__init__(*args, **kwargs)
        self.artist_id = artist_id


class AddSongForm(FlaskForm):
    title = TextAreaField(_l('Song title'), validators=[DataRequired(), Length(min=1, max=240)])
    link = TextAreaField(_l('Streaming link'), validators=[DataRequired()])


class EditAlbumForm(FlaskForm):
    title = TextAreaField(_l('Album title'), validators=[DataRequired(), Length(min=1, max=240)])
    year = IntegerField(_l('Year'), validators=[NumberRange(min=0, max=current_app.config['CURRENT_YEAR'])])
    link = TextAreaField(_l('Streaming link'), validators=[DataRequired()])
    songs_count = IntegerField(_l('Count of songs'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def __init__(self, album_id, *args, **kwargs):
        super(EditAlbumForm, self).__init__(*args, **kwargs)
        self.id = album_id
