.PHONY: help validate start logs stop compose clean get-version test bump-version build release docs changelog backup

help:
	@echo "make help         -- show this help"
	@echo "make validate     -- validate docker compose file"
	@echo "make start        -- start all services"
	@echo "make logs         -- view service logs"
	@echo "make stop         -- stop all services"
	@echo "make compose      -- run docker-compose commands"
	@echo "make clean        -- clean all"
	@echo "make get-version  -- get current version"
	@echo "make test         -- run tests"
	@echo "make bump-version -- bump version"
	@echo "make build        -- build docker image"
	@echo "make release      -- release new version"
	@echo "make changelog    -- update changelog"
	@echo "make docs         -- build documentation"
	@echo "make backup       -- backup data"


validate:
	./compose.sh validate

start:
	./compose.sh start -l

logs:
	./compose.sh logs

stop:
	./compose.sh stop

compose:
	./compose.sh $(MAKEFLAGS)

clean:
	./scripts/clean.sh $(MAKEFLAGS)

get-version:
	./scripts/get-version.sh

test:
	./scripts/test.sh $(MAKEFLAGS)

bump-version:
	./scripts/bump-version.sh $(MAKEFLAGS)

build:
	./scripts/build.sh $(MAKEFLAGS)

release:
	./scripts/release.sh

changelog:
	./scripts/changelog.sh $(MAKEFLAGS)

docs:
	./scripts/docs.sh $(MAKEFLAGS)

backup:
	./scripts/backup.sh
