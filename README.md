# PHOTO CONTEST API 📸

**This README will get you started and guide you through the project**

## Description

Photo contest API is an API for the Runtime Revolution photo contest that takes place every month and aims to allow a fair and easy voting for all participants.

## Setup time

### Prerequisites - Install [pyenv](https://github.com/pyenv/pyenv) and [poetry](https://python-poetry.org/docs/#installation)

If you have this one already, you can jump to the next section (Configuration - Setting your python version).

- Example:
    1. Pyenv
        - We will need to install some dependencies that will also depend on the OS being used.  
          For macOS users:

          ```bash
          brew install openssl readline sqlite3 xz zlib
          ```

        - To initialize the pyenv installer use:

          ```bash
          curl https://pyenv.run | bash
          ```

        - Depending on the shell you'r using, you can see something at the end of this installation like:

          ```bash
          WARNING: seems you still have not added 'pyenv' to the load path.

          Load pyenv automatically by adding the following to ~/.bashrc:

          export PATH="$HOME/.pyenv/bin:$PATH"
          eval "$(pyenv init -)"
          eval "$(pyenv virtualenv-init -)"
          ```  

          You just need to follow the steps above, add the export to your shell file and restart your shell.

    2. Poetry
        - To install poetry, do it by running:

          ```bash
          curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
          ```

        - Once this ends, run this to configure your current shell with the path to poetry:

          ```bash
          source $HOME/.poetry/env
          ```

        - And finally we can confirm you got this installed by running:

          ```bash
          poetry --version
          ```

        - You can also update poetry to the latest stable version:

          ```bash
          poetry self update
          ```

### Configuration - Setting your python version

- Now that you have pyenv, install the version you want to use:

    ```bash
    pyenv install -v 3.10.4
    ```

- Check your list for the installed python version:

    ```bash
    ls ~/.pyenv/versions/
    ```

    or by using

    ```bash
    pyenv versions
    ```

### Configuration - Using poetry for package and dependency management

  *To use poetry, we will need to have ***python 3.5+***.*

- Now lets start by always activating a virtual environment to work on when we open the project:  
    If you need to get out of this virtual environment just type **deactivate**

    ```bash
    poetry shell
    ```

- You should have a file called pyproject.toml, with it we can install everything that is needed!  
  Just a second, make sure you are on your project folder! Lets go and install everything now:

    ```bash
    poetry install
    ```

    This is great! Right now, we have our packages installed!

- One last thing! We still need to tell our IDE to use this new interpreter!  
Alright, and how do we do this? Its easy, really. (This next steps will be for vscode)

    1. Copy the path from the command below:

        ```bash
        poetry env info --path
        ```

    2. In your vscode, go to settings and search for python interpreter

    3. Now select to use a specific path and use the one you just copied  
    Press Enter and you'r done! Now vscode will use this version.

- You can now start using the project, but wait! don't go! Now we have our virtual environment  
  ready, but do you really want to keep activating it everytime you join the project?  
  Lets take a look on how we can automate this and make sure that we use the correct versions each time we are in a new project.
  Let me introduce you to a new section.

### Nice to have  

Well, hello there! If you are looking for automation, you have come to the right place!

#### direnv

Looking for a way to start your venv by doing... nothing!?  
I know i know, it looks almost like magic. Let me tell you about direnv

- direnv will load and unload a virtual environment everytime we enter or leave the folder  
  How do we install it? Lets take a look.

    1. Lets start by creating an empty file called .envrc

    2. Now we can download direnv [here](https://direnv.net/docs/installation.html)

    3. Hook it into your shell like [this](https://direnv.net/docs/hook.html)

    4. Alright and finally add the following to your .envrc:  
    `layout pyenv 3.10.4`  
    Note: Everytime you edit your .envrc file direnv will ask you to give permission by typing:  
    `direnv allow`

    5. Reload your shell and you'r set! Now you can leave your folder and come back inside to test if .direnv will show up (thats your new venv).  
    Everytime you go into or out of your project folder .direnv will activate or deactivate!

## How to run

To run, you can start by putting on some comfortable shoes and then... im just kidding, im just kidding!
Lets start with the prerequisites and then move onto the action.

### Prerequisites - Install [docker](https://docs.docker.com/get-docker/)

If you have this one already, you can jump to the next section (Running the project)

### Running the project

*Now, how can we run the app?*

- Now that u have docker installed we just need to build our image out of  
Dockerfile. Its a little file you have on your project folder that will tell docker  
everything he needs to run and make a new environment just like yours! isnt that awesome?  
I wish we had something like that and didn't had to go through this README 🤔

  ```bash
    docker-compose build
  ```

- Hopefully everything went smooth and we are ready to see how the project is going!  
For us to take a look lets run:

  ```bash
    docker-compose up
  ```

Perfect! You are now running the project locally and you can now start coding!

## Running tests

*Coming with implementation on pytest*

## Guidelines

### Branch Naming

Everytime we need to work on a new feature, bug or any type of task, we need to create a new branch.
Below will be a step by step guide on how we can create and start to work on a task:

The nomenclature for someone named "João Gomes" that need to fix a new "Bug" on a ticket with the ID "1234" and name "Update salary" goes like this:

`jg/bug/1234/Update-salary`

- jg - First and last name initials

- bug - Type of task to be performed

- 1234 - Ticket ID

- Update-salary - Ticket name

## Who do I talk to?

- You can always talk to your Team Leader or the repo owner for any question regarding this project.
