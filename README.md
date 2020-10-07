# BlueBlogOverhauled
Completely Overhauled the looks of my previous project BlueBlog and Changed database to MySql.

# Features
* User Registration
* User Login & Logout
* Changed MySql default encoding to utf8mb4, so that we can use emojis
* Forgot Password, Change Password, Reset Password Views
* Now using django-taggit library to include Tags and Search by tags
* User can comment, reply
* User can delete his own comment or reply
* Added permissions to the pages
* Now using Google-maps api in contact page
* Now admin will recieve mail on his gmail account if some submitted a contact form or not
* User Profile
* User can will redirect to previous page after login 
* Fully featured RichTextEditor included
* Give feedback
* Add your images to your profile
* Create, Update, Edit & Delete Posts
* Search
* Customized admin panel
* You can use excerpts or tags for the post
* Add your excerpts and tags
* Fully responsive


# Want to use it in your machine?

Clone project & Install Requirements

> Make sure you have already installed python3 and git.

```
$ git clone https://github.com/Avihwr/BlueBlogOverhauled.git
$ pip install -r requirements.txt
```

# Migrate & Collect Static

> Make sure you're in the BlueBlogOverhauled direcotry.
```
$ python manage.py migrate
$ python manage.py collectstatic
```
# Create Admin User and Run Server

```
$ python manage.py createsuperuser
$ python manage.py runserver
```

Andd thats it!!



