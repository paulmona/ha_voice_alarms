# Voice Alarm Assistant - Project Summary

## Overview

This project is a Home Assistant custom integration that enables voice-controlled alarm management through the built-in Home Assistant voice assistant. Users can set, list, and delete alarms using natural language voice commands.

## Project Structure

```
ha_addon/
├── custom_components/alarm_assistant/    # Main integration code
│   ├── __init__.py                       # Integration entry point
│   ├── manifest.json                     # Integration metadata
│   ├── const.py                          # Constants and configuration
│   ├── config_flow.py                    # Configuration UI
│   ├── alarm_storage.py                  # SQLite database for alarms
│   ├── alarm_manager.py                  # Alarm scheduling and triggering
│   ├── alarm_tools.py                    # LLM tools (set/list/delete)
│   ├── llm_functions.py                  # LLM API registration
│   ├── strings.json                      # UI strings
│   ├── translations/
│   │   └── en.json                       # English translations
│   └── .gitignore                        # Git ignore rules
│
├── www/alarm_sounds/                     # Alarm sound files location
│   └── README.md                         # Instructions for sound files
│
├── README.md                             # Main documentation
├── INSTALLATION.md                       # Installation instructions
├── EXAMPLES.md                           # Usage examples
├── info.md                               # Quick start info
├── hacs.json                            # HACS configuration
└── PROJECT_SUMMARY.md                    # This file
```

## Core Components

### 1. Integration Entry Point (`__init__.py`)
- Sets up the integration with Home Assistant
- Initializes the alarm manager
- Registers LLM functions
- Handles config entry lifecycle

### 2. Alarm Storage (`alarm_storage.py`)
- SQLite database for persistent alarm storage
- CRUD operations for alarms
- Supports one-time and repeating alarms
- Thread-safe singleton pattern

### 3. Alarm Manager (`alarm_manager.py`)
- Schedules alarms using Home Assistant's event system
- Triggers alarms at specified times
- Plays alarm sounds via media players
- Handles repeating alarm logic
- Sends persistent notifications

### 4. Alarm Tools (`alarm_tools.py`)
Three LLM tools for voice interaction:

- **SetAlarmTool**: Creates new alarms
  - Parameters: time, name, repeat_days (optional), sound (optional)
  - Validates time format (HH:MM)
  - Supports repeating on specific days

- **ListAlarmsTool**: Lists all configured alarms
  - Returns alarm details (ID, name, time, enabled status)
  - Formats response for natural language

- **DeleteAlarmTool**: Removes alarms
  - Delete by ID, name pattern, or all alarms
  - Flexible matching for user convenience

### 5. LLM Functions (`llm_functions.py`)
- Registers the AlarmAPI with Home Assistant's LLM system
- Manages tool availability based on configuration
- Handles registration/unregistration lifecycle

### 6. Configuration Flow (`config_flow.py`)
- User-friendly configuration UI
- Settings:
  - Enable/disable alarm functionality
  - Select media player for alarm sounds
  - Choose default alarm sound
  - Set alarm volume (0.0 - 1.0)
- Options flow for updating configuration

### 7. Constants (`const.py`)
- Domain and integration names
- Configuration keys
- Default values
- Alarm sound options
- LLM prompts

## Features

### Voice Commands
- **Set alarms**: "Set an alarm for 7:30 AM called morning alarm"
- **List alarms**: "What alarms do I have?"
- **Delete alarms**: "Delete my morning alarm"
- **Repeating alarms**: "Set an alarm for 8:00 on weekdays"

### Alarm Types
- One-time alarms
- Repeating alarms (specific days of the week)
- Custom alarm names
- Multiple alarm sounds (default, gentle, beep, chime, bell)

### Integration Features
- Persistent storage (survives restarts)
- Media player integration
- Configurable volume
- Home Assistant notifications
- Easy configuration UI

## Technical Details

### Architecture Pattern
- Follows Home Assistant integration best practices
- Uses Home Assistant's LLM Tools API
- SQLite for data persistence
- Event-driven alarm scheduling
- Singleton pattern for storage

### Dependencies
- Home Assistant 2024.1.0+
- No external Python packages required
- Uses built-in Home Assistant components:
  - `homeassistant.helpers.llm`
  - `homeassistant.helpers.event`
  - `homeassistant.config_entries`

### Data Storage
- Alarms: SQLite database at `custom_components/alarm_assistant/alarms.db`
- Sound files: `/www/alarm_sounds/*.mp3`
- Configuration: Managed by Home Assistant config entries

### Alarm Scheduling
- Uses `async_track_point_in_time` for precise scheduling
- Calculates next trigger time for repeating alarms
- Automatically reschedules after trigger
- Disables one-time alarms after triggering

### Time Format
- Internal: 24-hour format (HH:MM)
- Voice input: Natural language (converted by voice assistant)
- Timezone-aware using Home Assistant's timezone

## Installation Requirements

1. Home Assistant 2024.1.0 or newer
2. Configured voice assistant
3. At least one media player entity
4. Alarm sound files (MP3/WAV format)

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `alarm_enabled` | bool | true | Enable alarm functionality |
| `media_player_entity` | entity | None | Media player for sounds |
| `alarm_sound` | string | "default" | Default alarm sound |
| `alarm_volume` | float | 0.5 | Volume level (0.0-1.0) |

## Usage Flow

1. **User speaks command** → Home Assistant voice assistant
2. **Voice assistant processes** → Identifies alarm intent
3. **LLM calls tool** → SetAlarmTool/ListAlarmsTool/DeleteAlarmTool
4. **Tool executes** → Interacts with AlarmStorage
5. **Response generated** → Natural language response to user
6. **Alarm scheduled** → AlarmManager schedules with Home Assistant
7. **Alarm triggers** → Plays sound via media player + notification

## Alarm Trigger Flow

1. **Time reached** → Home Assistant event system triggers callback
2. **AlarmManager._trigger_alarm()** called
3. **Play sound** → Calls media_player.play_media service
4. **Send notification** → Creates persistent notification
5. **Handle recurrence**:
   - One-time: Disable alarm
   - Repeating: Schedule next occurrence

## Extensibility

### Adding Custom Sounds
1. Add sound file to `/www/alarm_sounds/`
2. Update `ALARM_SOUNDS` in `const.py`
3. Update sound mapping in `alarm_manager.py`

### Adding New Tools
1. Create new tool class in `alarm_tools.py`
2. Inherit from `llm.Tool`
3. Define `name`, `description`, `parameters`, `async_call()`
4. Register in `llm_functions.py`

### Custom Alarm Actions
Modify `AlarmManager._trigger_alarm()` to:
- Control lights
- Adjust thermostat
- Send mobile notifications
- Trigger automations

## Testing

### Manual Testing
1. Set alarm for 1 minute in future
2. Verify alarm appears in list
3. Wait for trigger
4. Confirm sound plays and notification appears
5. Check logs for any errors

### Voice Testing
1. "Set an alarm for [time]"
2. "What alarms do I have?"
3. "Delete [alarm name]"

### Debug Logging
Enable in `configuration.yaml`:
```yaml
logger:
  logs:
    custom_components.alarm_assistant: debug
```

## Known Limitations

1. Alarm sounds must be manually added by user
2. Requires media player entity for sound playback
3. One integration instance per Home Assistant installation
4. Time format limited to HH:MM (no seconds)
5. Maximum alarm storage limited by SQLite (millions+)

## Future Enhancements

Potential improvements:
- Snooze functionality
- Gradual volume increase
- Integration with sleep tracking
- Smart wake-up (based on sleep cycles)
- Alarm groups/categories
- Custom actions per alarm
- Mobile app integration
- Alarm history/analytics

## Comparison with Example

Based on the LLM Intents example project:

### Similarities
- Uses Home Assistant LLM Tools API
- Config flow for user configuration
- Multiple tools registered with API
- Similar file structure
- Options flow for updates

### Differences
- Alarm storage vs. API caching
- Scheduled tasks vs. one-time API calls
- Media player integration vs. web APIs
- Local data vs. external services
- Time-based triggers vs. on-demand

## Credits

This integration is inspired by the [LLM Intents](https://github.com/skye-harris/llm_intents) integration, which demonstrates how to add voice-controlled tools to Home Assistant.

## License

Open source - use and modify as needed for your Home Assistant installation.
