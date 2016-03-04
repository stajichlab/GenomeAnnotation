MARKDOWN=pandoc --from markdown --standalone --indented-code-classes=perl

all: htmlall pdfall

pdfall: $(patsubst %.md,%.pdf,$(wildcard *.md)) 

htmlall: $(patsubst %.md,%.html,$(wildcard *.md)) 



%.html: %.md
	$(MARKDOWN) $< --to html5 --output $@

%.pdf: %.md
	$(MARKDOWN) $< --to latex --output $@
