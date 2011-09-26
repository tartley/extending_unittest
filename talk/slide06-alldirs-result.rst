
With AllDirsTestRunner, all tests are run everywhere::

    DjangoProject
     |--DjangoApp
     |   |  models.py
     |   |  other.py
     |   |--tests
     |   |   |  models_tests.py
     |       |  other_tests.py
     |         
     |--OtherPackages
     |   |  mymodule.py
     |   |--tests
     |   |   |  mymodule_tests.py
     |
     |--AcceptanceTests
     |   |  login_test.py
     |   |  change_password_test.py

