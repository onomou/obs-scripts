# OBS-Studio python scripts

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# OBS_Projector_Hotkeys.py
# Exposes hotkeys for showing Windowed and Fullscreen Projector (Preview)

import obspython as obs
import base64

# TODO: window geometry does not seem to matter; it always starts in the middle of the screen
window_geometry_64 = base64.b64encode(bytes('PyQt5.QtCore.QRect(10, 10, 0, 0)', 'utf-8')).decode('utf-8')

source_name = "Blank"

hotkey_id_array = []
hotkey_names_by_id = {}
# ------------------------------------------------------------

def fullscreen_preview(is_pressed):
    global fullscreen_monitor
    print('fullscreen', fullscreen_monitor)
    if is_pressed:
        obs.obs_frontend_open_projector('Preview', fullscreen_monitor, '', '')

def windowed_preview(is_pressed):
    if is_pressed:
        obs.obs_frontend_open_projector('Preview', -1, window_geometry_64, '')

fullscreen_monitor = 0

hotkeys = {
    'fullscreen': {
        'name': 'fullscreen_preview',
        'description': 'Show Fullscreen Projector (Preview)',
        'id': obs.OBS_INVALID_HOTKEY_ID,
        'function': fullscreen_preview,
    },
    'windowed': {
        'name': 'windowed_preview',
        'description': 'Show Windowed Projector (Preview)',
        'id': obs.OBS_INVALID_HOTKEY_ID,
        'function': windowed_preview,
    },
}

def script_load(settings):
    # obs_hotkey_register_frontend(name, description, callback)
    # Adds a frontend hotkey. The callback takes one parameter: a boolean ‘pressed’ parameter.
    global hotkeys
    for key, values in hotkeys.items():
        values['id'] = obs.obs_hotkey_register_frontend(values['name'], values['description'], values['function'])
        the_data_array = obs.obs_data_get_array(settings, values['name'])
        obs.obs_hotkey_load(hotkeys['fullscreen']['id'], the_data_array)
        obs.obs_data_array_release(the_data_array)

def script_save(settings):
    # save hotkeys in script properties
    for key, values in hotkeys.items():
        the_data_array = obs.obs_hotkey_save(values['id']) # undocumented, libobs/obs-hotkey.c, gets data array for given hotkey id
        obs.obs_data_set_array(settings, values['name'], the_data_array)
        obs.obs_data_array_release(the_data_array)

def script_update(settings):
    global fullscreen_monitor
    # print("script update")
    fullscreen_monitor = obs.obs_data_get_int(settings, "fullscreen_monitor")

def script_properties():
    # print("script props")
    props = obs.obs_properties_create()

    obs.obs_properties_add_int(
        props, "fullscreen_monitor", "Fullscreen Monitor", 0, 1, 1 # TODO: enumerate and select from available outputs, obs_enum_outputs()?
    )

    return props
