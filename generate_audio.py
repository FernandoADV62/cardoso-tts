"""Sintetiza um roteiro usando as variáveis do workflow."""
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import time

import numpy as np
import onnxruntime as ort
import soundfile as sf
from kokoro_onnx import Kokoro


def generate():
    started = time.monotonic()
    name = os.environ.get("OUTPUT", "narracao")
    text = os.environ["TEXT"].strip()
    speed = float(os.environ.get("SPEED", "1").replace(",", "."))
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", name):
        raise ValueError("Use letras, números, hífen ou sublinhado no nome.")
    if not text or not 0.5 <= speed <= 2:
        raise ValueError("Informe um texto e uma velocidade entre 0,5 e 2.")
    options = ort.SessionOptions()
    options.intra_op_num_threads = 2
    options.inter_op_num_threads = 1
    session = ort.InferenceSession("models/kokoro-v1.0.onnx", options,
                                   providers=["CPUExecutionProvider"])
    engine = Kokoro.from_session(session, "models/voices-v1.0.bin")
    samples, rate = engine.create(text, voice=os.environ.get("VOICE", "pf_dora"),
                                  speed=speed, lang=os.environ.get("LANGUAGE", "pt-br"))
    if not samples.size or not np.isfinite(samples).all() or not np.any(samples):
        raise ValueError("A síntese produziu áudio inválido.")
    peak = float(np.max(np.abs(samples)))
    samples = samples * min(1, 0.96 / peak)
    out = Path("output")
    out.mkdir(exist_ok=True)
    wav = out / (name + ".wav")
    sf.write(wav, samples, rate, subtype="PCM_16")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-codec:a",
                    "libmp3lame", "-b:a", "128k", str(wav.with_suffix(".mp3"))], check=True)
    metrics = dict(seconds=len(samples)/rate, sample_rate=rate, speed=speed,
                   render_seconds=time.monotonic()-started, source_peak=peak,
                   peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
    wav.with_suffix(".json").write_text(json.dumps(metrics, indent=2))
    print(metrics)


if __name__ == "__main__":
    generate()
