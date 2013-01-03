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
    data.html \
    members.html \
    networking.html \
    nvm.html \
    projects.html \
    storage.html \
    vazhkudai.html

all: $(ALL_HTML)

%.html: %.src $(ALL_INC)
	mkhtml $<

clean:
	rm -rf $(ALL_HTML)
