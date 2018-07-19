all:
	@echo ""
	@echo "Comandos disponibles:"
	@echo ""
	@echo "  iniciar         instala todas las dependencias."
	@echo "  test            ejecute los tests una sola vez."
	@echo "  test_live	     ejecuta los tests contínuamente."
	@echo ""
	@echo ""


iniciar:
	pipenv install

test:
	pipenv run pytest --capture=no


test_live:
	pipenv run ptw -- --capture=no
