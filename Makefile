SHELL := /bin/bash

UV := uv
RUFF := $(UV) run ruff
ASCIIDOCTOR_PDF := asciidoctor-pdf

# -- Document ----------------------------------------------------------------

projeto-vapor.pdf: projeto-vapor.adoc atributos-pt-br.adoc pdf-theme.yml
	$(ASCIIDOCTOR_PDF) -r asciidoctor-kroki \
		-a kroki-server-url=https://kroki.io \
		-a allow-uri-read \
		-a source-highlighter=rouge \
		-a rouge-style=github \
		-a pdf-theme=pdf-theme.yml \
		-a pdf-fontsdir="fonts;GEM_FONTS_DIR" \
		-o $@ $<

# -- Docker ------------------------------------------------------------------

up:
	docker compose up --build

down:
	docker compose down

# -- Development -------------------------------------------------------------

lint:
	$(RUFF) check vapor/
	$(RUFF) format --check vapor/

format:
	$(RUFF) format vapor/
	$(RUFF) check vapor/ --fix

runserver:
	$(UV) run uvicorn vapor.web:app --host 0.0.0.0 --port 8000 --reload

# -- Misc --------------------------------------------------------------------

.PHONY: all up down lint format runserver clean
all: projeto-vapor.pdf

clean:
	rm -f projeto-vapor.pdf
