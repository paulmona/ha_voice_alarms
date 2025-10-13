# Voice Alarm Assistant

Enable voice-controlled alarm management in Home Assistant through the built-in voice assistant.

## Quick Start

After installation:

1. **Configure**: Settings → Devices & Services → Add Integration → "Voice Alarm Assistant"
2. **Select Media Player**: Choose which speaker/media player to use for alarms
3. **Add Alarm Sounds**: Place MP3 files in `<config>/www/alarm_sounds/`
4. **Test**: Try saying "Set an alarm for 7:30 AM"

## Voice Commands

### Set Alarms
- "Set an alarm for 7:30 AM called morning alarm"
- "Wake me up at 6:00"
- "Set a repeating alarm for 8:00 on Monday and Friday"

### List Alarms
- "What alarms do I have?"
- "List my alarms"

### Delete Alarms
- "Delete my morning alarm"
- "Cancel all alarms"

## Features

✓ Voice-controlled alarm management
✓ One-time and repeating alarms
✓ Custom alarm sounds
✓ Integration with Home Assistant media players
✓ Persistent alarm storage
✓ Easy configuration UI

## Requirements

- Home Assistant 2024.1.0+
- Configured voice assistant
- Media player entity
- Alarm sound files (MP3/WAV)

For detailed installation instructions, see [INSTALLATION.md](INSTALLATION.md)
