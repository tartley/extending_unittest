
Demo readable test names::

    . set_test_options 2
    rerun ./manage.py test --settings=settings.test-quick-web --verbosity=2 ordering

And compare number of lines output::

    . set_test_options 1
    ./manage.py test --settings=settings.test-quick-web --verbosity=2 ordering 2>&1 | fold -w 80 | wc

    . set_test_options 2
    ./manage.py test --settings=settings.test-quick-web --verbosity=2 ordering 2>&1 | fold -w 80 | wc

