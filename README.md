# ORNL-TechInt-Page

This project is for building a public-facing page describing the
Technology Integration Group, NCCS, ORNL.

The master copy resides at

    https://github.com/ORNL-TechInt/ORNL-TechInt-Page

Here's an outline of the recipe for making a change:

 * Get a copy of the repo (see "[Gitting a Copy](#copy)")

 * Edit the files and review your changes (see "[Making
   Changes](#changes)", "[Special Measures](#special)", and
   "[Implications](#implications)")

 * Deploy the updated files (see "[Deploying Changes](#deploying)")


<a name="copy">
## Gitting a Copy

If you have a github account that is a member of the ORNL-TechInt
organization, you can get a development copy of the repository that
will allow you make changes to the site and push them back into the
repository:

    $ git clone git@github.com:ORNL-TechInt/ORNL-TechInt-Page.git [dirname]

Alternatively, you can get a read-only copy of the site:

    $ git clone git://github.com/ORNL-TechInt/ORNL-TechInt-Page.git [dirname]

If you need your github account added to the ORNL-TechInt
organization, send a request to tbarron at ornl dot gov or fwang2 at
ornl dot gov.

In what follows, "$TECHINT" refers to the git working directory.


<a name="changes">
## Making Changes

Edit the .src files (see "[Special Measures](#special)" and
"[Implications](#implications)"below). Running mkhtml will generate
.html from the .src files. Git will keep track of your updates. You
can see the results of your changes by running

    $ make review

and visiting http://users.nccs.gov/~UID/techint/ in your browser
(where UID is your NCCS username). 'make review' deploys the site in
your account at $HOME/www/techint.

NOTE: Running 'make review' will only work on a machine where
/ccs/wwwusers is mounted. Examples are home, dtnXX, rhea, etc.

<a name="deploying">
## Deploying Changes

Once you're satisfied with your changes, do the following to deploy
them to production:

    $ git commit -a  (you'll be asked to write something describing your update)
    $ git push
    $ make deploy

This sequence will 1) commit your changes to your local git repo, 2)
push your changes up to the shared repository at github.com, and 3)
deploy the files to /ccs/wwwproj/stf008/techint where they'll be
visible through the URL http://techint.nccs.gov.


<a name="special">
## Special Measures

To style these pages similarly to olcf.ornl.gov, it's necessary to put
the same header on them that the OLCF site uses. This header consists
of a combination of HTML and CSS. Since the html files include the css
file, this can easily be done with a single copy of the css.

However, the HTML specification doesn't provide a way for including
common HTML snippets into multiple files. So we're faced with either
maintaining the same navigation code across 30+ files or finding some
way of incorporating a single copy of the code into the 30+ files.

To address this, I have written a <del>small python script</del> static
file generator (but I didn't know to call it that when I wrote it) called
mkhtml that understands simple includes and conditionals. For example,
index.html is generated from index.src, which contains directives like

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


<a name="implications">
## Implications

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

    * Add the new file to the ALL_MEMBERS list in Makefile.

    * Add a new &lt;li> tag for the new entry in hdrnav.inc.

    * Add a new &lt;li> tag for the new entry in members.src.

    * Run 'make review' to examine the changes in your personal web
      area (http://users.nccs.gov/~UID/techint/index.html)

    * Once satisfied with your updates, commit and push the changes in
      the master branch.

    * Run 'make deploy' to update the production website at
      http://techint.nccs.gov. NOTE: This must be done on a machine
      with /ccs/wwwproj mounted.

 * For a new year in publications or software, add the new material to
   publications.src or software.src and a new &lt;li> tag in
   hdrnav.inc. After that, review and verify the changes, then commit
   and push. Finally, run 'make deploy'.


## Makefile Targets

The following targets are available in the Makefile:

 * all: rebuild all html files from .src and .inc files. This is the
   default target that gets run if make is invoked with no arguments.

 * %.html: tells make that foo.html depends on foo.src as well as
       all the .inc files

 * review: deploys the site to $HOME/www/techint. After running this,
   you should be able to view the result in your browser by visiting
   http://users.nccs.gov/~UID/techint/ (where UID is your lowercase
   username). Use this to verify that your changes had the effect you
   intended.

 * deploy: deploys the site to /ccs/wwwproj/stf008/techint, which is
   where the URL techint.nccs.gov points.

 * README.html: run Markdown.pl to generate README.html

 * mkhtml: creates symlink mkhtml -> mkhtml.py if needed

 * clean: removes generated files

 * w3valid: runs each .html file through validator.w3.org. If there
       are errors in foo.html, they are saved in validation_foo.html.

 * valid: run the local python validation checks on the .html files.

 * validate: create symlink validate -> validate.py if needed

 * version: generate the javascript version file based on 'git describe'

## Potential Improvements

 * With some work, I think we could get rid of mkhtml and replace it with
   [jekyll](http://jekyllrb.com/) (or some other static file generator).
