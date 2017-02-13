OUT_DIR = build
SRC_DIR = src

all: \
	${OUT_DIR} \
	${OUT_DIR}/index.html \
	${OUT_DIR}/moxie.css

${OUT_DIR}:
	mkdir -p "${OUT_DIR}"

${OUT_DIR}/index.html: ${SRC_DIR}/index.html
	cp "$?" "$@"

${OUT_DIR}/moxie.css: ${SRC_DIR}/moxie.css
	cp "$?" "$@"

.PHONY: devd watch

serve:
	devd --notimestamps --livereload --watch="${OUT_DIR}" \
		/="${OUT_DIR}/"

watch:
	watchexec -e html,css -i "\*/${OUT_DIR}/\*" make
