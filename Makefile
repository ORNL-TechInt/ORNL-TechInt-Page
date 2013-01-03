ALL_INC = content_close.inc \
    content_intro.inc \
    hdbody.inc \
    hdrnav.inc \
    html_close.inc \
    html_intro.inc

ALL_HTML = index.html \
    architecture.html \
    atchley.html \
    barron.html \
    cwang.html \
    data.html \
    dillow.html \
    fuller.html \
    fwang.html \
    gunasekaran.html \
    harney.html \
    kim.html \
    members.html \
    miller.html \
    mowery.html \
    networking.html \
    nvm.html \
    oral.html \
    projects.html \
    publications.html \
    simmons.html \
    smith.html \
    stansberry.html \
    steinert.html \
    storage.html \
    vazhkudai.html \
    white.html

all: $(ALL_HTML)

%.html: %.src $(ALL_INC)
	mkhtml $<

clean:
	rm -rf $(ALL_HTML)
