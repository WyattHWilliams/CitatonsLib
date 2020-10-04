# ----- [///// IMPORTS /////] -----
from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField, FormField, IntegerField, FieldList
from wtforms.validators import InputRequired
from config import app, db


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
    # sections = db.relationship('Section', backref='citations')


class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    parent_citation_id = db.Column(db.Integer,
                                   foreign_key='citations.id',
                                   nullable=False)
    sec_summary = db.Column(db.Text)
    # entries = db.relationship('Entry', backref='sections')

    # relationships
    citation = db.relationship('Citation', backref=db.backref(
        'sections', lazy='dynamic', collection_class=list))


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
    parent_section_id = db.Column(db.Integer,
                                  foreign_key='sections.id',
                                  nullable=False)

    # relationships
    section = db.relationship('Section', backref=db.backref(
        'entries', lazy='dynamic', collection_class=list))
    # referenced_citations = db.relationship('Citation', backref='entries')


class NewEntryForm(Form):
    page_start = IntegerField('From Page')
    paragraph_start = IntegerField('Paragraph')
    page_stop = IntegerField('To Page')
    paragraph_stop = IntegerField('Paragraph')
    content = StringField('Entry', validators=[InputRequired()])


class NewSectionForm(Form):
    sec_summary = StringField('Section Summary', validators=[InputRequired()])
    entries = FieldList(FormField(NewEntryForm), min_entries=1)
    # entry_form = FormField(NewEntryForm)


class NewCitationForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    volume = StringField('Volume')
    edition = StringField('Edition')
    author = StringField('Author')
    publisher = StringField('Publisher')
    yr_published = IntegerField('Year Published')
    url = StringField('URL')
    lccn = StringField('Library of Congress Call Number')
    yr_accessed = IntegerField('Year First Accessed')
    summary_status = SelectField('Summary Status', choices=[
                                 (s, s) for s in Citation.sum_states])
    sections = FieldList(FormField(NewSectionForm),
                         min_entries=1)
    # section_form = FormField(NewSectionForm)
