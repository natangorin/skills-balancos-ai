.DEFAULT_GOAL := help

help: ## lista os alvos
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

check: ## valida frontmatter, tamanho, tools citadas e links de todas as skills
	python3 scripts/check.py

zips: ## gera dist/<skill>.zip para subir no Claude.ai (Configurações › Skills)
	@mkdir -p dist
	@for d in skills/*/; do n=$$(basename $$d); rm -f dist/$$n.zip; (cd skills && zip -qr ../dist/$$n.zip $$n -x '*.DS_Store'); echo "dist/$$n.zip"; done

clean: ## remove dist/
	rm -rf dist
