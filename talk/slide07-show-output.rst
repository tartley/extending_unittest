
So now we can run all our tests using the standard
Django invocation::

    ./manage.py test --settings=settings.test-quick-web reporting

    ./manage.py test --settings=settings.test-quick-web --verbosity=2 reporting

    rerun ./manage.py test --settings=settings.test-quick-web --verbosity=2 reporting

[and demo rerun working]

http://bitbucket.org/tartley/rerun

