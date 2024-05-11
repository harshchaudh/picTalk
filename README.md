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
PicTalk is a website designed for photography enthusiasts. Users can upload their own images to share with the community. Other users can then interact with these images by commenting and/or liking/disliking images. This in turn provides valuable, constructive feedback to the original user and creates engagment among users.  Overall, PicTalk provides a platform for amatuer photographers to showcase their work and receive feedback from others in the community.

For website's similar to PicTalk, [Instagram](https://www.instagram.com) and [Unsplash](https://unsplash.com/) would be good comparisons, they have similar but opposite purposes, while PicTalk achieves both.

### Design
- **User Interface**: Minimilist layout, a fair portion of the website is whitespace and rarely is the full screen ever used. We've chosen a colour pallete that provided that was visually satisfyingh. Large and easily identifiable fonts, buttons, links, etc. Small screens like phone screens where taken into consideration and were mostly accomplished automatically by Bootstrap. However, certain aspects of the website do not function on small screens specifically the navigation bar. As such, **PicTalk is a desktop-first website**.

- **Navigation**: The website is fairly simple as such all navigatable items are all available to the user on the home page. There's a persistant navigation bar that only changes with the login state of the user. The main content changes as the user visits different sections of the website. All labels and possible links are all fairly clear.

- **Features**
    - Gallery page, images update the moment a user uploads the image. It's current implementation does not particular work when scaled up (or at least may not)
### Use
- 

## Architecture

## Getting started
This section details the steps required to deploy the website and complete necessary tests. The following instructions are for Ubuntu based Linux distrubtions; **Ubuntu 22.04.4 LTS** was used specificaly.

### Prerequsites
We'll assume you have the basic's like Python. Packages can be installed using the command `pip3 install <<package>>`, where **package** is the package that needs to be installed.

|Package Name|Version|package|
|----|----|----|
|Flask|3.0.3|flask|
|SQLAlchemy|2.0.29|sqlalchemy|
|Flask SQLAlchemy|3.1.1|flask-sqlalchemy|
|FLask Login|0.6.3|flask-login|

### Deployment

## Running tests

