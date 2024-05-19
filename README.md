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
    -Base Template:
        This is the skeleton of our app. It includes the navigation bar and handles messages that pop up when you perform actions like logging in or posting a picture.
    -Home Page:
        This is your starting point. It features a carousel with a welcome message, prompts to sign up, and links to explore our gallery.
    -Login Page:
        If you have an account, log in here to start sharing and interacting.
    -Signup Page:
        New here? Create an account easily and join our community.
    -Profile Page:
        This is your personal space. It shows your submissions, your followers, and the people you’re following. You can also edit your profile here.
    -Edit Profile Page:
        Update your username, bio, and other details to keep your profile fresh.
    -Gallery Page:
        Explore a wide range of images shared by our community. It’s a great place to find inspiration and see what others are up to.
    -Gallery Tags Page:
        Looking for something specific? Check out images tagged with your favorite keywords.
    -Create Post Page:
        Share your latest creation by uploading an image, adding a caption, and tagging it.
    -Search Page:
        Find other users or tags that interest you. It’s a handy tool to discover new content and connections.
    -View Post Page:
        Dive into a single post to see the image in detail, read the caption, and check out the comments.
### Usage

-With PicTalk, you can:

- **Create and Manage Accounts**: Signing up and managing your account is a breeze. Customize your profile to make it your own.
- **Upload Pictures**: Share your favorite moments and artistic creations. Add titles and descriptions to give context to your posts.
- **Comment and Interact**: Dive into discussions, leave comments, and connect with other users. It’s all about building a community.
- **Explore Content**: Browse the homepage to discover fresh and popular pictures. Our gallery is full of inspiration and new perspectives.

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
Ensure you have a .flaskenv file in main directory with the following line:
FLASK_APP=picTalk.py

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
