.PHONY: help dev preview rebuild index serve

PORT ?= 8765

help:
	@echo "Available commands:"
	@echo "  make dev          Start BrowserSync live preview, opens the directory page"
	@echo "  make preview      Start simple no-cache preview server"
	@echo "  make rebuild      Regenerate outreach/index.html"
	@echo "  make index        Alias for rebuild"
	@echo "  make serve        Run production-style slug/PDF server on port 8000"
	@echo ""
	@echo "Options:"
	@echo "  PORT=9000 make dev"

dev:
	./scripts/live-preview.sh $(PORT)

preview:
	./scripts/preview.sh $(PORT)

rebuild:
	./scripts/generate-outreach-index.py

index: rebuild

serve:
	python3 serve.py
