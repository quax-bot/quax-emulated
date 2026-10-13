"""Prints how smooth each video of a folder is, from the frames that differ from the one before.

A frame identical to the previous one carries no motion: mpdecimate drops it, so a still screen does not
count. Gaps of over half a second are pauses between Maestro commands, not slow rendering.
"""

import os
import re
import statistics
import subprocess
import sys

PAUSE = 0.5


def unique_frame_times(video):
    result = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", video, "-vf", "mpdecimate=hi=256:lo=128:frac=0.05,showinfo", "-f", "null", "-"],
        capture_output=True, text=True)
    return [float(t) for t in re.findall(r"pts_time:([0-9.]+)", result.stderr)]


def measure(video):
    times = unique_frame_times(video)
    gaps = [b - a for a, b in zip(times, times[1:])]
    motion = [gap for gap in gaps if gap < PAUSE]
    if not motion:
        return {"unique_frames": len(times), "motion_fps": 0}
    quantiles = statistics.quantiles(motion, n=10)
    return {
        "unique_frames": len(times),
        "length_s": round(times[-1] - times[0], 1),
        "motion_fps": round(len(motion) / sum(motion), 1),
        "p50_ms": round(statistics.median(motion) * 1000),
        "p90_ms": round(quantiles[-1] * 1000),
    }


def main(folder, variant):
    videos = sorted(f for f in os.listdir(folder) if f.endswith((".mp4", ".webm")) and ".trimmed" not in f)
    if not videos:
        print(f"BENCH variant={variant} no video")
    for name in videos:
        fields = " ".join(f"{key}={value}" for key, value in measure(os.path.join(folder, name)).items())
        print(f"BENCH variant={variant} video={name} {fields}")


if __name__ == "__main__":
    main(*sys.argv[1:])
