# Rhasspy Hermes

[![Continous Integration](https://github.com/rhasspy/rhasspy-hermes/workflows/Tests/badge.svg)](https://github.com/rhasspy/rhasspy-hermes/actions)
[![PyPI package version](https://img.shields.io/pypi/v/rhasspy-hermes.svg)](https://pypi.org/project/rhasspy-hermes)
[![Python versions](https://img.shields.io/pypi/pyversions/rhasspy-hermes.svg)](https://www.python.org)
[![GitHub license](https://img.shields.io/github/license/rhasspy/rhasspy-hermes.svg)](https://github.com/rhasspy/rhasspy-hermes/blob/master/LICENSE)

Python classes for [Hermes protocol](https://docs.snips.ai/reference/hermes) support in [Rhasspy](https://rhasspy.readthedocs.io/).

## Installation

```bash
pip install rhasspy-hermes
```

## Command-Line Usage

A command-line interface is available to do some basic transcription, intent recognition, text to speech, and wakeword tasks. Run the following command:

```bash
python3 -m rhasspyhermes --help
```

to see the available commands and their options. You can add a `--debug` argument to see DEBUG information.

Each command will print the appropriate Hermes response message(s) as JSON (one per line). With the `--print-topics` flag, the MQTT topic will be printed before each JSON message.

### Examples

Transcribe multiple WAV files:

```bash
python3 -m rhasspyhermes transcribe-wav /path/to/my-1.wav /path/to/my-2.wav ...
{ ... }  # prints hermes/asr/textCaptured message for my-1.wav
{ ... }  # prints hermes/asr/textCaptured message for my-2.wav
```

Transcribe a WAV file (stdin):

```bash
python3 -m rhasspyhermes transcribe-wav < /path/to/my.wav
{ ... }  # prints hermes/asr/textCaptured message
```

Recognize an intent from text:

```bash
python3 -m rhasspyhermes recognize-intent 'turn on the living room lamp'
{ ... }  # prints hermes/intent/<intentName> message
```

Speak a sentence:

```bash
python3 -m rhasspyhermes speak-sentence --language en 'what can I do for you, human?'
{ ... }  # prints hermes/tts/sayFinished message
```

Wait for wake word:

```bash
python3 -m rhasspyhermes wait-wake
{ ... }  # prints hermes/hotword/<wakewordId>/detected message
```
