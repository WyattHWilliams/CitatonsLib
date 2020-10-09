# ----- [///// IMPORTS /////] -----
from itertools import zip_longest
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


@app.route('/edit/<int:cit_id>', methods=['GET', 'POST'])
def edit_citation(cit_id):
    cit = Citation.query.get_or_404(cit_id)
    form = NewCitationForm(obj=cit)

    if form.validate_on_submit():
        cit.title = form.title.data
        cit.volume = form.volume.data
        cit.edition = form.edition.data
        cit.author = form.author.data
        cit.publisher = form.publisher.data
        cit.yr_published = form.yr_published.data
        cit.url = form.url.data
        cit.lccn = form.lccn.data
        cit.yr_accessed = form.yr_accessed.data
        cit.summary_status = form.summary_status.data

        for sec, section in zip_longest(cit.sections, form.sections.data, fillvalue=None):
            if sec == None:
                new_section = Section(sec_summary=section['sec_summary'])
                db.session.add(new_section)

                for entry in section['entries']:
                    new_entry = Entry(page_start=entry['page_start'],
                                      paragraph_start=entry['paragraph_start'],
                                      page_stop=entry['page_stop'],
                                      paragraph_stop=entry['paragraph_stop'],
                                      content=entry['content'])
                    db.session.add(new_entry)
                    new_section.entries.append(new_entry)

                cit.sections.append(new_section)

            else:
                sec.sec_summary = section['sec_summary']

                for ent, entry in zip_longest(sec.entries, section['entries'], fillvalue=None):
                    if ent == None:
                        new_entry = Entry(page_start=entry['page_start'],
                                          paragraph_start=entry['paragraph_start'],
                                          page_stop=entry['page_stop'],
                                          paragraph_stop=entry['paragraph_stop'],
                                          content=entry['content'])
                        db.session.add(new_entry)
                        sec.entries.append(new_entry)

                    else:
                        ent.page_start = entry['page_start']
                        ent.paragraph_start = entry['paragraph_start']
                        ent.page_stop = entry['page_stop']
                        ent.paragraph_stop = entry['paragraph_stop']
                        ent.content = entry['content']

        db.session.commit()
        return redirect('/')

    return render_template('edit.html', form=form, citation=cit)
