OUT_DIR = build
SRC_DIR = src
NODE_BIN_DIR = $(realpath node_modules/.bin)

all: \
	${OUT_DIR} \
	${OUT_DIR}/index.html \
	${OUT_DIR}/moxie.css \
	${OUT_DIR}/moxie.js

${OUT_DIR}:
	mkdir -p "${OUT_DIR}"

${OUT_DIR}/index.html: ${SRC_DIR}/index.html
	cp "$?" "$@"

${OUT_DIR}/moxie.css: ${SRC_DIR}/moxie.css
	cp "$?" "$@"

${OUT_DIR}/moxie.js: ${SRC_DIR}/Moxie.elm
	${NODE_BIN_DIR}/elm-make "$?" --output="$@" --warn

.PHONY: test devd watch

test:
	${NODE_BIN_DIR}/elm-test --compiler ${NODE_BIN_DIR}/elm-make

serve:
	devd --notimestamps --livereload --watch="${OUT_DIR}" \
		/="${OUT_DIR}/"

watch:
	watchexec -e elm,html,css -i "\*/${OUT_DIR}/\*" make
