# RoomHub
## Room reservation and organizing webapp

Software specification/architecture/implementation documentation in Hungarian in the PDF.
DR;
[https://github.com/najibghadri/RoomHub/blob/master/image.png]

## Installation on Windows:
 - Download this repo.
 - Install python 3.7 - https://www.python.org/downloads/release/python-371/
 - In shell. Install virtualenv and make a python environment close to the roomhub folder, and activate it:
   - pip install virtualenvwrapper-win
   - mkvirtualenv myproject
   - workon myproject
 - Install Django
   - pip install django
 - In the folder mysite/:
   - python manage.py migrate
   - python manage.py runserver

Same on Linux, macOS.

Done with Pilinszki-Nagy Csongor (@csongorpilinszkinagy)
