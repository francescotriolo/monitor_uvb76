# Monitor UVB-76

A work-in-progress detector that listens on 4625 kHz and flags anything that isn't the standard UVB-76 "buzzer": a voice, other sounds, or silence.

## How it works

The audio is split into 50 ms blocks, and each block is reduced to a single number: its energy. The last 10 seconds are kept in a circular buffer. Every 5 seconds, the program measures how periodic that window is, using autocorrelation. It looks for a peak between 1.5 and 4 seconds, where the buzzer's rhythm (about 2.35 s) falls. It also measures the window's energy. From these two values it labels the window as "buzzer", "anomaly" or "no signal", and writes one line per window to a CSV file with date and time.

The idea is that the buzzer is almost perfectly regular, while a human voice or random sounds are not.

## Current results

On the buzzer recording, periodicity (10 s windows) stays between 0.55 and 0.70. On the voice recording, which also contains silence, it stays between 0.03 and 0.30, except for the first window (0.47). That window contains about 4 s of buzzer and 6 s of silence, and it is the only disagreement with my own listening of the transmission. The provisional threshold is 0.45.

On synthetic signals, periodicity stays above the threshold until the noise amplitude is about 3.7 times the buzzer's amplitude. The threshold is based on two recordings and one easy test case, so it needs to be recalibrated on real-world data.

## Quick start

Audio files are not included in the repository. Put `buzzer.wav` and `voce.wav` in the project folder (the buzzer comes from Wikimedia Commons, the voice from a YouTube video; `yt-dlp` and `ffmpeg` are needed to download and convert them).

```
pip install -r requirements.txt
python script_voce.py        # whole-file analysis
python flusso_simulato.py    # same analysis, replayed block by block as a simulated stream
python -m pytest
```

## Status

What works today:

- The detector analyses `.wav` files as described above.
- A simulated stream (a recording replayed block by block, plus synthetic signals) is used to test the detector in different conditions. The streaming pipeline produces the same values as the whole-file analysis on the two test recordings.
- Each window is written to a CSV log with its timestamp, the second within the stream, periodicity and energy.
- Each window is classified into one of three states: "buzzer", "anomaly" or "no signal".
- The reconnection logic (increasing delays between attempts, so as not to flood the server) is implemented and tested with a simulated source that drops. It is not connected to a real source yet.

## Limitations

- There is no connection to a real audio source yet. Connecting to the WebSDR audio WebSocket is the next step.
- The threshold and the other parameters were tuned on only two recordings. The detector has not been tested on long, varied real-world signals (fading, interference, weak reception).
- The "no signal" state only catches extreme cases (a stream of zeros). A real dead channel usually produces noise, so a proper energy threshold is still needed.
- The detector looks for the buzzer's rhythm, so any change in that rhythm would be reported as an anomaly.

Not implemented yet: a watchdog (to detect a stream that stays connected but stops delivering audio), audio recording, and notifications.

## A note on recordings

Audio recordings are not included in this repository. They are meant for personal analysis only, so please don't redistribute them.

## Language note

Code identifiers, comments and commit messages are in Italian.

| Name | Meaning |
|---|---|
| `blocchi_audio` | audio blocks |
| `periodicita_da_flusso` | periodicity over a stream |
| `classifica_finestra` | window classifier |
| `calcola_attesa` | reconnection delay |

## License
MIT