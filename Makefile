APP=match
JS_FILES=media/js/glossary.js media/js/slpchart01.js media/js/wheel_match.js
MAX_COMPLEXITY=7

all: jenkins

include *.mk

eslint: $(JS_SENTINAL)
	$(NODE_MODULES)/.bin/eslint $(JS_FILES)

.PHONY: eslint
