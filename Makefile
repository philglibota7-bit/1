.PHONY: hilfe bauen test starten pruefen sauber

hilfe:
	@echo "make bauen    – Katalog, Pro-Seite, Rechtsseiten, Sitemap erzeugen"
	@echo "make test     – Tests laufen lassen"
	@echo "make starten  – lokal auf http://localhost:8000/werkbank.html"
	@echo "make pruefen  – bauen + test + Vollstaendigkeitspruefung"

bauen:
	@python3 build.py

test:
	@python3 -m unittest discover -s tests -v

starten:
	@echo "http://localhost:8000/werkbank.html"
	@python3 -m http.server 8000

pruefen: bauen test
	@python3 -c "import json,sys; \
	m=json.load(open('tools.json'))['marke']; \
	sys.exit('FEHLT: echte Impressumsdaten in tools.json' if 'DEIN' in m['betreiber'] else 0)"
	@echo "Alles in Ordnung."

sauber:
	@rm -rf cockpit/__pycache__ tests/__pycache__ __pycache__
