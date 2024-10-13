# Backend_FMTPLA

## _Test Purpose Only Repos_

This repository contains my files for the backend services to make an API, store data to databases via API in Mobile App. This Backend Service fully created using Python Fast API. Another Configuration can be looked at .env.example for database connection. Public resource that i've used is from flickr public feed for photos with Atom format.

## _How to Run_

#### 1. Clone this Repo

#### 2. Python Installed in the OS

#### 3. Create the Environment for your python app

```sh
python -m virtualenv env
```

#### 4. Activate the Env

```sh
# For Windows
./env/Scripts/activate
```

```sh
# For Mac/Unix/Linux
source env/bin/activate
```

#### 5. Install The Library

```sh
python -m pip install -r requirements.txt
```

#### 6. Configure the dotenv

You should check your DB Connection rist and create table user_history in your db as database.py

#### 7. ✨Run the Application✨

```sh
fastapi dev main.py
```

## _Result_

```console
INFO     Using path main.py
INFO     Resolved absolute path [path to your directory]\main.py
INFO     Searching for package file structure from directories with __init__.py files
INFO     Importing from [path to your directory]

 ╭─ Python module file ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯

INFO     Importing module main
INFO     Found importable FastAPI app

 ╭─ Importable FastAPI app ─╮
 │                          │
 │  from main import app    │
 │                          │
 ╰──────────────────────────╯

INFO     Using import string main:app

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: [path to your directory]
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [8688] using WatchFiles
INFO:     Started server process [15084]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

If you already see the page above in your CLI, it means the program run normally. You can check the docs for the documentation of the API and test the API quickly.

## Screenshots

![App Screenshot](https://i.ibb.co.com/GPjnMBs/image.png)
