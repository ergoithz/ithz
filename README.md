# ithz
[A simple CMS](http://ithz.eu/en/ithz_cms) for my personal website, hosted on Google App Engine.

This project is pretty old (it was mainly developed between December 2009 and May 2010) but have been migrated to webapp2 and django 1.2 templates at Mars 2015 (and then migrated to github).

## Features

* Different user typologies (public user, administrator, moderator, editor and registered user) with separated and hierarchic permissions.
* Javascript is divided in micro-modules, which are loaded only when necessary, degrades gracefully.
* Ajax (sadly using obsolete hash urls).
* Clean and strict object-oriented interfaces for component communication (including templates).

