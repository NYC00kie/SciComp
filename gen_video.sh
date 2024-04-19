#!/usr/bin/env bash

python3 -c 'import subprocess
for i in range(4):
        subprocess.call([
        "ffmpeg",
        "-framerate", "10",
        "-i", f"./out/grid_post_{i}_%d.jpg",
        "-c:v", "libx264",
        "-r", "10",
        f"output_{i}.mp4",
        "-y", "-hide_banner"
        ])'