# Kokoro-82M TTS — Local Setup / Локальный запуск

[Русский](#русский) | [English](#english)

---

<a name="русский"></a>
## Русский

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
1. Проверяет наличие Python в системе.
2. Создает изолированное виртуальное окружение `venv` (если отсутствует).
3. Устанавливает зависимости из `requirements.txt`.
4. Скачивает недостающие файлы модели (`kokoro-v1.0.onnx` и `voices-v1.0.bin`).
5. Запускает веб-интерфейс по адресу: http://127.0.0.1:7860

#### Ручной запуск через терминал
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Структура проекта

```text
Kokoro/
├── app.py              # Веб-интерфейс на Gradio
├── run_ui.bat          # Скрипт автоматической настройки и запуска
├── requirements.txt    # Список Python-зависимостей
├── kokoro-v1.0.onnx    # Веса модели (ONNX)
├── voices-v1.0.bin     # Файл с 54 голосами
├── test_output.wav     # Тестовый аудиофайл
└── README.md           # Документация проекта
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

Kokoro-82M is a lightweight (82M parameters) and ultra-fast open-weight Text-to-Speech (TTS) model with 24 kHz audio quality.

### About the Model
- Architecture: StyleTTS 2 + ISTFTNet (decoder-only, non-diffusion).
- Weights Size: ~320 MB (ONNX).
- Resource Usage: Under 1 GB RAM/VRAM.
- Inference Speed: 20–50x faster than real-time (RTF < 0.05).
- License: Apache 2.0.
- Supported Languages:
  - English (American `a`, British `b`)
  - French (`f`)
  - Spanish (`e`)
  - Italian (`i`)
  - Brazilian Portuguese (`p`)
  - Japanese (`j`)
  - Mandarin Chinese (`z`)
  - Hindi (`h`)
  - Note: Russian language is not supported in the official model.

### Quick Start

#### Automated Launch (Windows)
Run the script:
```text
run_ui.bat
```
The script will automatically:
1. Verify Python availability on the system.
2. Create an isolated virtual environment (`venv`) if not present.
3. Install dependencies from `requirements.txt`.
4. Download missing model files (`kokoro-v1.0.onnx` and `voices-v1.0.bin`).
5. Launch the web interface at: http://127.0.0.1:7860

#### Manual Launch via Terminal
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Project Structure

```text
Kokoro/
├── app.py              # Gradio web interface
├── run_ui.bat          # Automated setup and launch script
├── requirements.txt    # Python dependencies list
├── kokoro-v1.0.onnx    # Model weights (ONNX)
├── voices-v1.0.bin     # Voice embeddings file (54 voices)
├── test_output.wav     # Sample generated audio file
└── README.md           # Project documentation
```

### Voice Naming Scheme

The model provides 54 built-in voices. Voice identifiers follow a prefix pattern:
- First character: Language or dialect
  - `a` — American English
  - `b` — British English
  - `e` — Spanish
  - `f` — French
  - `i` — Italian
  - `j` — Japanese
  - `p` — Portuguese
  - `z` — Mandarin Chinese
  - `h` — Hindi
- Second character: Gender
  - `f` — Female
  - `m` — Male

Popular voices:
- `af_heart` — balanced female voice (US)
- `af_bella`, `af_nicole`, `af_sky` — soft female voices (US)
- `am_adam`, `am_michael` — deep male voices (US)
- `bf_alice`, `bm_george` — British voices (UK)
