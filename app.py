# ----- [///// IMPORTS /////] -----
from flask import Flask, request, render_template, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from config import app, db
from models import Citation, Section, Entry, NewCitationForm, NewEntryForm, NewSectionForm


# ----- [///// FUNCTIONS /////] -----
def create_models():
    db.drop_all()
    db.create_all()
    print('models created')


# ----- [///// PREP /////] -----
create_models()


# ----- [///// ROUTES /////] -----
@app.route('/', methods=['GET', 'POST'])
def main():
    form = NewCitationForm()

    if form.validate_on_submit():
        # citation data
        title = form.title.data
        volume = form.volume.data
        edition = form.edition.data
        author = form.author.data
        publisher = form.publisher.data
        yr_published = form.yr_published.data
        url = form.url.data
        lccn = form.lccn.data
        yr_accessed = form.yr_accessed.data
        summary_status = form.summary_status.data

        new_citation = Citation(title=title,
                                volume=volume,
                                edition=edition,
                                author=author,
                                publisher=publisher,
                                yr_published=yr_published,
                                url=url,
                                lccn=lccn,
                                yr_accessed=yr_accessed,
                                summary_status=summary_status)
        db.session.add(new_citation)

        for section in form.sections.data:
            new_section = Section(**section)
            db.session.add(new_section)

            for entry in form.entries.data:
                new_entry = Entry(**entry)
                db.session.add(new_entry)
                new_section.entries.append(new_entry)

            new_citation.sections.append(new_section)

        db.session.commit()
        citations = Citation.query

        return render_template('new.html', form=form, citations=citations)

    return render_template('new.html', form=form)
