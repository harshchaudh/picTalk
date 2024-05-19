# CITS3403 - Group Project

|Student ID|Name|GitHub Username|
|----|----|----|
|23097928|Harsh Chaudhari|harshchaudh|
|23655909|Jay Kim|wwwwvwwwwvvwwwvw|
|23426595|Wesley Dalbock|wdalbock|
|23087371|Jayden Hondris|JaydenHond|

View Projects/CITS3403 Group Project, to view agile process.

Note: The username and password requirements are never made obvious to the user, view app/utilities.py to see requirements.
***
# PicTalk
## About
### Purpose
PicTalk is a website designed for photography enthusiasts. Users can upload their own images to share with the community. Other users can then interact with these images by commenting on them. This in turn provides valuable, constructive feedback to the original user and creates engagement among users.  Overall, PicTalk provides a platform for amateur photographers to showcase their work and receive feedback from others in the community.

For websites similar to PicTalk, [Instagram](https://www.instagram.com) and [Unsplash](https://unsplash.com/) would be appropriate comparisons, they have similar but opposite purposes, while PicTalk achieves both.

### Design
- **User Interface**: Minimal layout, a fair portion of the website is whitespace; and rarely is the full screen ever used. We've chosen a colour palette that is visually satisfying. Large and easily identifiable fonts, buttons, links, etc. Small screens, like phone screens, were taken into consideration and were mostly accomplished automatically by Bootstrap. While PicTalk can be viewed on a smaller screens, it would still be considered a desktop-first website.

- **Navigation**: The website is fairly simple, as all navigable items are available to the user on the home page. There's a persistent navigation bar that only changes with the login state of the user. The main content changes as the user visits different sections of the website. All labels and possible links are fairly clear.

- **Pages**
    - **Base Template**:
        This is the skeleton of our app. It includes the navigation bar and handles messages that pop up when you perform actions like logging in or posting a picture.
    - **Home Page**:
        This is your starting point. It features a carousel with a welcome message, prompts to sign up, and links to explore our gallery.
    - **Login Page**:
        If you have an account, log in here to start sharing and interacting.
    - **Signup Page**:
        New here? Create an account easily and join our community.
    - **Profile Page**:
        This is your personal space. It shows your submissions, your followers, and the people you’re following. You can also edit your profile here.
    - **Edit Profile Page**:
        Update your username and biography to keep your profile fresh.
    - **Gallery Page**:
        Explore a wide range of images shared by our community. It’s a great place to find inspiration and see what others are up to.
    - **Gallery Tags Page**:
        Looking for something specific? Check out images tagged with your favourite keywords.
    - **Create Post Page**:
        Share your latest creation by uploading an image, adding a caption, and tagging it.
    - **Search Page**:
        Find other users or tags that interest you. It’s a handy tool to discover new content and connections.
    - **View Post Page**:
        Dive into a single post to see the image in detail, read the caption, and check out the comments.
### Usage

With PicTalk, you can:

- **Create and Manage Accounts**: Signing up and managing your account is a breeze. Customize your profile to make it your own.
- **Upload Pictures**: Share your favorite moments and artistic creations. Add titles and descriptions to give context to your posts.
- **Comment and Interact**: Dive into discussions, leave comments, and connect with other users. It’s all about building a community.
- **Explore Content**: Browse the homepage to discover fresh and popular pictures. Our gallery is full of inspiration and new perspectives.

### Architecture


PicTalk is built using a modern web application architecture that leverages the power of Python and Flask for the backend, along with HTML, CSS, and JavaScript for the frontend. Here's a high-level overview of the architecture:

- **Backend**

    - **Flask**: A lightweight and flexible web framework that handles server-side logic, routing, and request handling.
    - **SQLAlchemy**: An ORM (Object-Relational Mapping) tool used for database interactions, making it easy to perform CRUD operations.
    - **Flask-Login**: Manages user authentication and session handling, ensuring secure login and logout functionalities.

- **Frontend**
    - **HTML**: Structures the web pages, providing the content and layout for different parts of the application.
    - **CSS**: Styles the web pages, making them visually appealing and responsive. Custom CSS files and Bootstrap are used for consistent and attractive design.
    - **JavaScript**: Adds interactivity and dynamic behavior to the web pages, enhancing the user experience.

- **Templates**
    - **Jinja2**: The templating engine used with Flask to dynamically generate HTML pages. Templates are extended from a base layout to maintain a consistent look and feel across the application.

- **Database**
    - **SQLite**: Used as the database to store user information, posts, comments, and other data. SQLAlchemy provides an easy interface to interact with the database.

- **File Structure**
    - **App Package**: Contains all the application code, including configurations, routes, models, forms, and utilities.
    - **Static Files**: Includes CSS, JavaScript, and image files used in the application.
    - **Templates**: Contains HTML template files that define the structure of the web pages.

This architecture ensures that PicTalk is scalable, maintainable, and easy to develop and deploy. It separates concerns between the backend and frontend, making it easier to manage and extend the application over time.

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
Ensure you have a .flaskenv file in main directory with at least the following lines outlining environments of:
`FLASK_APP=picTalk.py` and `SECRET_KEY`.

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
And open the link 'http://127.0.0.1:5000' on your preferred browser. 
### Systems tests
It's advised to collapse all the functions when viewing the source code (on Vscode, the shortcut is `CTRL + K CTRL + 0`). To run all tests, navigate to the tests directory (failing to navigate to the tests directory, will result in certain tests failing) then run `seleniumTests.py`. Do not have the flask app running in the background, otherwise this will overload the server.
```
python3 seleniumTests.py
```
The tests take a upwards of a 135 seconds to complete, as such to run a specific test, 
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
