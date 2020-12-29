DOCS_DIR=./docs/

init:
	pip install -r requirements.txt

render:
	mkdir -p $(DOCS_DIR)
	python3 render.py

clean::
	rm -rf $(DOCS_DIR)


local:
	mkdir -p $(DOCS_DIR)
	python3 render.py --local