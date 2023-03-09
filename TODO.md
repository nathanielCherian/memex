# 3/10/22
- Clean up a little bit
- Sanitize sql data
- Add quick search to tests
- Powersearch without -p
    - I want this to search all string columns
- Adding column for date
- Make date a searchable column
- Plugins maybe? How would I do this?

# 1/5/22
- sanitize sql data
- Powersearch without -p option
    - Right now it only searches keywords field, should I change this
- Re-test the api stuff
    - Am I accessing database correctly?
    - Standardize parameters for requests
- Plugins
    - How do I want to implement user created plugins
        - Is there an efficent and safe way to do this
    - Where are plugins stored
    - How are plugins triggered
    

# TODO as of 10/15/22
- ~~Make session/entry object based~~
~~- more powerful searching~~
- ~~test mode~~ 
- santize SQL data
~~- add tests for power search~~
~~- add example to readme for power search~~
~~- debug power search~~
    ~~- Throw proper errors~~
    ~~- add comparisons~~

- limited number of entries shown from list
    - Maybe show from most recent to oldest
    - Variable config file
- add logging to api 
- change naming of "power"
- Improve power search functionality!
    - comparisons for numbers
    - Standardize constants/enums
- display entry in tuple form clihandler


Older stuff
- verbose error messages
- backups for database
- ~~logging~~
- Database ~~to~~/from csv
- ~~enhance CLI~~, ~~more detailed help~~
- ~~add flags to certain CLI commands~~
    - ~~search~~
- ~~black code formatting~~
- Options/plugins for filing
- ~~create .memex config file~~

## Noble Recomended Fixes
- ~~remove requirements~~
- ~~run testing through tox~~
    - ~~black~~
    - ~~isort~~
    - *flake8*
    - *pylint*
- ~~Make testing run api before starting~~
- Enhance README
    - "dev status"
    - installation instructions
- Find permament location for Database
- ~~rename .memex to .memexrc~~
- ~~Move CLI code from bin script to library~~
- ~~rename servercli to memex_api~~
