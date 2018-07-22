# Project 3

In this project we revisit the National Parks Service [Civil War Battlefields](
https://archive.org/details/CivilWarBattleSummariesOfMajorBattles) dataset.
You will build a web app to interface with the NPS data, including the 
database backend, a tornado web app to serve the data, and a client-side dynamic
interface using Bootstrap and JQuery.

This repository contains the following components:

  - `battlefields/`

    - `__init__.py` - empty, so we can use the directory as a package

    - `db.py` - this python module will contain the database functionality
  
  - `data/`

    - `battles.db` - this file doesn't exist yet, but your database module should
       create it here to contain the sqlite database.
  
    - `nps_battlefields.json` - this file contains a lightly-modified version
      of the NPS dataset.
      
  - `web_content/` - this directory contains content served by tornado
  
    - `css/` - css stylesheets
    
      - `style.css` - a blank stylesheet for you to fill in as needed
    
    - `html/` - tornado templates
    
      - `search.html` - this is the only template we'll need. Your HTML goes 
        here
    
    - `img/` - static image files
    
      - `favicon.png` - a "favicon" image for browsers to add to their bookmarks
    
    - `js/` - javascript
    
      - `battlefields.js` - this should contain all the custom code for your
        client-side frontend

    - `README.md` - these instructions
    
    - `web.py` - the tornado app. This is where you'll add your server-side 
      python code in order to serve requests for the data made by the web
      frontend.
  
## Activities

These are the tasks you'll need to complete to get the app working, according to
the files you'll need to modify.

### battlefields/db.py

This provides the basic database functionality. You need to add the following
features. Look for `#TODO` sections in the code.

1. `__init__()`

  - create a connection to the database
  
  - call the methods to create and populate the table

  
2. `_create_table()`

  - Use SQL to create the table. Remember to consider the case where there's
    already a table and/or data in the database
    
3. `_populate_table()`

  - Fill the table using data from the JSON file
  
4. `search()`

  - a search method that returns battles matching `name` AND `state` criteria
    passed as arguments.
    
5. `detail()`

  - this method returns the complete record for a single battle, specified by
    `battle_id`.
    
6. `states()`

  - this method returns a list of all possible values for the `state` column.
  
  - I think it's easier if you parse the rows here and have this method return 
    just a list of states as strings, rather than the list of rows that comes
    back from `cur.execute()`

### web.py

This is your Tornado app. It's job is mostly to serve the data, but it also
renders the basic form of the main page as HTML, and serves the JavaScript used
to build the dynamic interface.

1. `MainHandler` - render `search.html`

2. `StatesHandler` - send the client a JSON dictionary.

   - key is `data`
   
   - value is a list of states as strings
   
3. `SearchHandler` - perform a search

   - get params from web interface

   - return results in a JSON dictionary
   
   - key is `data`
   
   - value is the list of rows
   
4. `DetailHandler` - return a single record by id

  - get id from web interface
  
  - return results in a JSON dictionary
  
  - key is `data`
  
  - value is the single row

5. Application definition

  - hook up the handlers you've created to appropriate URLS
     
     - `/` -> MainHandler
     
     - `/states` -> StatesHandler
     
     - `/search` -> SearchHandler
     
     - `/detail` -> DetailHandler

### web_content/js/battlefields.js

This file provides the JavaScript functions that are used in building the 
client-side interface.

1. `states_list(json)` - this function uses JSON data to build the `#states` dropdown:

    - it will be the callback passed in a `$.get` statement requesting `/states`

    - iterate over the returned list of states
    
    - add `<option>` elements to `#states`
      
2. `results_table` - this function uses JSON data to build a results table

    - it will be the callback for a `$.get` statement requesting `/search`
    
    - create the new table
    
    - give it a thead, tbody
    
    - add a header row
    
    - build the tbody rows by iterating over the JSON list of results
    
    - replace the contents of `#results_col` with the new table
    
3. `start_search` - this is a wrapper for `results_table`

   - it is what gets called when you click the button to submit the search
   
   - it performs the `$.get` statement and attaches `results_table` as the 
     callback to invoke once the data has been received
     
4. `display_details` - this function uses JSON data to fill in the `#details`
    modal
    
      - it will be the callback for a `$.get` statement requesting `/detail`
      
      - note: the `#details` modal is invisible until `.modal()` is invoked,
        then it fills the screen like a dialog box
        
5. `get_details` - this is a wrapper for `display_details`

      - it does `$.get` to request `/detail` for a given `battle_id`
      
      - attaches `display_details` as the callback

6. anonymous function attached to `document.ready`

   - build the dropdown
   
   - attach `start_search` to the form's `submit` event
   
      - this will be triggered when someone clicks the button
      
      - or when they type ENTER inside the text box
      
### web_content/html/search.html

1. Add the form 

   - a text box called `#battle`
   
   - a dropdown called `#state`
   
   - a submit button called `#search_btn`
