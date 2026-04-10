SHELL := /bin/bash

ASCIIDOCTOR_PDF := asciidoctor-pdf

projeto-vapor.pdf: projeto-vapor.adoc atributos-pt-br.adoc pdf-theme.yml
	$(ASCIIDOCTOR_PDF) -r asciidoctor-kroki \
		-a kroki-server-url=https://kroki.io \
		-a allow-uri-read \
		-a pdf-theme=pdf-theme.yml \
		-a pdf-fontsdir="fonts;GEM_FONTS_DIR" \
		-o $@ $<

.PHONY: all
all: projeto-vapor.pdf

.PHONY: clean
clean:
	rm -f projeto-vapor.pdf
