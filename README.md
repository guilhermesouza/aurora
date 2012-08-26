aurora
======

aurora is a web interface for deploy tool fabric created for remote deploying and "console scared" boys.
Inspired by [Webistrano](https://github.com/peritor/webistrano/).

features
========
* Remote deploy anywhere
* Clear interface
* Agile control over tasks, stages, deployments, project and their parameters
* Supports custom branchs for deployments
* Deployment history
* Granularity permissions for stages and users control
* Import/Export fabfile
* Support for prompting (user input) available on non mod_wsgi (special realization of signals)
* Provided with fabfile for aurora

install
=======
* Run `pip install -r requirements.txt`
* Go in project folder `cd aurora`
* Run `python manage.py syncdb`
* Run `python manage.py migrate`
* Change DEBUG in aurora/settings.py
* Run `python manage.py runserver`
* Open http://127.0.0.1:8000/

license
====
Aurora is released under the MIT [license](http://www.opensource.org/licenses/MIT)

todo
====
Replace pexpect.
