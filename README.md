# Voice Alarm Assistant for Home Assistant

A custom Home Assistant integration that enables voice-controlled alarm management through the Home Assistant voice assistant.

## Features

- **Set Alarms**: Use voice commands to set alarms at specific times
- **List Alarms**: Ask what alarms are currently set
- **Delete Alarms**: Remove alarms by ID, name, or delete all at once
- **Repeating Alarms**: Set alarms to repeat on specific days of the week
- **Custom Alarm Sounds**: Choose from multiple alarm sounds
- **Media Player Integration**: Play alarm sounds through any Home Assistant media player

## Installation

### Method 1: Manual Installation

1. Copy the `custom_components/alarm_assistant` folder to your Home Assistant `custom_components` directory:
   ```
   <config_directory>/custom_components/alarm_assistant/
   ```

2. Create the alarm sounds directory:
   ```
   <config_directory>/www/alarm_sounds/
   ```

3. Add your alarm sound files (MP3 format recommended):
   - `default.mp3`
   - `gentle.mp3`
   - `beep.mp3`
   - `chime.mp3`
   - `bell.mp3`

4. Restart Home Assistant

5. Go to **Settings** → **Devices & Services** → **Add Integration**

6. Search for "Voice Alarm Assistant" and configure it

### Method 2: HACS (Coming Soon)

This integration is not yet available through HACS but can be added as a custom repository.

## Configuration

During setup, you can configure:

- **Enable Alarms**: Turn alarm functionality on or off
- **Media Player**: Select which media player to use for alarm sounds
- **Default Alarm Sound**: Choose the default sound for new alarms
- **Alarm Volume**: Set the playback volume (0.0 to 1.0)

## Voice Commands

Once configured, you can use the following types of voice commands:

### Setting Alarms

- "Set an alarm for 7:30 AM called morning alarm"
- "Wake me up at 6:00"
- "Set an alarm for 14:00 called meeting reminder"
- "Set a repeating alarm for 8:00 on Monday, Wednesday, and Friday"

### Listing Alarms

- "What alarms do I have?"
- "List my alarms"
- "Show me all alarms"

### Deleting Alarms

- "Delete my morning alarm"
- "Cancel the alarm at 7:30"
- "Delete all alarms"
- "Remove all my alarms"

## Technical Details

### Alarm Time Format

Alarms use 24-hour time format internally (HH:MM). The voice assistant will interpret natural language times and convert them appropriately.

### Repeating Alarms

When setting repeating alarms, specify days using:
- `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`

### Alarm Storage

Alarms are stored in a SQLite database located at:
```
<config_directory>/custom_components/alarm_assistant/alarms.db
```

### Alarm Sounds

Alarm sounds should be placed in:
```
<config_directory>/www/alarm_sounds/
```

The integration looks for these files:
- `default.mp3` - Default alarm sound
- `gentle.mp3` - Gentle wake-up sound
- `beep.mp3` - Simple beep sound
- `chime.mp3` - Chime sound
- `bell.mp3` - Bell sound

You can use any MP3, WAV, or other audio format supported by your media player.

## Example Voice Interactions

**User**: "Set an alarm for 7:00 AM called morning routine"
**Assistant**: "Alarm 'morning routine' set for 07:00"

**User**: "What alarms do I have?"
**Assistant**: "You have 2 alarms set: morning routine at 07:00, and meeting reminder at 14:00"

**User**: "Delete my morning routine alarm"
**Assistant**: "Deleted 1 alarm matching 'morning routine'"

## Troubleshooting

### Alarms Not Triggering

1. Check that the integration is enabled in Settings → Devices & Services
2. Verify that alarms are listed when you ask "what alarms do I have?"
3. Check Home Assistant logs for errors related to `alarm_assistant`
4. Ensure your media player entity is available and working

### No Sound When Alarm Triggers

1. Verify media player entity is configured correctly
2. Check that alarm sound files exist in `/www/alarm_sounds/`
3. Test the media player manually to ensure it works
4. Check volume settings in the integration options

### Voice Commands Not Working

1. Ensure the integration is properly set up in Settings → Devices & Services
2. Check that your voice assistant is configured and working
3. Verify the integration is enabled in the configuration
4. Check Home Assistant logs for any LLM-related errors

## Development

This integration is based on the Home Assistant LLM Tools framework, allowing seamless integration with voice assistants.

### File Structure

```
custom_components/alarm_assistant/
├── __init__.py           # Integration entry point
├── manifest.json         # Integration metadata
├── const.py             # Constants and configuration
├── config_flow.py       # Configuration UI
├── alarm_storage.py     # SQLite database for alarms
├── alarm_manager.py     # Alarm scheduling and triggering
├── alarm_tools.py       # LLM tools (set, list, delete)
└── llm_functions.py     # LLM API registration
```

## License

This project is provided as-is for use with Home Assistant.

## Credits

Inspired by the [LLM Intents](https://github.com/skye-harris/llm_intents) integration for Home Assistant.
