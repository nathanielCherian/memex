# memex

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Your personal database and archive on everything that is meaningful to you.

Quickly find that one gif or blog you saw a month ago through a powerful database search.

The term 'memex' (memory-extension) comes form [Vannevar Bush](https://en.wikipedia.org/wiki/Memex)'s fictional device that would be a *digital searchable record* of our lives.



NOTE: This project is pre-alpha, use at your own risk.

## Installation
Memex uses the [poetry package manager](https://python-poetry.org/). Please install using the directions from their website before continuing

```$ git clone https://github.com/nathanielCherian/memex```

```$ cd memex && poetry install```

```$ poetry shell```

This will activate the poetry virtual enviornment

## Configuration
On running memex for the first time, a configuration file will be created at ```~/.memex```.

## PowerSearch
```$ memex search -p "url='*twitter*'&(keywords="buisness")

## Usage
```$ memex file [url?] [keywords?]```
Stores a new entry to the database. keywords are space-seperated.

```$ memex list```
Shows all entrys in the database

```$ memex search term [-p,--power]```
Returns entries that match the term regex. Use PowerSearch to refine a search.

```$ memex inspect [id]```
Displays full entry of given id.

Memex also comes with an API that allows remote access to the database.

```$ memex-api create [token-name?]```
Creates a new authorization token.

```$ memex-api list```
Lists valid tokens

```$ memex-api revoke [token-id]```
Revokes authorizaiton token.

```$ memex-api start```
Starts the API


## Advanced Usage
Plugins...

![memex data flow diagram](/media/memex-flow.png)


## Testing

```$ poetry run tox ```

## Philosophy
- Lightweight
    - Doesn't need to do everything
    - Simple to use (shouldn't take more than 10 seconds to add an entry)
- Modular
    - The user should be able to choose how they want to expand their memex
    - Modularality through extensions allows bare-minimum functionality or over the top features
- Secure
    - [Privacy](https://userdatamanifesto.org/)
    - Prevent Data loss 
