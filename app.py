# ----- [///// IMPORTS /////] -----
import datetime
from itertools import zip_longest
from wiki import check_wiki_exist, fetch_wiki_data, make_printable, excluded_sections
from flask import Flask, request, render_template, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from config import app, db
from models import Citation, Section, Entry, NewCitationForm, NewEntryForm, NewSectionForm, WikiUrlForm, SearchForm
from wtforms import SubmitField


# ----- [///// FUNCTIONS /////] -----
def create_models():
    db.drop_all()
    db.create_all()
    print('models created')


# ----- [///// PREP /////] -----
create_models()


# ----- [///// ROUTES /////] -----
@app.route('/', methods=['GET', 'POST'])
def home():
    citations = Citation.query.all()
    form = SearchForm()

    if form.validate_on_submit():
        search = form.search.data
        search_params = search.split()
        results = []
        r1 = db.session.query(Entry).filter(
            Entry.content.like(f'%{search_params[0]}%'))
        r2 = db.session.query(Entry).filter(
            Entry.content.like(f'%{search_params[0].capitalize()}%'))

        for r in r1:
            results.append(r)
        for r in r2:
            results.append(r)

        return render_template('home.html', form=form, citations=citations, search_results=results)
    else:
        return render_template('home.html', form=form, citations=citations)


@ app.route('/add_citation', methods=['GET', 'POST'])
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
            new_section = Section(sec_summary=section['sec_summary'],
                                  sec_title=section['sec_title'])
            db.session.add(new_section)

            for entry in section['entries']:
                new_entry = Entry(page_start=entry['page_start'],
                                  paragraph_start=entry['paragraph_start'],
                                  page_stop=entry['page_stop'],
                                  paragraph_stop=entry['paragraph_stop'],
                                  content=entry['content'])
                db.session.add(new_entry)
                new_section.entries.append(new_entry)

            new_citation.sections.append(new_section)

        db.session.commit()

        return redirect('/')

    return render_template('new.html', form=form)


@ app.route('/add_wiki/url', methods=['GET', 'POST'])
def get_wiki_url():
    form = WikiUrlForm()

    if form.validate_on_submit():
        session['wikiPage'] = form.url.data.split('/')[-1]
        if check_wiki_exist(session['wikiPage']) == True:
            return redirect('/add_wiki')
        else:
            error = 'Wiki page does not exist'
            return render_template('get_url.html', form=form, error=error)

    return render_template('get_url.html', form=form)


@ app.route('/add_wiki', methods=['GET', 'POST'])
def add_wiki():
    page = fetch_wiki_data(session['wikiPage'])
    new_citation = Citation(title=make_printable(page.title),
                            publisher='Wikipedia',
                            url=page.fullurl,
                            yr_accessed=datetime.datetime.now().strftime('%Y'))
    db.session.add(new_citation)

    for page_section in page.sections:
        if page_section.title in excluded_sections:
            continue
        if len(page_section.sections) != 0:
            for subsection in page_section.sections:
                new_section = Section(
                    sec_title=make_printable(page_section.title) + ': ' + make_printable(subsection.title))
                db.session.add(new_section)

                text = subsection.text.split('. ')
                for sentence in text:
                    printable_sentence = make_printable(sentence) + '.'
                    new_entry = Entry(content=printable_sentence)

                    db.session.add(new_entry)
                    new_section.entries.append(new_entry)

                new_citation.sections.append(new_section)

        else:
            new_section = Section(sec_title=make_printable(page_section.title))
            db.session.add(new_section)

            text = page_section.text.split('. ')
            for sentence in text:
                printable_sentence = make_printable(sentence) + '.'
                new_entry = Entry(content=printable_sentence)

                db.session.add(new_entry)
                new_section.entries.append(new_entry)

            new_citation.sections.append(new_section)

    db.session.flush()
    cit = Citation.query.get_or_404(new_citation.id)
    form = NewCitationForm(obj=cit)

    return render_template('new.html', form=form)


@ app.route('/edit/<int:cit_id>', methods=['GET', 'POST'])
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
                new_section = Section(sec_summary=section['sec_summary'],
                                      sec_title=section['sec_title'])
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

            elif section == None:
                db.session.delete(sec)

            else:
                sec.sec_summary = section['sec_summary']
                sec.sec_title = section['sec_title']

                for ent, entry in zip_longest(sec.entries, section['entries'], fillvalue=None):
                    if ent == None:
                        new_entry = Entry(page_start=entry['page_start'],
                                          paragraph_start=entry['paragraph_start'],
                                          page_stop=entry['page_stop'],
                                          paragraph_stop=entry['paragraph_stop'],
                                          content=entry['content'])
                        db.session.add(new_entry)
                        sec.entries.append(new_entry)

                    elif entry == None:
                        db.session.delete(ent)

                    else:
                        ent.page_start = entry['page_start']
                        ent.paragraph_start = entry['paragraph_start']
                        ent.page_stop = entry['page_stop']
                        ent.paragraph_stop = entry['paragraph_stop']
                        ent.content = entry['content']

        db.session.commit()
        return redirect('/')

    return render_template('edit.html', form=form, citation=cit)
