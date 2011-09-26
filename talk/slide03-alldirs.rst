
Problem 1 : Django only runs tests in 'models.py' and 'tests.py'::

    DjangoProject
     |--DjangoApplication
     |   |  models.py       # testst run
     |   |  tests.py        # tests run
     |   |  <other>.py      # tests NOT run
     |         
     |--OtherPackages
     |   |  tests.py        # tests NOT run
     |
     |--AcceptanceTests
     |   |  tests.py        # tests NOT run

