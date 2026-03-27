SHELL := /bin/bash

ASCIIDOCTOR_PDF := /opt/homebrew/bin/asciidoctor-pdf

projeto-vapor.pdf: projeto-vapor.adoc atributos-pt-br.adoc
	DIAGRAM_PLANTUML_CLASSPATH=/opt/homebrew/Cellar/plantuml/1.2026.2/libexec/plantuml.jar \
	$(ASCIIDOCTOR_PDF) -r asciidoctor-diagram -o $@ $<

.PHONY: all
all: projeto-vapor.pdf

.PHONY: clean
clean:
	rm -f projeto-vapor.pdf
