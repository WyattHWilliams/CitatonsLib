# ----- [///// IMPORTS /////] -----
from flask import Flask, request, render_template, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FormField
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap

# ----- [///// COMFIGURATIONS /////] -----
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SHH'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
Bootstrap(app)


# ----- [///// FUNCTIONS /////] -----
def create_models():
    db.drop_all()
    db.create_all()
    print('models created')


# ----- [///// MODELS /////] -----
class Citation(db.Model):
    __tablename__ = 'citations'
    sum_states = ['Not Started', 'In Progress', 'Complete']

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    volume = db.Column(db.Text,
                       nullable=True)
    edition = db.Column(db.Integer,
                        nullable=True)
    author = db.Column(db.Text,
                       nullable=False,
                       default='Unknown')
    publisher = db.Column(db.Text,
                          nullable=False,
                          default='Unknown')
    yr_published = db.Column(db.Text, default='Unknown')
    url = db.Column(db.Text)
    lccn = db.Column(db.Text)
    yr_accessed = db.Column(db.Text)
    summary_status = db.Column(db.Text,
                               nullable=False,
                               default='Not Started')
    sections = db.relationship('Section', backref='citations')


class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    parent_citation = db.Column(db.Integer,
                                foreign_key='citations.id',
                                nullable=False)
    sec_summary = db.Column(db.Text)
    entries = db.relationship('Entry', backref='sections')


class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    page_start = db.Column(db.Text)
    paragraph_start = db.Column(db.Text)
    page_stop = db.Column(db.Text)
    paragraph_stop = db.Column(db.Text)
    content = db.Column(db.Text)
    parent_section = db.Column(db.Integer,
                               foreign_key='sections.id',
                               nullable=False)
    # referenced_citations = db.relationship('Citation', backref='entries')


class NewEntryForm(FlaskForm):
    page_start = StringField('From Page')
    paragraph_start = StringField('Paragraph')
    page_stop = StringField('To Page')
    paragraph_stop = StringField('Paragraph')
    content = StringField('Entry', validators=[InputRequired()])


class NewSectionForm(FlaskForm):
    sec_summary = StringField('Section Summary', validators=[InputRequired()])
    entry_form = FormField(NewEntryForm)


class NewCitationForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    volume = StringField('Volume')
    edition = StringField('Edition')
    author = StringField('Author')
    publisher = StringField('Publisher')
    yr_published = StringField('Year Published')
    url = StringField('URL')
    lccn = StringField('Library of Congress Call Number')
    yr_accessed = StringField('Year First Accessed')
    summary_status = SelectField('Summary Status', choices=[
                                 (s, s) for s in Citation.sum_states])
    section_form = FormField(NewSectionForm)


create_models()


@app.route('/')
def main():
    form = NewCitationForm()
    return render_template('newCitation.html', form=form)
