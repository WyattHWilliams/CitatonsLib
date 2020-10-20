# ----- [///// IMPORTS /////] -----
from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField, FormField, IntegerField, FieldList, SubmitField
from wtforms.validators import InputRequired, Optional
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
    edition = db.Column(db.Text,
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
                                   db.ForeignKey('citations.id'),
                                   nullable=False)
    sec_title = db.Column(db.Text)
    sec_summary = db.Column(db.Text)
    # entries = db.relationship('Entry', backref='sections')

    # relationships
    citation = db.relationship('Citation', backref=db.backref(
        'sections',  cascade="all,delete", lazy='dynamic', collection_class=list))


class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    page_start = db.Column(db.Text,
                           default=0)
    paragraph_start = db.Column(db.Text,
                                default=0)
    page_stop = db.Column(db.Text,
                          default=0)
    paragraph_stop = db.Column(db.Text,
                               default=0)
    content = db.Column(db.Text)
    parent_section_id = db.Column(db.Integer,
                                  db.ForeignKey('sections.id'),
                                  nullable=False)

    # relationships
    section = db.relationship('Section', backref=db.backref(
        'entries', cascade="all,delete", lazy='dynamic', collection_class=list))
    # tags = db.relationship('Tag', secondary='assigned_tags',
    #                        backref='entries', cascade="all,delete")
    # referenced_citations = db.relationship('Citation', backref='entries')


class NewEntryForm(Form):
    page_start = IntegerField('From Page', validators=[Optional()], render_kw={
        "placeholder": "Pg."})
    paragraph_start = IntegerField('Paragraph', validators=[Optional()], render_kw={
        "placeholder": "pr."})
    page_stop = IntegerField('To Page', validators=[Optional()], render_kw={
        "placeholder": "Pg."})
    paragraph_stop = IntegerField('Paragraph', validators=[Optional()], render_kw={
        "placeholder": "pr."})
    content = StringField('Entry')


class NewSectionForm(Form):
    sec_title = StringField('Section Title', validators=[InputRequired()], render_kw={
        "placeholder": "Section Title"})
    sec_summary = StringField('Section Summary', render_kw={
        "placeholder": "Seciton Summary"})
    entries = FieldList(FormField(NewEntryForm), min_entries=0)
    # entry_form = FormField(NewEntryForm)


class NewCitationForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()], render_kw={
                        "placeholder": "Title"})
    volume = StringField('Volume')
    edition = StringField('Edition')
    author = StringField('Author')
    publisher = StringField('Publisher')
    yr_published = IntegerField('Year Published', validators=[Optional()])
    url = StringField('URL')
    lccn = StringField('Library of Congress Call Number')
    yr_accessed = IntegerField('Year First Accessed', validators=[Optional()])
    summary_status = SelectField('Summary Status', choices=[
                                 (s, s) for s in Citation.sum_states])
    sections = FieldList(FormField(NewSectionForm),
                         min_entries=0)
    # section_form = FormField(NewSectionForm)


class WikiUrlForm(FlaskForm):
    url = StringField('URL', validators=[InputRequired()])


class SearchForm(FlaskForm):
    search = StringField('Search')
