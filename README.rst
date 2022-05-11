Open edX Demo plugin
=====================

|ci-badge| |license-badge|


Overview
--------

Where all the extensions & tools for the Open edX Demo Site installation live!

Here's the list of solutions implemented in this repository:

- Assign course access roles to users after their registration process
- Common configurations
- Commands for resetting databases to initial state [WIP]

Usage
-----

First, install the plugin:

.. code-block:: bash

  git clone https://github.com/eduNEXT/openedx-demo-plugin/
  pip install ./openedx-demo-plugin

Then:

- After the registration your user will have course access permissions
- ... [WIP]

Development Workflow
--------------------

One Time Setup
~~~~~~~~~~~~~~
.. code-block::

  # Clone the repository
  git clone git@github.com:edx/openedx-demo-plugin.git
  cd openedx-demo-plugin

  # Set up a virtualenv using virtualenvwrapper with the same name as the repo and activate it
  mkvirtualenv -p python3.8 openedx-demo-plugin


Every time you develop something in this repo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block::

  # Activate the virtualenv
  workon openedx-demo-plugin

  # Grab the latest code
  git checkout main
  git pull

  # Install/update the dev requirements
  make requirements

  # Run the tests and quality checks (to verify the status before you make any changes)
  make validate

  # Make a new branch for your changes
  git checkout -b <your_github_username>/<short_description>

  # Using your favorite editor, edit the code to make your change.
  vim …

  # Run your new tests
  pytest ./path/to/new/tests

  # Run all the tests and quality checks
  make validate

  # Commit all your changes
  git commit …
  git push

  # Open a PR and ask for review.

License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.


.. |ci-badge| image:: https://github.com/eduNEXT/openedx-demo-plugin/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/eduNEXT/openedx-demo-plugin/actions
    :alt: CI

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/openedx-demo-plugin.svg
    :target: https://github.com/eduNEXT/openedx-demo-plugin/blob/main/LICENSE.txt
    :alt: License
