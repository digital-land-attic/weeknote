# current git branch
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
DOCS_DIR=./docs/

# default action is to build
render:
	mkdir -p $(DOCS_DIR)
	touch $(DOCS_DIR)/.nojekyll
	python3 render.py

init:
	pip install -r requirements.txt

clean::
	rm -rf $(DOCS_DIR)

commit-docs::
	git add docs
	git diff --quiet && git diff --staged --quiet || (git commit -m "Rebuilt weeknotes $(shell date +%F)"; git push origin $(BRANCH))

# TBD: remove, make the same links work locally and on the site
local:
	mkdir -p $(DOCS_DIR)
	python3 render.py --local

STATIC_DIR := docs/static
LOCAL_FRONTEND :=../frontend

assets/css:
	mkdir -p $(STATIC_DIR)/stylesheets
	cd $(LOCAL_FRONTEND) && gulp stylesheets
	rsync -r $(LOCAL_FRONTEND)/digital_land_frontend/static/stylesheets/ $(STATIC_DIR)/stylesheets/

assets/js:
	mkdir -p $(STATIC_DIR)/javascripts
	cd $(LOCAL_FRONTEND) && gulp js
	rsync -r $(LOCAL_FRONTEND)/digital_land_frontend/static/javascripts/ $(STATIC_DIR)/javascripts/

assets:: assets/css assets/js

server:
	python -m http.server --directory docs/
