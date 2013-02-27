What is it?
======

Aurora is a web interface for deploy tool fabric created for remote deploying and "console scared" boys.
Inspired by [Webistrano](https://github.com/peritor/webistrano/).


Features:
========

* Remote deploy anywhere (with SSH-keys ofc.)
* Agile control over tasks, stages, deployments, project and their parameters
* Supports custom branchs for deployments
* Deployment history
* Granularity permissions for stages and users control
* Import/Export fabfile
* Support for prompting (user input) available on non mod_wsgi (special realization of signals)


How to run it?
=======

* Create env `virtualenv aurora` somewhere and activate it: `source aurora/bin/activate`
* Run `pip install fabric`
* Go in project folder `cd aurora`
* Run `fab local_setup`
* Run `python manage.py runserver`
* Open http://127.0.0.1:8000/ in browser


License:
=======

Aurora is released under the MIT [license](http://www.opensource.org/licenses/MIT)
