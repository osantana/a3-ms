SHELL := /bin/bash

ASCIIDOCTOR_PDF := asciidoctor-pdf

projeto-vapor.pdf: projeto-vapor.adoc atributos-pt-br.adoc
	$(ASCIIDOCTOR_PDF) -r asciidoctor-kroki \
		-a kroki-server-url=https://kroki.io \
		-a allow-uri-read \
		-o $@ $<

.PHONY: all
all: projeto-vapor.pdf

.PHONY: clean
clean:
	rm -f projeto-vapor.pdf
