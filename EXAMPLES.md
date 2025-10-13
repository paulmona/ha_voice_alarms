# Usage Examples

## Basic Alarm Commands

### Setting Simple Alarms

**Command**: "Set an alarm for 7:00 AM"
**Result**: Creates a one-time alarm at 07:00 with a default name

**Command**: "Set an alarm for 14:30 called meeting reminder"
**Result**: Creates a one-time alarm at 14:30 named "meeting reminder"

**Command**: "Wake me up at 6:45"
**Result**: Creates a one-time alarm at 06:45

### Setting Repeating Alarms

**Command**: "Set an alarm for 7:00 every Monday"
**Result**: Alarm repeats every Monday at 07:00

**Command**: "Set an alarm for 8:00 on weekdays"
**Result**: Alarm repeats Monday through Friday at 08:00

**Command**: "Set a repeating alarm for 9:00 on Monday, Wednesday, and Friday called workout"
**Result**: Alarm repeats on specified days at 09:00

### Choosing Alarm Sounds

**Command**: "Set an alarm for 7:00 with gentle sound"
**Result**: Creates alarm with the gentle wake-up sound

**Command**: "Set an alarm for 6:30 with chime sound called morning"
**Result**: Creates alarm with chime sound

## Listing Alarms

**Command**: "What alarms do I have?"
**Response**: "You have 2 alarms set: morning alarm at 07:00, and meeting reminder at 14:30"

**Command**: "List all my alarms"
**Response**: Lists all configured alarms with their times and settings

**Command**: "Show me my alarms"
**Response**: Displays all active alarms

## Deleting Alarms

### Delete by Name

**Command**: "Delete my morning alarm"
**Result**: Removes alarm(s) with "morning" in the name

**Command**: "Cancel the workout alarm"
**Result**: Removes alarm(s) with "workout" in the name

### Delete All Alarms

**Command**: "Delete all alarms"
**Result**: Removes all configured alarms

**Command**: "Clear all my alarms"
**Result**: Removes all configured alarms

**Command**: "Cancel all alarms"
**Result**: Removes all configured alarms

## Complete Workflow Examples

### Morning Routine Setup

```
User: "Set an alarm for 6:30 AM called wake up"
Assistant: "Alarm 'wake up' set for 06:30"

User: "Set an alarm for 7:00 AM called breakfast with gentle sound"
Assistant: "Alarm 'breakfast' set for 07:00 with gentle sound"

User: "What alarms do I have?"
Assistant: "You have 2 alarms set: wake up at 06:30, and breakfast at 07:00"
```

### Workday Schedule

```
User: "Set a repeating alarm for 7:00 on Monday, Tuesday, Wednesday, Thursday, and Friday called workday"
Assistant: "Alarm 'workday' set for 07:00 on mon, tue, wed, thu, fri"

User: "Set an alarm for 12:00 on weekdays called lunch break"
Assistant: "Alarm 'lunch break' set for 12:00 on mon, tue, wed, thu, fri"
```

### Managing Multiple Alarms

```
User: "What alarms do I have?"
Assistant: "You have 4 alarms set: wake up at 06:30, breakfast at 07:00, workday at 07:00 on weekdays, lunch break at 12:00 on weekdays"

User: "Delete the breakfast alarm"
Assistant: "Deleted 1 alarm matching 'breakfast'"

User: "What alarms do I have now?"
Assistant: "You have 3 alarms set: wake up at 06:30, workday at 07:00 on weekdays, lunch break at 12:00 on weekdays"
```

### Weekend vs Weekday Alarms

```
User: "Set an alarm for 7:00 on weekdays called work"
Assistant: "Alarm 'work' set for 07:00 on mon, tue, wed, thu, fri"

User: "Set an alarm for 9:00 on Saturday and Sunday called weekend with gentle sound"
Assistant: "Alarm 'weekend' set for 09:00 on sat, sun with gentle sound"
```

## Advanced Use Cases

### Medication Reminders

```
User: "Set an alarm for 8:00 called morning medication"
User: "Set an alarm for 20:00 called evening medication"
User: "Set an alarm for 12:00 called lunch medication"
```

### Exercise Schedule

```
User: "Set an alarm for 6:00 on Monday, Wednesday, Friday called gym with beep sound"
User: "Set an alarm for 17:00 on Tuesday, Thursday called running with chime sound"
```

### Study/Work Breaks

```
User: "Set an alarm for 10:30 called morning break"
User: "Set an alarm for 15:00 called afternoon break"
```

### Cooking Timers (One-time)

```
User: "Set an alarm for 18:30 called check dinner"
User: "Set an alarm for 12:15 called pizza done"
```

## Troubleshooting Examples

### Alarm Not Found

```
User: "Delete my test alarm"
Assistant: "No alarms found matching 'test'"

Solution: List alarms first to see exact names
User: "What alarms do I have?"
```

### Time Format Clarification

The system uses 24-hour format internally:
- 7:00 AM = 07:00
- 2:00 PM = 14:00
- 11:30 PM = 23:30

Most voice assistants will convert natural language to the correct format.

### Repeating Days

Valid day specifications:
- "Monday" → mon
- "Tuesday" → tue
- "Wednesday" → wed
- "Thursday" → thu
- "Friday" → fri
- "Saturday" → sat
- "Sunday" → sun

You can also use:
- "weekdays" → mon, tue, wed, thu, fri
- "weekend" → sat, sun
- "every day" → all days

## Configuration Examples

### Media Player Configuration

The integration can work with any Home Assistant media player:

```
media_player.bedroom_speaker
media_player.living_room_tv
media_player.google_home_mini
media_player.echo_dot
media_player.sonos_kitchen
```

### Volume Settings

Recommended volume levels:
- Gentle wake-up: 0.3 - 0.5
- Normal alarm: 0.5 - 0.7
- Urgent alarm: 0.7 - 1.0

### Custom Sound Setup

To add custom sounds:

1. Add your MP3 file to `/www/alarm_sounds/custom.mp3`
2. Modify `alarm_manager.py` to include:
   ```python
   "custom": "/local/alarm_sounds/custom.mp3"
   ```
3. Modify `const.py` to add "custom" to `ALARM_SOUNDS` list
4. Restart Home Assistant

## Integration with Automations

You can trigger automations when alarms go off by listening to the persistent notification service:

```yaml
automation:
  - alias: "Lights on when alarm triggers"
    trigger:
      platform: event
      event_type: call_service
      event_data:
        domain: persistent_notification
        service: create
    condition:
      condition: template
      value_template: "{{ 'Alarm' in trigger.event.data.service_data.title }}"
    action:
      - service: light.turn_on
        target:
          entity_id: light.bedroom
        data:
          brightness: 255
```

## Testing Tips

### Test Without Waiting

To test alarm functionality without waiting:

1. Set an alarm for 1 minute from now
2. Watch the Home Assistant logs
3. Verify the sound plays
4. Check for persistent notification

### Debug Mode

Enable debug logging in `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.alarm_assistant: debug
```

Then check logs:
- Settings → System → Logs
- Search for "alarm_assistant"
