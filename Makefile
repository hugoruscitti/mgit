all:
	@echo ""
	@echo "Comandos disponibles:"
	@echo ""
	@echo "  test            ejecute los tests una sola vez."
	@echo "  test_live	ejecuta los tests contínuamente."
	@echo ""
	@echo ""


test:
	pipenv run pytest --capture=no


test_live:
	pipenv run ptw -- --capture=no
