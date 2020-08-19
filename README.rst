##############
Rhasspy Hermes
##############

.. image:: https://github.com/rhasspy/rhasspy-hermes/workflows/Tests/badge.svg
   :target: https://github.com/rhasspy/rhasspy-hermes/actions
   :alt: Continuous integration

.. image:: https://img.shields.io/pypi/v/rhasspy-hermes.svg
   :target: https://pypi.org/project/rhasspy-hermes
   :alt: PyPI package version

.. image:: https://img.shields.io/pypi/pyversions/rhasspy-hermes.svg
   :target: https://www.python.org
   :alt: Supported Python versions

.. image:: https://img.shields.io/github/license/rhasspy/rhasspy-hermes.svg
   :target: https://github.com/rhasspy/rhasspy-hermes/blob/master/LICENSE
   :alt: License

Python classes for `Hermes protocol`_ support in Rhasspy_.

.. _Rhasspy: https://rhasspy.readthedocs.io/en/latest/

.. _`Hermes protocol`: https://docs.snips.ai/reference/hermes

************
Installation
************

Install the latest version of the package from PyPI:

.. code-block:: shell

  pip3 install rhasspy-hermes

******************
Command-Line Usage
******************

A command-line interface is available to do some basic transcription, intent recognition, text to speech, and wakeword tasks. Run the following command:

.. code-block:: shell

  python3 -m rhasspyhermes --help

to see the available commands and their options. You can add a ``--debug`` argument to see DEBUG information.

Each command will print the appropriate Hermes response message(s) as JSON (one per line). With the ``--print-topics`` flag, the MQTT topic will be printed before each JSON message.

Examples
========

Transcribe multiple WAV files:

.. code-block:: shell

  python3 -m rhasspyhermes transcribe-wav /path/to/my-1.wav /path/to/my-2.wav ...
  { ... }  # prints hermes/asr/textCaptured message for my-1.wav
  { ... }  # prints hermes/asr/textCaptured message for my-2.wav

Transcribe a WAV file (stdin):

.. code-block:: shell

  python3 -m rhasspyhermes transcribe-wav < /path/to/my.wav
  { ... }  # prints hermes/asr/textCaptured message

Recognize an intent from text:

.. code-block:: shell

  python3 -m rhasspyhermes recognize-intent 'turn on the living room lamp'
  { ... }  # prints hermes/intent/<intentName> message

Speak a sentence:

.. code-block:: shell

  python3 -m rhasspyhermes speak-sentence --language en 'what can I do for you, human?'
  { ... }  # prints hermes/tts/sayFinished message

Wait for wake word:

.. code-block:: shell

  python3 -m rhasspyhermes wait-wake
  { ... }  # prints hermes/hotword/<wakewordId>/detected message

*******
License
*******

This project is provided by `Michael Hansen`_ as open source software with the MIT license. See the LICENSE_ file for more information.

.. _`Michael Hansen`: mailto:hansen.mike@gmail.com

.. _LICENSE: https://github.com/rhasspy/rhasspy-hermes/blob/master/LICENSE