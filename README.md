# PHOTO CONTEST API 📸

**This README will get you started and guide you through the project**

## Description

Photo contest API is an API for the Runtime Revolution photo contest that takes place every month and aims to allow a fair and easy voting for all participants.

## Table of Contents

- [PHOTO CONTEST API 📸](#photo-contest-api-)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Setup Time](#setup-time)
    - [Prerequisites -](#prerequisites--)
    - [Configuration - Setting your python version](#configuration---setting-your-python-version)
    - [Configuration - Using poetry for package and dependency management](#configuration---using-poetry-for-package-and-dependency-management)
    - [Running the Project](#running-the-project)
  - [Running Tests](#running-tests)
    - [TLDR;](#tldr)
    - [Setting up localstack s3 to fake Aws](#setting-up-localstack-s3-to-fake-aws)
    - [Nice to Have](#nice-to-have)
      - [Direnv](#direnv)
  - [Guidelines](#guidelines)
    - [Branch Naming](#branch-naming)
  - [Who do I talk to?](#who-do-i-talk-to)
  - [Data model](#data-model)
  - [FAQ](#faq)
    - [Macos m1](#macos-m1)
      - [gdal related error](#gdal-related-error)

## Setup Time

### Prerequisites - 

Install [pyenv](https://github.com/pyenv/pyenv) and [poetry](https://python-poetry.org/docs/#installation)

If you have this one already, you can jump to the next section [(Configuration - Setting your python version)](#configuration---setting-your-python-version).

### Configuration - Setting your python version

- Now that you have pyenv, install the version we want to use:

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

  *To use poetry, we will need to have ***python 3.5 or greater***.*

- Now let's start by always activating a virtual environment to work on when we open the project:
    If you need to get out of this virtual environment just type **deactivate**

    ```bash
    poetry shell
    ```

- You should have a file called pyproject.toml, with it we can install everything that is needed!
  Just a second, make sure you are on your project folder! Let's go and install everything now:

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
    Press Enter and you'r done! Now vscode will use this one.

### Running the Project

*Now, how can we run the app?*

To start the docker container run
  ```bash
    make up
  ```
After that run the migrations if needed
  ```bash
    make migrate
  ```
Finally run the app

  ```bash
    make run
  ```

Perfect! You are now running the project locally and you can now start coding!

## Running Tests

To run the tests, inside your working environment run:
  ```bash
    make test
  ```

To add tests remember that the python automatic discover only works properly for files named "test_*.py".

If you want to use the vscode debugger for a particular test you can use the launch.json.example, rename it launch.json
and place it in the .vscode folder in the root of your working directory.

### TLDR;

Check what's available in the Makefile.

Python 3.10.13 environment must exist and be active. Use poetry shell for this.
  ```bash
    make up
    make migrate
    make run
  ```

### Setting up localstack s3 to fake Aws

After you have installed Docker we will need to install AWS CLI. Even though we are simulating
the AWS, we will require this to comunicate with the docker containers:
  1. Install [AWS CLI](https://aws.amazon.com/cli/)
  2. After it is installed we will need to supply credentials, even if the
    credentials are dummies. Localstack requires this details to be present. For that run the command:
      ```bash
        aws configure
      ```

### Nice to Have

Well, hello there! If you are looking for automation, you have come to the right place!

#### Direnv

Looking for a way to start your venv by doing... nothing!?
I know i know, it looks almost like magic. Let me tell you about direnv

- direnv will load and unload a virtual environment everytime we enter or leave the folder
  How do we install it? Let's take a look.

    1. Let's start by creating an empty file called .envrc

    2. Now we can download direnv [here](https://direnv.net/docs/installation.html)

    3. Hook it into your shell like [this](https://direnv.net/docs/hook.html)

    4. Alright and finally add the following to your .envrc:

        `layout pyenv 3.10.4`
        Note: Everytime you edit your .envrc file direnv will ask you to give permission by typing:
        `direnv allow`

    5. ***Important: Now that you changed for direnv replicate the python interpreter change that you did in poetry section***

    6. Reload your shell and you'r set! Now you can leave your folder and come back inside to test if .direnv will show up (thats your new venv).
    Everytime you go into or out of your project folder .direnv will activate or deactivate!
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

## Data model

The data model for this project is as follows:

<!-- ![Data Model](/revent-api/Documentation/DataModel.png) -->

```mermaid
classDiagram
    User <|-- Collection
    User <|-- Picture
    PictureComment <|-- Picture
    Contest <|-- Picture
    Contest <|-- ContestSubmission
    Contest <|-- User
    ContestSubmission <|-- User
    PictureComment <|-- User
    Collection <|-- Picture
    ContestSubmission <|-- Picture

    class User{
      +String email
      +String name_first
      +String name_last
      +Picture profile_picture
      +DateTime profile_picture_updated_at
      +String user_handle
      
    }
    class Picture{
      +User User
      +String picture_path
      +User likes
    }
    class PictureComment{
      +User user
      +Picture picture
      +String text
      +DateTime created_at
    }
    class Collection{
      +String name
      +User user
      +Picture pictures
    }
    class Contest{
        +String title
        +String description
        +Picture cover_picture
        +String prize
        +Boolean automated_dates
        +DateTime upload_phase_start
        +DateTime upload_phase_end
        +DateTime voting_phase_end
        +User winners
        +User created_by

    }
    class ContestSubmission{
        +Contest contest
        +Picture picture
        +DateTime submission_date
        +User votes
    }
    
``````

## FAQ

### Macos m1

#### gdal related error

When experiencing an error such as the one below:

```bash
OSError: dlopen(/usr/local/lib/libgdal.dylib, 0x0006): Symbol not found: __ZN3Aws6Client19ClientConfigurationC1Ev
  Referenced from: <94E9B77D-69B0-39FF-BF05-8494E3AB846D> /usr/local/Cellar/apache-arrow/12.0.1_4/lib/libarrow.1200.1.0.dylib
  Expected in:     <D3694CDE-733E-33BE-9C47-F7B918E1764B> /usr/local/Cellar/aws-sdk-cpp/1.11.145/lib/libaws-cpp-sdk-core.dylib
```

> The solution considers you are using Rosetta in your terminal

Try to reinstall gdal.

1. Check it is installed

```bash
brew list
```

2. Remove it

```bash
brew remove gdal
```

3. Install it

```bash
brew install gdal
```

