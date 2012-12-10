ORNL-TechInt-Page
=================

This project is for building a public-facing page describing the
Technology Integration Group, NCCS, ORNL.

The master copy resides at

   https://github.com/ORNL-TechInt/ORNL-TechInt-Page


Gitting a Copy
--------------

If you have a github account that is a member of the ORNL-TechInt
organization, you can get a development copy of the repository that
will allow you make changes to the site and push them back into the
repository:

 $ git clone git@github.com:ORNL-TechInt/ORNL-TechInt-Page.git [dirname]

Alternatively, you can get a read-only copy of the site:

 $ git clone git://github.com/ORNL-TechInt/ORNL-TechInt-Page.git [dirname]


Git Hooks
---------

A pre-commit hook can be used to validate the HTML before completing
the commit and a post-commit hook can be used to update the version
value displayed at the bottom of the main page of the site. After
cloning your copy of the repo, you can activate these hooks by running

   $ ./githooks/mk_symlinks

This creates the appropriate symlinks from .git/hooks to scripts in
githooks.
