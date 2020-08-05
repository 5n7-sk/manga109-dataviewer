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
