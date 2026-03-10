"""Модуль централизованного логирования проекта.

Главные принципы:
- вывод в терминал только через print;
- 1:1 дублирование каждого выведенного сообщения в txt-файл;
- поддержка 2 режимов: основной и детальный;
- русский текст логов + эмодзи для визуальной навигации.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any


_LOG_FILE_PATH: Path | None = None
_DETAILED_MODE: bool = False
_LOG_LOCK = Lock()
_LOGGER_READY: bool = False


def _now() -> str:
    """Возвращает строку текущего времени в человекочитаемом формате."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _stringify_message(*parts: Any, sep: str = " ") -> str:
    """Собирает произвольные части сообщения в одну строку."""
    return sep.join(str(part) for part in parts)


def _write_line_to_file(line: str) -> None:
    """Записывает готовую строку в лог-файл (если путь инициализирован)."""
    if _LOG_FILE_PATH is None:
        return

    with _LOG_FILE_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(f"{line}\n")


def _emit_line(line: str) -> None:
    """Единая точка вывода: print + 1:1 запись в файл."""
    with _LOG_LOCK:
        print(line)
        _write_line_to_file(line)


def _log(level: str, emoji: str, message: str, detailed: bool) -> None:
    """Форматирует и публикует лог, учитывая режим детализации."""
    if detailed and not _DETAILED_MODE:
        return

    formatted_line = f"[{_now()}] {emoji} [{level}] {message}"
    _emit_line(formatted_line)


def init_logger(log_file_path: str | Path, detailed_mode: bool = False) -> None:
    """Инициализирует логгер и подготавливает новый (перезаписанный) txt-файл.

    Args:
        log_file_path: путь к txt-файлу логов из main.
        detailed_mode: True -> включить детальные логи, False -> только основные.
    """
    global _LOG_FILE_PATH, _DETAILED_MODE, _LOGGER_READY

    _LOG_FILE_PATH = Path(log_file_path)
    _DETAILED_MODE = detailed_mode

    _LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    _LOG_FILE_PATH.write_text("", encoding="utf-8")

    _LOGGER_READY = True

    _log("ОСНОВНОЙ", "🚀", "Логгер инициализирован и файл логов перезаписан.", detailed=False)
    _log("ОСНОВНОЙ", "⚙️", f"Режим детального логирования: {'ВКЛ' if _DETAILED_MODE else 'ВЫКЛ'}.", detailed=False)
    _log("ДЕТАЛЬНО", "🧭", f"Путь к лог-файлу: {_LOG_FILE_PATH.resolve()}.", detailed=True)


def set_detailed_mode(enabled: bool) -> None:
    """Динамически включает/выключает режим детального логирования."""
    global _DETAILED_MODE
    _DETAILED_MODE = enabled
    _log("ОСНОВНОЙ", "🔁", f"Детальный режим переключен: {'ВКЛ' if enabled else 'ВЫКЛ'}.", detailed=False)


def is_detailed_mode() -> bool:
    """Возвращает текущее состояние детального режима."""
    return _DETAILED_MODE


def is_logger_ready() -> bool:
    """Возвращает флаг инициализации логгера."""
    return _LOGGER_READY


def log_main(*parts: Any, sep: str = " ") -> None:
    """Пишет основной лог (всегда выводится)."""
    message = _stringify_message(*parts, sep=sep)
    _log("ОСНОВНОЙ", "📌", message, detailed=False)


def log_detail(*parts: Any, sep: str = " ") -> None:
    """Пишет детальный лог (только если включен detailed_mode)."""
    message = _stringify_message(*parts, sep=sep)
    _log("ДЕТАЛЬНО", "🔍", message, detailed=True)


def log_step(step_name: str, status: str, details: str = "") -> None:
    """Унифицированный лог шага пайплайна для удобной трассировки."""
    base_message = f"Шаг: {step_name} | Статус: {status}"
    full_message = f"{base_message} | Детали: {details}" if details else base_message
    log_main("🧩", full_message)


def log_exception(context: str, error: Exception) -> None:
    """Пишет информацию об исключении в основной и детальный канал."""
    log_main("💥", f"Ошибка в блоке '{context}': {error}")
    log_detail("📚", f"Тип ошибки: {type(error).__name__}")


def log_dict(title: str, payload: dict[str, Any], detailed: bool = True) -> None:
    """Красиво логирует словарь в несколько строк для анализа состояния."""
    if not payload:
        if detailed:
            log_detail("🗂️", f"{title}: словарь пуст.")
        else:
            log_main("🗂️", f"{title}: словарь пуст.")
        return

    header = f"{title}: найдено ключей = {len(payload)}"
    if detailed:
        log_detail("🗂️", header)
    else:
        log_main("🗂️", header)

    for key, value in payload.items():
        line = f"    • {key}: {value}"
        if detailed:
            log_detail(line)
        else:
            log_main(line)


def log_list(title: str, items: list[Any], detailed: bool = True, preview_limit: int = 20) -> None:
    """Логирует список с ограничением превью, чтобы не захламлять вывод."""
    count = len(items)
    header = f"{title}: элементов = {count}"

    if detailed:
        log_detail("📚", header)
    else:
        log_main("📚", header)

    if count == 0:
        return

    limit = min(preview_limit, count)
    for index in range(limit):
        line = f"    • [{index}] {items[index]}"
        if detailed:
            log_detail(line)
        else:
            log_main(line)

    if count > limit:
        tail = f"… и ещё {count - limit} элементов (скрыто, чтобы сохранить читаемость логов)."
        if detailed:
            log_detail(tail)
        else:
            log_main(tail)
