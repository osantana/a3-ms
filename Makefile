SHELL := /bin/bash

ASCIIDOCTOR_PDF := /opt/homebrew/bin/asciidoctor-pdf

projeto-vapor.pdf: projeto-vapor.adoc atributos-pt-br.adoc
	$(ASCIIDOCTOR_PDF) -o $@ $<

.PHONY: all
all: projeto-vapor.pdf

.PHONY: clean
clean:
	rm -f projeto-vapor.pdf
