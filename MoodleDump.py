import wget
import json
import requests, ssl
import getpass
import os
import re
import urllib
from urllib.parse import urlparse

working_directory = "MoodleDump v1"
ssl._create_default_https_context = ssl._create_unverified_context
api_base_url = "https://moodle.upm.es/titulaciones/oficiales/" 

def downloadfile(url):
    try:
        wget.download(url)
    except Exception as e:
        print("\nError downloading: " + url)
        print(e)
        os.system("echo '" + url + "' >> LogErrors")

def authentication(user, password):
    response = requests.post(api_base_url + "/login/token.php?username=" + user 
                                          + "&password=" + password
                                          + "&service=moodle_mobile_app")
    json_data = json.loads(response.text)
    return json_data['token']

def getuserid(token):
    response = requests.post(api_base_url + "webservice/rest/server.php?moodlewsrestformat=json"
                                          + "&moodlewssettingfilter=true&moodlewssettingfileurl=true"
                                          + "&wsfunction=core_webservice_get_site_info"
                                          + "&wstoken=" + token)
    json_data = json.loads(response.text)
    return str(json_data['userid'])

def gcoursescfolders(token, userid):
    response = requests.post(api_base_url + "webservice/rest/server.php?moodlewsrestformat=json"
                                          + "&moodlewssettingfilter=true&moodlewssettingfileurl=true"
                                          + "&wsfunction=core_enrol_get_users_courses"
                                          + "&wstoken=" + token
                                          + "&userid=" + userid)
    json_data = json.loads(response.text)
    courses = []
    for line in json_data:
        course = str(line['id'])
        directory = line['shortname']
        courses.append(course)
        if not os.path.exists(directory):
            os.makedirs(directory)
            olddirectory=os.getcwd()
            os.chdir(directory)
            print("\nWorking on: " + directory)
            downloadcontent(course,token)
            os.chdir(olddirectory)

def downloadcontent(course, token):
    response = requests.post(api_base_url + "webservice/rest/server.php?moodlewsrestformat=json"                                          + "&courseid=" + course
                                          + "&moodlewssettingfilter=true"
                                          + "&moodlewssettingfileurl=true"
                                          + "&wsfunction=core_course_get_contents"
                                          + "&wstoken=" + token
                                          + "&courseid=" + course)

    json_data = json.loads(response.text)
    pattern_field =   '"fileurl": *"[^"]*"'
    pattern_url = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    fileurls = re.findall(pattern_field, json.dumps(json_data))
    urls = re.findall(pattern_url,''.join(str(e) for e in fileurls))
    for url in urls:
        if(urlparse(url).hostname == "moodle.upm.es"):
            downloadfile(url + "&token=" + token)
    

if __name__ == '__main__':
    MoodleDump = """
    ___  ___                _ _     ______                       
    |  \/  |               | | |    |  _  \                      
    | .  . | ___   ___   __| | | ___| | | |_   _ _ __ ___  _ __  
    | |\/| |/ _ \ / _ \ / _` | |/ _ \ | | | | | | '_ ` _ \| '_ \ 
    | |  | | (_) | (_) | (_| | |  __/ |/ /| |_| | | | | | | |_) |
    \_|  |_/\___/ \___/ \__,_|_|\___|___/  \__,_|_| |_| |_| .__/ 
                                                          | |    
                                                          |_|    
    """
    print(MoodleDump)

    print("Email: ")
    user = input()
    password = getpass.getpass("Password: ")

    token = authentication(user, password)
    userid = getuserid(token)

    os.makedirs(working_directory)
    os.chdir(working_directory)

    gcoursescfolders(token, userid)