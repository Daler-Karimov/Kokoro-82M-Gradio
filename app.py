import os
import time
import gradio as gr
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

# Пути к файлам модели
MODEL_PATH = "kokoro-v1.0.onnx"
VOICES_PATH = "voices-v1.0.bin"

# Загрузка модели
print("Загрузка модели Kokoro-82M ONNX...")
kokoro = Kokoro(MODEL_PATH, VOICES_PATH)
available_voices = kokoro.get_voices()
print(f"Модель готова. Загружено голосов: {len(available_voices)}")

# Соответствие префиксов голосов языковым кодам и описаниям
VOICE_LABELS = {
    # US English
    "af_heart": "af_heart (US Female — Популярный)",
    "af_bella": "af_bella (US Female — Мягкий)",
    "af_nicole": "af_nicole (US Female — Спокойный)",
    "af_sky": "af_sky (US Female — Светлый)",
    "af_sarah": "af_sarah (US Female — Четкий)",
    "af_alloy": "af_alloy (US Female)",
    "af_aoede": "af_aoede (US Female)",
    "af_jessica": "af_jessica (US Female)",
    "af_kore": "af_kore (US Female)",
    "af_nova": "af_nova (US Female)",
    "af_river": "af_river (US Female)",
    "am_adam": "am_adam (US Male — Глубокий)",
    "am_michael": "am_michael (US Male — Выразительный)",
    "am_echo": "am_echo (US Male)",
    "am_eric": "am_eric (US Male)",
    "am_fenrir": "am_fenrir (US Male)",
    "am_liam": "am_liam (US Male)",
    "am_onyx": "am_onyx (US Male)",
    "am_puck": "am_puck (US Male)",
    "am_santa": "am_santa (US Male)",
    
    # UK English
    "bf_alice": "bf_alice (UK Female — Элегантный)",
    "bf_emma": "bf_emma (UK Female — Дружелюбный)",
    "bf_isabella": "bf_isabella (UK Female)",
    "bf_lily": "bf_lily (UK Female)",
    "bm_george": "bm_george (UK Male — Классический)",
    "bm_fable": "bm_fable (UK Male)",
    "bm_lewis": "bm_lewis (UK Male)",
    "bm_daniel": "bm_daniel (UK Male)",

    # Other languages
    "ef_dora": "ef_dora (Spanish Female)",
    "em_alex": "em_alex (Spanish Male)",
    "em_santa": "em_santa (Spanish Male)",
    "ff_siwis": "ff_siwis (French Female)",
    "if_sara": "if_sara (Italian Female)",
    "im_nicola": "im_nicola (Italian Male)",
    "jf_alpha": "jf_alpha (Japanese Female)",
    "jf_gongitsune": "jf_gongitsune (Japanese Female)",
    "jf_nezumi": "jf_nezumi (Japanese Female)",
    "jf_tebukuro": "jf_tebukuro (Japanese Female)",
    "jm_kumo": "jm_kumo (Japanese Male)",
    "pf_dora": "pf_dora (Portuguese Female)",
    "pm_alex": "pm_alex (Portuguese Male)",
    "pm_santa": "pm_santa (Portuguese Male)",
    "zf_xiaobei": "zf_xiaobei (Chinese Female)",
    "zf_xiaoni": "zf_xiaoni (Chinese Female)",
    "zf_xiaoxiao": "zf_xiaoxiao (Chinese Female)",
    "zf_xiaoyi": "zf_xiaoyi (Chinese Female)",
    "zm_yunjian": "zm_yunjian (Chinese Male)",
    "zm_yunxi": "zm_yunxi (Chinese Male)",
    "zm_yunxia": "zm_yunxia (Chinese Male)",
    "zm_yunyang": "zm_yunyang (Chinese Male)",
    "hf_alpha": "hf_alpha (Hindi Female)",
    "hf_beta": "hf_beta (Hindi Female)",
    "hm_omega": "hm_omega (Hindi Male)",
    "hm_psi": "hm_psi (Hindi Male)",
}

PREFIX_TO_LANG = {
    "a": "en-us",
    "b": "en-gb",
    "e": "es",
    "f": "fr-fr",
    "i": "it",
    "j": "ja",
    "p": "pt-br",
    "z": "cmn",
    "h": "hi",
}

VOICE_CHOICES = [(VOICE_LABELS.get(v, v), v) for v in available_voices]
VOICE_CHOICES.sort(key=lambda x: (x[1] != "af_heart", x[0]))

def generate_speech(text: str, voice: str, speed: float, manual_lang: str):
    if not text.strip():
        return None, "Пожалуйста, введите текст для озвучивания."
    
    if manual_lang and manual_lang != "Автоматически по голосу":
        lang = manual_lang
    else:
        prefix = voice[0] if voice else "a"
        lang = PREFIX_TO_LANG.get(prefix, "en-us")
    
    start_time = time.time()
    try:
        samples, sample_rate = kokoro.create(
            text=text.strip(),
            voice=voice,
            speed=speed,
            lang=lang
        )
    except Exception as e:
        return None, f"Ошибка генерации: {str(e)}"
    
    generation_time = time.time() - start_time
    audio_duration = len(samples) / sample_rate
    speedup = audio_duration / generation_time if generation_time > 0 else 0
    
    max_val = np.max(np.abs(samples))
    if max_val > 0:
        samples = samples / max_val * 0.95
        
    stats_msg = (
        f"**Успешно сгенерировано**\n\n"
        f"Время генерации: `{generation_time:.2f} сек` | "
        f"Длительность аудио: `{audio_duration:.2f} сек` | "
        f"Скорость: **`{speedup:.1f}x` быстрее реального времени**"
    )
    
    return (sample_rate, samples), stats_msg

with gr.Blocks(title="Kokoro-82M TTS") as demo:
    gr.Markdown(
        """
        # Kokoro-82M Text-to-Speech (Local UI)
        Локальная TTS-модель (82M параметров) со студийным качеством звука (24 кГц).
        """
    )
    
    with gr.Row():
        with gr.Column(scale=3):
            text_input = gr.Textbox(
                label="Текст для озвучивания",
                placeholder="Введите текст на поддерживаемом языке...",
                lines=5,
                value="Hello! Kokoro is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture, it delivers comparable quality to much larger models."
            )
            
            with gr.Row():
                voice_select = gr.Dropdown(
                    label="Голос (Всего 54 голоса)",
                    choices=VOICE_CHOICES,
                    value="af_heart"
                )
                speed_slider = gr.Slider(
                    label="Скорость речи",
                    minimum=0.5,
                    maximum=2.0,
                    value=1.0,
                    step=0.05
                )
                lang_override = gr.Dropdown(
                    label="Язык (lang)",
                    choices=[
                        "Автоматически по голосу",
                        "en-us",
                        "en-gb",
                        "es",
                        "fr-fr",
                        "it",
                        "ja",
                        "pt-br",
                        "cmn",
                        "hi"
                    ],
                    value="Автоматически по голосу"
                )
                
            generate_btn = gr.Button("Сгенерировать речь", variant="primary", size="lg")

        with gr.Column(scale=2):
            audio_output = gr.Audio(label="Результат", type="numpy", autoplay=True)
            stats_output = gr.Markdown()
            
    gr.Examples(
        examples=[
            [
                "Welcome to the local text-to-speech studio! Kokoro is running directly on your hardware with near-instant generation.",
                "af_heart",
                1.0,
                "Автоматически по голосу"
            ],
            [
                "Good evening. In other news today, scientific advancements continue to reshape the landscape of artificial intelligence.",
                "bm_george",
                1.0,
                "Автоматически по голосу"
            ],
            [
                "The quick brown fox jumps over the lazy dog. Can you believe how natural this voice sounds?",
                "am_adam",
                1.0,
                "Автоматически по голосу"
            ],
            [
                "Bonjour! La synthese vocale avec Kokoro est incroyablement rapide et naturelle.",
                "ff_siwis",
                1.0,
                "Автоматически по голосу"
            ],
            [
                "Hola! Este es un modelo de texto a voz muy rapido y de codigo abierto.",
                "ef_dora",
                1.0,
                "Автоматически по голосу"
            ]
        ],
        inputs=[text_input, voice_select, speed_slider, lang_override],
        outputs=[audio_output, stats_output],
        fn=generate_speech,
        cache_examples=False
    )
    
    generate_btn.click(
        fn=generate_speech,
        inputs=[text_input, voice_select, speed_slider, lang_override],
        outputs=[audio_output, stats_output]
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft(), inbrowser=True)
