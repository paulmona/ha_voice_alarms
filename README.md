# Voice Alarm Assistant for Home Assistant

A custom Home Assistant integration that enables voice-controlled alarm and timer management through the Home Assistant voice assistant.

**Author**: Pewidot
**Repository**: https://github.com/Pewidot/ha_voice_alarms

## Features

### 🎯 Alarms
- **Set Alarms**: Voice commands to set alarms at specific times
- **List Alarms**: Ask what alarms are currently set
- **Delete Alarms**: Remove alarms by ID, name, or all at once
- **Repeating Alarms**: Set alarms to repeat on specific days
- **Stop/Snooze**: Stop or snooze ringing alarms
- **Persistent Storage**: Alarms survive Home Assistant restarts

### ⏱️ Timers
- **Set Timers**: Voice commands for countdown timers
- **List Timers**: Check active timers and remaining time
- **Cancel Timers**: Stop timers before completion
- **Multiple Timers**: Run multiple timers simultaneously

### 🔊 Customization
- **Multiple Sounds**: Choose from 5 built-in sounds
- **Custom Sounds**: Use your own audio files
- **Volume Control**: Configure alarm volume
- **Media Player Integration**: Works with any HA media player

### 🌍 Multilingual
Full support for 5 languages:
- 🇺🇸 English
- 🇩🇪 German (Deutsch)
- 🇪🇸 Spanish (Español)
- 🇮🇹 Italian (Italiano)
- 🇫🇷 French (Français)

## Installation

### Manual Installation

1. **Copy integration files**
   ```bash
   # Copy to your Home Assistant config directory
   <config>/custom_components/alarm_assistant/
   ```

2. **Add alarm sounds** (optional but recommended)
   ```bash
   # Create directory and add sound files
   <config>/www/alarm_sounds/
   ```

   Add at least `default.mp3` or use the included `bell.mp3`

3. **Restart Home Assistant**

4. **Add Integration**
   - Go to **Settings** → **Devices & Services**
   - Click **+ Add Integration**
   - Search for "Voice Alarm Assistant"
   - Configure settings

### HACS Installation

Add as custom repository:
```
https://github.com/Pewidot/ha_voice_alarms
```

## Configuration

### Integration Options

- **Enable Alarms**: Turn alarm functionality on/off
- **Enable Timers**: Turn timer functionality on/off
- **Media Player**: Select media player for sounds
- **Default Sound**: Choose default alarm sound
- **Volume**: Set playback volume (0.0 - 1.0)
- **Custom Sound Path**: Path to custom sound file (optional)
- **Snooze Duration**: Default snooze time in minutes (default: 9)

### Available Sounds

- `default` - Standard alarm
- `gentle` - Soft wake-up sound
- `beep` - Simple beep
- `chime` - Pleasant chime
- `bell` - Classic bell
- `custom` - Your own sound file

## Voice Commands

### Alarms

**Set Alarms:**
```
"Set an alarm for 7:30 AM"
"Set an alarm for 14:00 called meeting"
"Set a repeating alarm for 8:00 on weekdays"
"Set an alarm for 9:00 on Monday, Wednesday, Friday"
```

**List Alarms:**
```
"What alarms do I have?"
"List my alarms"
```

**Delete Alarms:**
```
"Delete my morning alarm"
"Delete all alarms"
```

**Control Ringing Alarms:**
```
"Stop the alarm"
"Snooze"
"Snooze for 10 minutes"
```

### Timers

**Set Timers:**
```
"Set a timer for 10 minutes"
"Set a timer for 30 minutes called pizza"
"Set a timer for 2 hours"
```

**List Timers:**
```
"What timers are running?"
"Show my timers"
```

**Cancel Timers:**
```
"Cancel the pizza timer"
"Cancel all timers"
"Stop the timer"
```

## Examples

### Morning Routine
```
User: "Set an alarm for 6:30 AM called wake up"
Assistant: "Alarm 'wake up' set for 06:30"

... alarm rings at 6:30 ...

User: "Snooze"
Assistant: "Snoozed 1 alarm for 9 minutes. Will ring again at 06:39"

... alarm rings at 6:39 ...

User: "Stop the alarm"
Assistant: "Stopped 1 ringing alarm"
```

### Cooking
```
User: "Set a timer for 20 minutes called chicken"
Assistant: "Timer 'chicken' set for 20 minutes"

User: "Set a timer for 10 minutes called vegetables"
Assistant: "Timer 'vegetables' set for 10 minutes"

User: "What timers are running?"
Assistant: "You have 2 timers running: chicken (15m 30s remaining), vegetables (5m 30s remaining)"
```

### Workday Schedule
```
User: "Set a repeating alarm for 7:00 on Monday, Tuesday, Wednesday, Thursday, Friday called work"
Assistant: "Alarm 'work' set for 07:00 on mon, tue, wed, thu, fri"
```

## Technical Details

### Storage
- **Alarms**: SQLite database (`alarms.db`) - persistent across restarts
- **Timers**: In-memory storage - lost on restart
- **Sounds**: `/www/alarm_sounds/` directory

### File Structure
```
custom_components/alarm_assistant/
├── __init__.py              # Integration entry point
├── manifest.json            # Metadata
├── const.py                 # Constants
├── config_flow.py           # Configuration UI
├── alarm_storage.py         # SQLite database
├── alarm_manager.py         # Alarm scheduling
├── alarm_tools.py           # Alarm LLM tools
├── alarm_control_tools.py   # Stop/snooze tools
├── timer_storage.py         # Timer storage
├── timer_manager.py         # Timer execution
├── timer_tools.py           # Timer LLM tools
├── llm_functions.py         # LLM API registration
└── translations/            # UI translations
    ├── en.json
    ├── de.json
    ├── es.json
    ├── it.json
    └── fr.json
```

### Alarm Time Format
- Internal: 24-hour format (HH:MM)
- Voice input: Natural language (converted automatically)
- Timezone: Uses Home Assistant's configured timezone

### Repeating Alarms
Use day abbreviations:
- `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`
- Voice assistant handles "weekdays", "weekend", etc.

## Troubleshooting

### Alarms Not Triggering
1. Check integration is enabled
2. Verify alarms exist: "What alarms do I have?"
3. Check logs for errors: Settings → System → Logs
4. Ensure media player is working

### No Sound
1. Verify media player is configured
2. Check sound files exist in `/www/alarm_sounds/`
3. Test media player manually
4. Check volume is not 0

### Voice Commands Not Working
1. Verify voice assistant is configured
2. Check integration is enabled
3. Try exact command: "Set an alarm for 7:30 AM"
4. Check logs for LLM errors

### Timer/Alarm Won't Stop
1. Say "Stop the alarm" or "Stop the timer"
2. Check media player state
3. Restart integration if needed

## Development

Built on Home Assistant's LLM Tools framework for seamless voice integration.

### Adding Custom Sounds
1. Add MP3/WAV file to `/www/alarm_sounds/`
2. Use "custom" as sound name
3. Set custom path in configuration

### Extending Functionality
- Add new tools in `alarm_tools.py` or `timer_tools.py`
- Register in `llm_functions.py`
- Follow Home Assistant LLM Tool API

## Version History

- **v1.1.0** - Added stop/snooze alarm functionality
- **v1.0.0** - Initial release with alarms, timers, multilingual support

## License

Open source - use and modify as needed for your Home Assistant installation.

## Credits

Inspired by the [LLM Intents](https://github.com/skye-harris/llm_intents) integration.

## Support

- **Issues**: https://github.com/Pewidot/ha_voice_alarms/issues
- **Repository**: https://github.com/Pewidot/ha_voice_alarms
- **Documentation**: See this README

---

**Made with ❤️ by Pewidot**
