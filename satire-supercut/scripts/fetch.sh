#!/usr/bin/env bash
# Usage:
#   fetch.sh subs  <channel-or-playlist-url> [max_videos]   -> subs/*.json3 (auto captions, no video)
#   fetch.sh clip  <video_id> <start_s> <end_s>             -> raw/<id>_<start>.mp4 + raw/<id>_<start>.json (word timings)
set -euo pipefail
mode=$1; shift
YTDLP=(uvx yt-dlp --js-runtimes node -q)
case $mode in
  subs)
    mkdir -p subs
    "${YTDLP[@]}" --skip-download --write-auto-subs --sub-langs en --sub-format json3 \
      --playlist-end "${2:-80}" -o 'subs/%(id)s.%(ext)s' -- "$1" ;;
  clip)
    id=$1; s=$2; e=$3; mkdir -p raw; out="raw/${id}_${s}"
    "${YTDLP[@]}" -f 'bv*[height<=720]+ba/b[height<=720]' --merge-output-format mp4 \
      --download-sections "*${s}-${e}" --force-keyframes-at-cuts -o "${out}.mp4" -- "$id"
    spokenly transcribe file "${out}.mp4" --format json > "${out}.json" || echo "warn: transcription failed for ${out}" >&2 ;;
  *) echo "unknown mode $mode" >&2; exit 1 ;;
esac
