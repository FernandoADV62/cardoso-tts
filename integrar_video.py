"""Uso: python integrar_video.py video.mp4 narracao.wav reels.mp4"""
import argparse
import subprocess
from pathlib import Path


def duration(path, stream):
    value = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", stream, "-show_entries",
        "stream=duration", "-of", "default=nk=1:nw=1", str(path)], text=True)
    return float(value.strip())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("video", "audio", "saida"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    video_seconds = duration(args.video, "v:0")
    audio_seconds = duration(args.audio, "a:0")
    end = max(video_seconds, audio_seconds)
    vf = ("scale=1080:1920:force_original_aspect_ratio=decrease:force_divisible_by=2,"
          "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,"
          f"tpad=stop_mode=clone:stop_duration={max(0, end-video_seconds):.6f}")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-n",
                    "-i", str(args.video), "-i", str(args.audio),
                    "-map", "0:v:0", "-map", "1:a:0", "-vf", vf,
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,apad",
                    "-t", str(end), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "18", "-c:a", "aac", "-ar", "48000", "-b:a", "160k",
                    "-movflags", "+faststart", str(args.saida)], check=True)


if __name__ == "__main__":
    main()
