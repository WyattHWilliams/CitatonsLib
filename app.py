# ----- [///// IMPORTS /////] -----
from flask import Flask, request, render_template, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from config import app, db
from models import Citation, Section, Entry, NewCitationForm, NewEntryForm, NewSectionForm
from wtforms import SubmitField


# ----- [///// FUNCTIONS /////] -----
def create_models():
    db.drop_all()
    db.create_all()
    print('models created')


# ----- [///// PREP /////] -----
create_models()


# ----- [///// ROUTES /////] -----
@app.route('/')
def home():
    citations = Citation.query.all()
    return render_template('home.html', citations=citations)


@app.route('/add_citation', methods=['GET', 'POST'])
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
            print('***********************')
            print(section)
            new_section = Section(sec_summary=section['sec_summary'])
            db.session.add(new_section)

            for entry in section['entries']:
                print('************************')
                print(entry)
                new_entry = Entry(page_start=entry['page_start'],
                                  paragraph_start=entry['paragraph_start'],
                                  page_stop=entry['page_stop'],
                                  paragraph_stop=entry['paragraph_stop'],
                                  content=entry['content'])
                db.session.add(new_entry)
                new_section.entries.append(new_entry)

            new_citation.sections.append(new_section)

        db.session.commit()
        citations = Citation.query

        return redirect('/')

    return render_template('new.html', form=form)
