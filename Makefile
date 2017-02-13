OUT_DIR = build

all: bootstrap \
	${OUT_DIR}

${OUT_DIR}:
	mkdir -p "${OUT_DIR}"

.PHONY: bootstrap devd watch

bootstrap:
	./bootstrap

serve: all
	devd --notimestamps --livereload --watch="${OUT_DIR}" \
		/="${OUT_DIR}/" \
		/static/=./test/

watch: all
	watchexec -e elm,html,css,json -i "\*/${OUT_DIR}/\*" make
