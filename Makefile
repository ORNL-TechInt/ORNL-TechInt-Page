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
    brumgard.html \
    cwang.html \
    fwang.html \
    griffith.html \
    gunasekaran.html \
    miller.html \
    mowery.html \
    oral.html \
    shin.html \
    sim.html \
    simmons.html \
    steinert.html \
    vazhkudai.html \
    white.html \
    zimmer.html

TARGET=/ccs/wwwproj/stf008/techint

XTARGET=$(HOME)/www/techint

all: mkhtml $(ALL_MEMBERS) $(ALL_OTHER)

%.html: %.src $(ALL_INC)
	./mkhtml $<

review: version
	rm -rf $(XTARGET)
	mkdir -p $(XTARGET)/js
	git archive --format tar HEAD | (cd $(XTARGET); tar x; make all)
	cp js/version.js $(XTARGET)/js/version.js

deploy: version
	rm -rf $(TARGET)
	mkdir -p $(TARGET)/js
	git archive --format tar master | (cd $(TARGET); tar x; make all)
	cp js/version.js $(TARGET)/js/version.js
	chmod -R g+w $(TARGET)

README.html: README.md
	Markdown.pl $< > $@

mkhtml: mkhtml.py
	ln -s mkhtml.py mkhtml

clean:
	rm -rf $(ALL_MEMBERS) $(ALL_OTHER) validation_*.html README.html

w3valid: all validate
	validate -r -w *.html

valid: all validate
	validate *.html

validate:
	if [[ ! -x validate ]]; then \
		ln -s validate.py validate; \
	fi

version:
	githooks/set-version
