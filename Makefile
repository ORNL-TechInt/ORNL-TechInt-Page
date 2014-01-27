ALL_INC = content_close.inc \
    content_intro.inc \
    hdbody.inc \
    hdrnav.inc \
    html_close.inc \
    html_intro.inc

ALL_OTHER = index.html \
    architecture.html \
    contact.html \
    data.html \
    jobs.html \
    members.html \
    networking.html \
    nvm.html \
    projects.html \
    publications.html \
    software.html \
    storage.html

ALL_MEMBERS = atchley.html \
    barron.html \
    cwang.html \
    fuller.html \
    fwang.html \
    gunasekaran.html \
    gupta.html \
    harney.html \
    kim.html \
    miller.html \
    mowery.html \
    oral.html \
    simmons.html \
    smith.html \
    stansberry.html \
    steinert.html \
    tiwari.html \
    vazhkudai.html \
    white.html

all: mkhtml $(ALL_MEMBERS) $(ALL_OTHER)

%.html: %.src $(ALL_INC)
	./mkhtml $<

README.html: README.md
	Markdown.pl $< > $@

mkhtml: mkhtml.py
	ln -s mkhtml.py mkhtml

clean:
	rm -rf $(ALL_MEMBERS) $(ALL_OTHER) validation_*.html README.html

w3valid: all
	validate -r -w *.html

valid: all
	validate *.html
