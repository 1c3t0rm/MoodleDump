# MoodleDump 

A Python 3 script based on the Web service [API functions OF Moodle](https://docs.moodle.org/dev/Web_service_API_functions), in its first version just download everything without folders of your courses.

## How to Run

You must have installed wget.

    pip install wget

Then:

    git clone https://github.com/1c3t0rm/MoodleDump.git
    //Must edit endpoint of your Moodle first...
    python3 MoodleDump.py

## Usage

Just insert your Moodle credentials and let it RUN :)

## Additional Info
Maybe some 404 errors that should not appear since they are false positives, will be fixed...
Meanwhile, if an error occurs, a file will be created in the corresponding course folder with links that have suffered an error.

## TO-DO
- Fix 404 errors.
- Add contents folders.**
- Just download a course.**
