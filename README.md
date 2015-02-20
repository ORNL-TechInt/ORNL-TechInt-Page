ORNL-TechInt-Page
=================

This project is for building a public-facing page describing the
Technology Integration Group, NCCS, ORNL.

The master copy resides at

    https://github.com/ORNL-TechInt/ORNL-TechInt-Page

Here's an outline of the recipe for making a change:

 * Get a copy of the repo (see "[Gitting a Copy](#copy)")

 * Install the git hooks by running $TECHINT/githooks/mk_symlinks (see
   "Git Hooks") (NOTE: If you don't install the githooks, you'll need
   to run githooks/post-merge by hand before deploying)

 * Edit the files and review your changes (see "Making Changes")

 * Deploy the updated files (see "Deploying Changes")


<a name="copy">
Gitting a Copy
--------------

If you have a github account that is a member of the ORNL-TechInt
organization, you can get a development copy of the repository that
will allow you make changes to the site and push them back into the
repository:

    $ git clone git@github.com:ORNL-TechInt/ORNL-TechInt-Page.git [dirname]

Alternatively, you can get a read-only copy of the site:

    $ git clone git://github.com/ORNL-TechInt/ORNL-TechInt-Page.git [dirname]

If you need your github account added to the ORNL-TechInt
organization, send a request to tbarron at ornl dot gov. In what
follows, "$TECHINT" refers to the git working directory.


Git Hooks
---------

Hook scripts are available for 1) updating js/version.js with the
output 'git describe' so that the site version and last update time is
displayed on the About page, and 2) running make to process .src files
to generate the .html files.

After cloning your copy of the repo, you can activate these hooks by
running

    $ $TECHINT/githooks/mk_symlinks

This creates the appropriate symlinks from .git/hooks to the scripts
in $TECHINT/githooks.

Available hook scripts include

>    set-version: generate js/version.js, based on the output of 'git
>      describe'. mk_symlinks links this as the post-commit hook.
>
>    post-merge: call set-version, then run make to rebuild the html
>      files. mk_symlinks links this as the post-merge hook.


Making Changes
--------------

Edit the files like normal. Git will keep track of your updates. You
can see the results of your changes by running

    $ make review

and visiting http://users.nccs.gov/~UID/techint/ in your browser
(where UID is your NCCS username). 'make review' will deploy the site
in your account at $HOME/www/techint.


Deploying Changes
-----------------

Once you're satisfied with your changes, do the following:

    $ git commit -a  (you'll be asked to write something describing your update)
    $ git push
    $ make deploy

This sequence will 1) commit your changes to your local git repo, 2)
push your changes up to the shared repository at github.com, and 3)
deploy the files to /ccs/wwwusers/stf008/techint where they'll be
visible through the URL http://techint.nccs.gov.

 
Special Measures
----------------

To style these pages similarly to olcf.ornl.gov, it's necessary to put
the same header on them that the OLCF site uses. This header consists
of a combination of HTML and CSS. Since the html files include the css
file, this can easily be done with a single copy of the css.

However, the HTML specification doesn't provide a way for including
common HTML snippets into multiple files. So we're faced with either
maintaining the same navigation code across 30+ files or finding some
way of incorporating a single copy of the code into the 30+ files.

To address this, I have written a small python script call mkhtml that
understands simple includes and conditionals. For example, index.html
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

    <meta name="keywords" content="index" />

mkhtml.py notices when this goes by and sets variable self.filetype to
the value indicated by the content attribute. The code above allows
for the currently active tab in the menu bar to be a different color
from the others.

There is also a Makefile with the dependencies defined so after
editing a .src or .inc file, you can just run make to rebuild the HTML
files.


Implications
------------

 * To change HTML content, edit the corresponding .src file. If you're
   just updating the git repository so someone else can fetch it and
   deploy your change, that's all you need to do (well, except for
   'git commit -a' and 'git push'). The person redeploying the files
   must run make after the .src files are up to date to rebuild the
   .html files.

 * The .css file will be reloaded by browsing requests directly (the
   user may need to issue a refresh), so there's no need to rebuild
   after changing the .css.

 * To add a new member to the group, a new thrust area, or a new year
   to the publications or software categories, several files must be
   updated. Let's take a new group member as an example. Here are the
   steps:

    * Create a new .src file based on the person's name. The
      convention so far has been to use last names unless that results
      in a collision, in which case we add the first initial (eg.,
      cwang.src and fwang.src for Chao and Feiyi).

    * Add the new file to the list in Makefile.

    * Add a new <li> tag for the new entry in hdrnav.inc.

    * Add a new <li> tag for the new entry in members.src.

    * Commit and push the changes.

    * Pull the changes into the deployment directory.

    * Run make (this step can be automated using the post merge git
      hook described above).

 * For a new year in publications or software, add the new material to
   publications.src or software.src and a new &lt;li> tag in hdrnav.inc.
   After that, commit and push the changes, pull the update into the
   deployment directory, and (unless it's automated) run make to
   generate the .html files.


Makefile Targets
----------------

The following targets are available in the Makefile:

 * all: rebuild all html files from .src and .inc files

 * %.html: tells make that foo.html depends on foo.src as well as
       all the .inc files

 * review: deploys the site to $HOME/www/techint. After running this,
   you should be able to view the result in your browser by visiting
   http://users.nccs.gov/~UID/techint/ (where UID is your lowercase
   username). Use this to verify that your changes had the effect you
   intended.

 * deploy: deploys the site to /ccs/wwwusers/stf008/techint, which is
   where the URL techint.nccs.gov points.

 * README.html: run Markdown.pl to generate README.html
    
 * mkhtml: creates symlink mkhtml -> mkhtml.py if needed

 * clean: removes generated files

 * w3valid: runs each .html file through validator.w3.org. If there
       are errors in foo.html, they are saved in validation_foo.html.

 * valid: run the local python validation checks on the .html files.
