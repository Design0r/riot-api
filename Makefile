#!make
ifneq (,$(wildcard ./.env))
    include .env
    export
endif



dev: 
	@docker compose up --build -d
	@cd riotapi && \
		uv run manage.py makemigrations && \
		uv run manage.py migrate && \
		uv run manage.py initadmin && \
		uv run manage.py runserver

