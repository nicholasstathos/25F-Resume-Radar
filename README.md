# Fall 2025 CS 3200 Project - ResumeRadar

This is the project repo for Neil Sridhar, Nick Stathos, and Amir Ablassanov's Fall 2025 CS 3200 Course Project.

ResumeRadar is a database-driven application that analyzes resumes and provides insights for job seekers and recruiters.

## Prerequisites

- A GitHub Account
- A terminal-based git client or GUI Git client such as GitHub Desktop or the Git plugin for VSCode.
- A distribution of Python running on your laptop. The distribution supported by the course is [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install).
  - Create a new Python 3.11 environment in `conda` named `db-proj` by running:  
     ```bash
     conda create -n db-proj python=3.11
     ```
  - Install the Python dependencies listed in `api/requirements.txt` and `app/src/requirements.txt` into your local Python environment. You can do this by running `pip install -r requirements.txt` in each respective directory.
     ```bash
     cd api
     pip install -r requirements.txt
     cd ../app
     pip install -r requirements.txt
     ```
     Note that the `..` means go to the parent folder of the folder you're currently in (which is `api/` after the first command)
- VSCode with the Python Plugin installed
  - You may use some other Python/code editor. However, Course staff will only support VS Code.

## Structure of the Repo

- This repository is organized into five main directories:
  - `./app` - the Streamlit app
  - `./api` - the Flask REST API
  - `./database-files` - SQL scripts to initialize the MySQL database
  - `./datasets` - folder for storing datasets

- The repo also contains a `docker-compose.yaml` file that is used to set up the Docker containers for the front end app, the REST API, and MySQL database.

## Project Overview

ResumeRadar processes and analyzes resume data to help match candidates with job opportunities. The application features:

- Resume parsing and data extraction
- Skills and experience analysis
- Job matching recommendations
- Database-driven search functionality
- Interactive data visualizations
- Role-based access control for different user types

## Setting Up the Repo

**Before you start**: You need to have a GitHub account and a terminal-based git client or GUI Git client such as GitHub Desktop or the Git plugin for VSCode.

1. Clone this repo to your local machine.
   1. You can do this by clicking the green "Code" button on the top right of the repo page and copying the URL. Then, in your terminal, run `git clone <URL>`.
   1. Or, you can use the GitHub Desktop app to clone the repo.
1. Open the repository folder in VSCode.
1. Set up the `.env` file in the `api` folder based on the `.env.template` file.
   1. Make a copy of the `.env.template` file and name it `.env`. 
   1. Open the new `.env` file. 
   1. On the last line, delete the `<...>` placeholder text, and put a password. Don't reuse any passwords you use for any other services (email, etc.)
1. For running the containers:
   1. `docker compose up -d` to start all the containers in the background
   1. `docker compose down` to shutdown and delete the containers
   1. `docker compose up db -d` only start the database container (replace db with api or app for the other two services as needed)
   1. `docker compose stop` to "turn off" the containers but not delete them.

**Note:** You can also use the Docker Desktop GUI to start and stop the containers after the first initial run.

## Important Tips

1. In general, any changes you make to the api code base (REST API) or the Streamlit app code should be *hot reloaded* when the files are saved. This means that the changes should be immediately available.  
   1. Don't forget to click the **Always Rerun** button in the browser tab of the Streamlit app for it to reload with changes. 
   1. Sometimes, a bug in the code will shut the containers down. If this is the case, try and fix the bug in the code. Then you can restart the `web-app` container in Docker Desktop or restart all the containers with `docker compose restart` (no *-d* flag). 
1. The MySQL Container is different. 
   1. When the MySQL container is ***created*** the first time, it will execute any `.sql` files in the `./database-files` folder. **Important:** it will execute them in alphabetical order.  
   1. The MySQL Container's log files are your friend! Remember, you can access them in Docker Desktop by going to the MySQL Container, and clicking on the `Logs` tab. If there are errors in your .sql files as it is trying to run them, there will be a message in the logs. You can search 🔍 for `Error` to find them more quickly. 
   1. If you need to update anything in any of your SQL files, you **MUST** recreate the MySQL container (rather than just stopping and restarting it). You can recreate the MySQL container by using the following command: `docker compose down db -v && docker compose up db -d`. 
      1. `docker compose down db -v` stops and deletes the MySQL container and the volume attached to it. 
      1. `docker compose up db -d` will create a new db container and re-run the files in the `database-files` folder.

## Team Members

- Neil Sridhar
- Nick Stathos
- Amir Ablassanov

## Project Demo

