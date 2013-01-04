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


Special Measures
----------------

To style these pages similarly to olcf.ornl.gov, it's necessary to put
the same header on them. This header consists of a combination of HTML
and CSS. Since the html files include the css file, this can easily be
done with a single copy of the css.

However, the HTML specification doesn't provide a way for including
common HTML snippets into multiple files. So we're faced with either
maintaining the same navigation code across 30+ files or finding some
way of incorporating a single copy of the code in to the 30+ files.

To address this, I have written a small python script call mkhtml that
understands simple includes and conditionals. For exmaple, index.html
is generated from index.src, which includes directives like

    %include('hdrnav.inc')

In turn, hdrnav.inc contains the following:

    %ifeq(self.filetype, 'index')
          <li class="current_page" />
           <a class="current_page" href="index.html">About</a>
    %else
          <li/>
           <a href="index.html">About</a>
    %endif

Each .src file contains a <meta ...> tag like the following:

    <meta name="filetype" content="index" />

mkhtml.py notices when this goes by and sets variable self.filetype to
the value indicated by the content attribute. This allows for the
currently active tab in the menu bar to be a different color from the
others.

There is also a Makefile with the dependencies defined so after
editing a .src or .inc file, you can just run make to rebuild the HTML
files.

Implications
------------

 * To change HTML content, edit the corresponding .src file. If you're
   just updating the git repository so someone else can fetch it and
   deploy your change, that's all you need to do. The person
   redeploying the files must run make after the .src files are up to
   date to rebuild the .html files.

 * The .css file will be reloaded by browsing requests directly, so
   there's no need to rebuild after changing the .css.

 * To add a new member to the group, a new thrust area, or a new year
   to the publications or software categories, several files must be
   updated. Let's take a new group member as an example. Here are the steps:

    * Create a new .src file based on the person's name. The
      convention so far has been to use last names unless that results
      in a collision, in which case we add the first initial (eg.,
      cwang.src and fwang.src for Chao and Feiyi).

    * Add the new file to the list in Makefile.

    * Add a new <li> tag for the new entry in hdrnav.inc.

    * Add a new <li> tag for the new entry in members.src.

    * For a new year in publications or software, add the new material
      to publications.src or software.src and a new <li> tag in
      hdrnav.inc.

    * Commit and push the changes.

    * Pull the changes into the deployment directory.

    * Run make.

