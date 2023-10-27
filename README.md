# roguearch

Для корректной установки и запуска нужно создать виртуальную среду под игру и выполнить `pip install -r requirements.txt`

Далее игру можно запускать с помощью `python3 roguelike.py`

## Workflow

Для разработки понадобится утилита `poetry`

Полезные команды:
- `poetry install` -- создать виртуальную среду с обычными зависимостями
- `poetry install --with dev` -- создать виртуальную среду с обычными и `dev`-зависимостями
- `poetry add <LIBRARY_NAME>` -- установить библиотеку `<LIBRARY_NAME>` как обычную зависимость
- `poetry add --group=dev <LIBRARY_NAME>` -- установить библиотеку `<LIBRARY_NAME>` как `dev`-зависимость
- `poetry run <EXECUTABLE_NAME>` -- выполнить `<EXECUTABLE_NAME>` с использованием среды `poetry`, для разработки изначально добавлены `flake8`, `mypy`, `pytest` (являются `dev`-зависимостями)

Если при добавлении новой функциональности понадобилось добавить новые библиотеки, нужно выполнить
```bash
poetry export -f requirements.txt --output requirements.txt
```
для добавления библиотек в зависимости

Документация `poetry`: https://python-poetry.org/docs/master/

**P.S.** Старайтесь писать типизированный код и, пока CI не завезли (если вообще завезем), проверяйте свой код с помощью `flake8`, `mypy` и `pytest` (не забывайте писать тесты)
