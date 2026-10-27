# Kokoro-82M TTS — Standalone / Автономный запуск

[Русский](#русский) | [English](#english)

---

<a name="русский"></a>
## Русский

> **Ветка `standalone`** содержит все необходимые библиотеки (`wheels/`) и файлы моделей (`voices-v1.0.bin`, `kokoro-v1.0.onnx.part*`), что позволяет запускать приложение на любом ПК с Windows **полностью без интернета**.

Kokoro-82M — легковесная (82 миллиона параметров) и сверхбыстрая модель синтеза речи (Text-to-Speech) с открытыми весами и качеством звука 24 кГц.

### О модели
- Архитектура: StyleTTS 2 + ISTFTNet (decoder-only, без диффузии).
- Размер весов: ~320 МБ (ONNX).
- Потребление ресурсов: менее 1 ГБ RAM/VRAM.
- Скорость генерации: в 20–50 раз быстрее реального времени (RTF < 0.05).
- Лицензия: Apache 2.0.
- Поддерживаемые языки:
  - Английский (американский `a`, британский `b`)
  - Французский (`f`)
  - Испанский (`e`)
  - Итальянский (`i`)
  - Бразильский португальский (`p`)
  - Японский (`j`)
  - Китайский (`z`)
  - Хинди (`h`)
  - Примечание: русский язык в официальной модели не поддерживается.

### Быстрый запуск

#### Автоматический запуск (Windows)
Запустите файл:
```text
run_ui.bat
```
Скрипт автоматически:
1. Проверяет наличие Python в системе (поддерживаются Python 3.10 — 3.14).
2. Создает изолированное виртуальное окружение `venv` (если отсутствует).
3. Устанавливает зависимости из локальной папки `wheels/` без подключения к сети.
4. При необходимости собирает модель `kokoro-v1.0.onnx` из частей `.part*`.
5. Запускает веб-интерфейс по адресу: http://127.0.0.1:7860

#### Ручной офлайн-запуск через терминал
```bash
python -m venv venv
venv\Scripts\activate
pip install --no-index --find-links=wheels -r requirements.txt
python app.py
```

### Структура проекта

```text
Kokoro/
├── app.py                   # Веб-интерфейс на Gradio
├── run_ui.bat               # Скрипт настройки и запуска (с поддержкой офлайн-режима)
├── requirements.txt         # Список Python-зависимостей
├── wheels/                  # Офлайн-пакеты (wheels) для Python 3.10-3.14 на Windows
├── kokoro-v1.0.onnx.part*   # Веса модели (ONNX), разбитые на части < 100 МБ для GitHub
├── voices-v1.0.bin          # Файл с 54 голосами
└── README.md                # Документация проекта
```

### Обозначение голосов

В модели доступно 54 встроенных голоса. Названия формируются по префиксу:
- Первая буква: язык или диалект
  - `a` — американский английский
  - `b` — британский английский
  - `e` — испанский
  - `f` — французский
  - `i` — итальянский
  - `j` — японский
  - `p` — португальский
  - `z` — китайский
  - `h` — хинди
- Вторая буква: пол
  - `f` — женский
  - `m` — мужской

Популярные голоса:
- `af_heart` — сбалансированный женский голос (US)
- `af_bella`, `af_nicole`, `af_sky` — мягкие женские голоса (US)
- `am_adam`, `am_michael` — глубокие мужские голоса (US)
- `bf_alice`, `bm_george` — британские голоса (UK)

---

<a name="english"></a>
## English

> **The `standalone` branch** includes all pre-downloaded Python wheels (`wheels/`) and model assets (`voices-v1.0.bin`, `kokoro-v1.0.onnx.part*`), allowing complete offline execution on Windows without downloading anything during setup.

Kokoro-82M is a lightweight (82M parameters) and ultra-fast open-weight Text-to-Speech (TTS) model with 24 kHz audio quality.

### Quick Start

#### Automated Launch (Windows)
Run the script:
```text
run_ui.bat
```
The script will automatically:
1. Verify Python availability on the system (Python 3.10 to 3.14 supported).
2. Create an isolated virtual environment (`venv`) if not present.
3. Install dependencies completely offline from the local `wheels/` directory.
4. Assemble `kokoro-v1.0.onnx` from parts if needed.
5. Launch the web interface at: http://127.0.0.1:7860
