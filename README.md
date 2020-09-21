
**Note-keeping and Citations Organizer**

I want to be able to keep a collection of summaries, quotes, and notes from various sources organized by topic, source-level, and citation information in a streamlined organizational structure to be used for the rapid drafting of essays.

I imagine the site having two major parts:

A) Entering sources/notes

-   The user inputs the citation information of the source they want to add. Title, author, publisher, url, etc.
    
-   The user is prompted to create a summary for the source. This summary is built out of sections (useful for outlining chapters in a book, or parts of an essay/article). Each summary includes entries and a section summary.
    

-   Entries are for each individual note that the user wishes to remember about the section. Ie. "Page 1, paragraph 3 talks about Theodore Geisel's early work as an ad maker."
    
-   Entries may include references to other sources, and should have a section where the user can list referenced sources. These references could later become their own user-inputed sources with their own summaries.
    
-   The Section summary is a text field that can be used to summarize the collective purpose of the section's entries.
    

-   The user should be able to submit entries and sections at whatever pace they want. I would like to be able to add entries to a source while reading a book or whatever. Therefore, each source should be modular, editable, and able to be saved without completion. This also warrants the use of a summary status like "Not started," "started," "finished" to be tagged onto all entered sources.
    
-   A system of tags should be included to help sort through large amounts of entries or sources.
    

B) Writing with the source library actively available.

-   The user should be able to enter an interface that mainly functions as a text editor. While writing, the backend should be using keyword searches, sentiment analysis, or simple language analysis from home-grown logic or 3rd party api to sort through the user's source library and recommend entries for citation.
    
-   The user should be able to quickly add these citations to the project they're writing in the form of footnotes, endnotes, etc.
    

Various web APIs could be used to generate tags for entries, generate tags for what's being written for the purpose of comparing it to what's being written, or be used to take keyword arguments from the user's writing to search databases like wikipedia or JSTOR for potentially relevant articles.

User's libraries should be private. Nobody likes other people poking around in their notes! Therefore users will login to gain access to their notes libraries.

---

1) What goal will your website be designed to achieve?

The website's primary function will be note-taking and organizing citations. A secondary function will be acting as a site-based text editor that allows the user to interact with the notes and citations they have saved.

2) What kind of users will visit your site?

The primary intended demographic will be students or anyone who does frequent text-based (armchair) research.

3) What data do you plan on using?

Users will have the ability to keep a library of notes, citations, and user-written essays on the site. Users can use tag-based searching to browse through their own notes. While writing, basic key-word recognition will be used to search for relevant user notes.

There will also be functionality for searching free online library sites for relevant articles directly from the essay writing interface.

4) Project creation outline:

		1.  Database schema and model creation for citations, summaries, sections, and note entries.
		    
		2.  Functionality and forms for add/edit citations and citation summaries.
		    
		3.  Tagging models and functionality.
		    
		4.  Searching for notes with specific parameters and tags. Making a search page section and figuring out how to display loads of notes cleanly.
		    
		5.  Making a page for a text editor.
		    
		6.  Adding functionality for analyzing the text editor for relevant keywords to use in a notes search.
		    
		7.  Implementing a search results section into the text editor where the user can easily view their notes while writing.
		    
		8.  Adding one-click functionality for adding a note and particular citation to the users text document.
    

5.  What does your database schema look like?
    

		1.  users(id, username, password, etc.)
		    
		2.  citations(citation information, user)
		    
		3.  Summary sections(parent citation, content, child entries)
		    
		4.  Summary entries(parent citation and section, content, page numbers, paragraph numbers, referenced 3rd party citations)
		    
		5.  Relations tables for users to user-libraries of citations and notes and such.
    

6.  What kinds of issues might you run into with your API?
    

		1.  Formatting content from different sources.
		    
		2.  Finding basic free text analysis tools to pull keywords from user-written documents.
    

7.  Is there any sensitive information you need to secure?
    

		1.  User libraries should be private. No user should be able to see another's notes.
    

7.  What functionality will your app include?
    

		1.  Time travel with dolphins
    

9.  What will the user flow look like?
    

	1.  Add new citation
    

		1.  Modular form for adding citation info and making a summary.
		    
		2.  Users can save this data and return to it any time to continue filling out their notes.
		    
		3.  Modular forms for adding a section and adding an entry.
    

	3.  Search Notes
    

		1.  Search through all of the users notes and essays for keywords/parameters
    

	5.  Write new essay
    

		1.  Text Editor
		    
		2.  Section on text editor page that displays potentially relevant notes.
		    

		1.  One-click functionality for adding a citation to an essay.
		    

		4.  Section on text editor page for searching through notes.
		    

		1.  One-click functionality for adding a citation to an essay.
		    

11.  What features make your site more than CRUD? Do you have any stretch goals?
    
		
		1.  With this modular approach to note-taking and essay writing, the only essential functionally is CRUD; however, what the user does with the tools of the site will explore the vast capabilities of those four simple processes.
    
	 Other goals:
    

		1.  I'd like to expand the functionality to academic debaters. Including a page where arguments could be imputed and relevant notes/essays from the user could be suggested.
		    
		2.  I'd like to add a section where relevant articles from places like wikipedia and jstor are provided to the user.