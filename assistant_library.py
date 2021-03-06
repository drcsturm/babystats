#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

The Google Assistant Library can be installed with:
    env/bin/pip install google-assistant-library==0.0.2

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import subprocess
import sys
sys.path.append('../')

import aiy.assistant.auth_helpers
import aiy.audio
import aiy.voicehat
from google.assistant.library import Assistant
from google.assistant.library.event import EventType

import babystats

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

pianobar_proc = None
pandora_commands = {
    'pause music': 'p',
    'play music': 'p',
    'next song': 'n',
    'love song': '+',
    'ban song': '-',
    'stop music': 'q',
    'quit music': 'q',
}

def power_off_pi():
    aiy.audio.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    aiy.audio.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('My IP address is %s' % ip_address.decode('utf-8'))


def volume(change):

    """Changes the volume and says the new level."""

    GET_VOLUME = r'amixer get Master | grep "Front Left:" | sed "s/.*\[\([0-9]\+\)%\].*/\1/"'
    SET_VOLUME = 'amixer -q set Master %d%%'

    res = subprocess.check_output(GET_VOLUME, shell=True).strip()
    try:
        logging.info("volume: %s", res)
        vol = int(res) + change
        vol = max(0, min(100, vol))
        subprocess.call(SET_VOLUME % vol, shell=True)
        aiy.audio.say('Volume at %d %%.' % vol)
    except (ValueError, subprocess.CalledProcessError):
        logging.exception("Error using amixer to adjust volume.")


def volume_up():
    volume(10)


def volume_down():
    volume(-10)


def record_baby_stat(text):
    response = babystats.send_data_to_babystats(text)
    aiy.audio.say(response)


def start_pandora():
    pianobar_proc = subprocess.Popen(['pianobar'], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, universal_newlines=True, shell=True)
    aiy.audio.say('Pandora started')


def command_pandora(text):
    if pianobar_proc:
        subprocess.Popen(["echo -n '{}' > ~/.config/pianobar/ctl".format(pandora_commands[text])], shell=True)
    else:
        aiy.audio.say('First say start music.')
    if pandora_commands[text] == 'q':
        pianobar_proc = None


def process_event(assistant, event):
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'power off':
            assistant.stop_conversation()
            power_off_pi()
        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'ip address':
            assistant.stop_conversation()
            say_ip()
        elif text == 'volume up':
            assistant.stop_conversation()
            volume_up()
        elif text == 'volume down':
            assistant.stop_conversation()
            volume_down()
        elif text == 'start music':
            assistant.stop_conversation()
            start_pandora()
        elif text in pandora_commands.keys():
            assistant.stop_conversation()
            command_pandora(text)
        elif any(s in text for s in babystats.babystat_commands):
            assistant.stop_conversation()
            record_baby_stat(text)


    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)




def main():
    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)


if __name__ == '__main__':
    main()
