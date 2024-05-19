# CITS3403 - Group Project

|Student ID|Name|GitHub Username|
|----|----|----|
|23097928|Harsh Chaudhari|harshchaudh|
|23655909|Jay Kim|wwwwvwwwwvvwwwvw|
|23426595|Wesley Dalbock|wdalbock|
|23087371|Jayden Hondris|JaydenHond|


***
# PicTalk
## About
### Purpose
PicTalk is a website designed for photography enthusiasts. Users can upload their own images to share with the community. Other users can then interact with these images by commenting on said images. This in turn provides valuable, constructive feedback to the original user and creates engagment among users.  Overall, PicTalk provides a platform for amatuer photographers to showcase their work and receive feedback from others in the community.

For website's similar to PicTalk, [Instagram](https://www.instagram.com) and [Unsplash](https://unsplash.com/) would be appropriate comparisons, they have similar but opposite purposes, while PicTalk achieves both.

### Design
- **User Interface**: Minimilist layout, a fair portion of the website is whitespace and rarely is the full screen ever used. We've chosen a colour pallete that was visually satisfying. Large and easily identifiable fonts, buttons, links, etc. Small screens like phone screens where taken into consideration and were mostly accomplished automatically by Bootstrap. With the exception of the navigation bar, all aspects of the website function normally on smaller screens. While PicTalk can be viewed on a smaller screen, due to amount of images it may be considered a desktop-first website.

- **Navigation**: The website is fairly simple as all navigatable items are all available to the user on the home page. There's a persistant navigation bar that only changes with the login state of the user. The main content changes as the user visits different sections of the website. All labels and possible links are all fairly clear. Nothing is really hidden away.

- **Pages**
    - Home page - gives a general idea of what PicTalk is about, this can be viewed without logging in.
    - Search page - allows the user to search other users and tags, this can viewed without logging in.
    - Gallery page - displays the latest images posted, this can be viewed without logging in, however, logged in viewers will be able to view images from users whom they follow.
    - Profile page - displays images postsed by that user, a submission, follower and following count. Does not require logging in, however, add a follower feature when users are logged in.
    - Submission page - allows users to post images, with a caption and with a maximum of 5 tags. Requires users to be logged in.
    - Login/Sign up page - allows users to sign up or log in.
### Use
- 

## Architecture

## Getting started
This section details the steps required to deploy the website and complete the necessary tests. The following instructions are for Ubuntu-based Linux distributions; **Ubuntu 22.04.4 LTS** was used specifically. 

### Prerequsites
We'll assume you have the basic software like Python 3. Create a virtual environment,

```cpp
python3 -m venv /path/to/venv

# Example 
python3 -m venv ~/.env

# Activate the virtual environment
source path/to/venv/bin/activate
```

Packages can be installed using the command `pip3 install <<package>>`, where **package** is the package that needs to be installed. Refer to the `requirments.txt` to get a full list of Python packages. To install all packages from `requirements.txt`, navigate to the project directory and run the command,

```
pip install -r requirements.txt
```
Many of the packages listed are not used.

### Deployment
To run the web application, run the command,
```cpp
flask run
```
Or,
```cpp
python3 picTalk.py
```

## Running tests
### Unit tests
Within the tests directory, run the command,
```cpp
python3 unitTests.py
```

### Systems tests
It's advised to collapse all the functions when viewing the source code (on Vscode, the shortcut is `CTRL + K CTRL + 0`). To run the test, navigate to the tests directory, then run `seleniumTests.py`. Failing to navigate to the tests directory, will result in certain tests failing.
```
python3 seleniumTests.py
```

To run a specific test, 
```cpp
# Modify this line:
if __name__ == "__main__":
    unittest.main(verbosity=2)

# Modify it to:
if __name__ == "__main__":
    unittest.main(argv=[''], defaultTest='BasicSeleniumTests.<name_of_test>', verbosity=2)

# For example, to run 'test_submit':
if __name__ == "__main__":
    unittest.main(argv=[''], defaultTest='BasicSeleniumTests.test_submit', verbosity=2)
```
