# Токенайзер отделяет «понять запрос» от «выполнить запрос»

Часть 2 туториала (cstack): `.` в начале строки значит meta-command (`.exit`), остальное идёт в `prepare_statement` (text -> Statement) и `execute_statement` (Statement -> действие). Пользователь сам понял, почему `buffer[0] == '.'`, и откуда `do_meta_command`.

Уточнение: это не буквально SOLID, а конвейер front-end (парсер) -> back-end (executor), как в SQLite. Колонки и оконные функции придут как поля Statement/AST, а не как отдельные «определители».

**Implications:** следующий шаг — Row (id, username, email), разбор аргументов insert через sscanf, затем Table/страницы. Тесты stage_02 в tests/run_tests.py пока красные, это ожидаемо.
