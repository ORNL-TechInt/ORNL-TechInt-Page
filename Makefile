ALL_HTML = index.html \
    projects.html \
    storage.html \
    nvm.html \
    data.html \
    networking.html

all: $(ALL_HTML)

%.html: %.src
	mkhtml $<

clean:
	rm -rf $(ALL_HTML)
