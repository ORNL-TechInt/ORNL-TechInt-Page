ALL_HTML = index.html \
    architecture.html \
    data.html \
    networking.html \
    nvm.html \
    projects.html \
    storage.html

all: $(ALL_HTML)

%.html: %.src
	mkhtml $<

clean:
	rm -rf $(ALL_HTML)
