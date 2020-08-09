.PHONY: format
format:
	poetry run black -v app.py
	poetry run black -v src

.PHONY: install
install:
	poetry install

.PHONY: link
link:
	mkdir ./data
	ln -fs ${path} ./data/manga109

.PHONY: run
run:
	poetry run streamlit run --server.port ${port} app.py
