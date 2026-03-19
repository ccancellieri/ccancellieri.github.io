.PHONY: serve dev deploy validate clean help

PORT ?= 5500

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

serve: ## Start a local dev server (Python)
	@echo "Starting server at http://localhost:$(PORT)"
	python3 -m http.server $(PORT)

dev: ## Open in VS Code and start live server
	code .
	@echo "Use Live Server extension (Alt+L Alt+O) or run: make serve"

deploy: ## Push to GitHub Pages
	git add index.html README.md REFERENCES.md
	git commit -m "Update portfolio"
	git push origin main
	@echo "Deployed! Site live at https://ccancellieri.github.io"

validate: ## Validate HTML (requires html5validator: pip install html5validator)
	html5validator --root . --also-check-css --log INFO index.html

minify: ## Minify HTML (requires html-minifier: npm i -g html-minifier)
	html-minifier --collapse-whitespace --remove-comments --minify-css true --minify-js true index.html -o index.min.html
	@echo "Minified: $$(wc -c < index.html) -> $$(wc -c < index.min.html) bytes"

lighthouse: ## Run Lighthouse audit (requires Chrome + lighthouse CLI)
	lighthouse http://localhost:$(PORT)/index.html --output html --output-path ./lighthouse-report.html
	@echo "Report saved to lighthouse-report.html"

clean: ## Remove generated files
	rm -f index.min.html lighthouse-report.html

stats: ## Show file stats
	@echo "=== Portfolio Stats ==="
	@echo "HTML size: $$(wc -c < index.html | tr -d ' ') bytes"
	@echo "HTML lines: $$(wc -l < index.html | tr -d ' ')"
	@echo "Sections: $$(grep -c '<section' index.html)"
	@echo "Project cards: $$(grep -c 'project-card' index.html)"
	@echo "Links: $$(grep -c '<a ' index.html)"
