# Installation Guide

## Prerequisites

- Home Assistant 2024.1.0 or newer
- A configured voice assistant (e.g., Assist, Wyoming, etc.)
- At least one media player entity for alarm sounds

## Step-by-Step Installation

### 1. Install the Custom Component

#### Option A: Manual Installation

1. Download or clone this repository
2. Copy the `custom_components/alarm_assistant` folder to your Home Assistant configuration directory:
   ```
   <config>/custom_components/alarm_assistant/
   ```

#### Option B: HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL
6. Select "Integration" as the category
7. Click "Add"
8. Find "Voice Alarm Assistant" in the list and install it

### 2. Add Alarm Sound Files

1. Create the directory for alarm sounds:
   ```
   <config>/www/alarm_sounds/
   ```

2. Add your alarm sound files (MP3 recommended):
   - `default.mp3`
   - `gentle.mp3`
   - `beep.mp3`
   - `chime.mp3`
   - `bell.mp3`

   You can find free alarm sounds at:
   - [Freesound.org](https://freesound.org/)
   - [Zapsplat](https://www.zapsplat.com/)
   - [Pixabay](https://pixabay.com/sound-effects/)

### 3. Restart Home Assistant

1. Go to **Settings** → **System** → **Restart**
2. Wait for Home Assistant to fully restart

### 4. Add the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration** (bottom right)
3. Search for "Voice Alarm Assistant"
4. Click on it to start the configuration

### 5. Configure the Integration

During setup, you'll be asked to configure:

- **Enable Alarm Management**: Turn on to enable voice alarm commands
- **Media Player**: Select the media player entity for alarm sounds
  - Examples: `media_player.living_room`, `media_player.bedroom_speaker`
- **Default Alarm Sound**: Choose the default sound (default, gentle, beep, chime, bell)
- **Alarm Volume**: Set volume level (0.0 = silent, 1.0 = maximum)

### 6. Test the Integration

Try these voice commands:

1. "Set an alarm for 7:30 AM called test alarm"
2. "What alarms do I have?"
3. "Delete my test alarm"

## Verifying Installation

### Check Integration Status

1. Go to **Settings** → **Devices & Services**
2. Find "Voice Alarm Assistant" in the list
3. Status should show "Configured"

### Check Logs

1. Go to **Settings** → **System** → **Logs**
2. Search for "alarm_assistant"
3. Should see messages like:
   - "Setting up Voice Alarm Assistant integration"
   - "Alarm Assistant API registered with LLM system"
   - "Alarm manager started with X active alarms"

### Test Media Player

1. Go to **Developer Tools** → **Services**
2. Select `media_player.play_media`
3. Fill in:
   - Entity: Your selected media player
   - Media content ID: `/local/alarm_sounds/default.mp3`
   - Media content type: `music`
4. Click "Call Service"
5. You should hear the alarm sound

## Directory Structure After Installation

```
<config>/
├── custom_components/
│   └── alarm_assistant/
│       ├── __init__.py
│       ├── manifest.json
│       ├── const.py
│       ├── config_flow.py
│       ├── alarm_storage.py
│       ├── alarm_manager.py
│       ├── alarm_tools.py
│       ├── llm_functions.py
│       ├── strings.json
│       ├── translations/
│       │   └── en.json
│       └── alarms.db (created automatically)
└── www/
    └── alarm_sounds/
        ├── default.mp3
        ├── gentle.mp3
        ├── beep.mp3
        ├── chime.mp3
        └── bell.mp3
```

## Troubleshooting Installation

### Integration Not Found

- Ensure files are in the correct directory: `<config>/custom_components/alarm_assistant/`
- Check file permissions (should be readable by Home Assistant)
- Restart Home Assistant again

### Configuration Errors

- Check Home Assistant logs for specific error messages
- Verify all required files are present
- Ensure `manifest.json` is valid JSON

### Media Player Not Listed

- Ensure you have at least one media player entity configured
- Check that the media player is available (not unavailable/unknown)
- Try configuring the integration again

### Alarm Sounds Not Playing

- Verify files exist in `<config>/www/alarm_sounds/`
- Check file permissions
- Test media player manually first
- Ensure volume is not set to 0.0

## Updating

### Manual Update

1. Download the latest version
2. Replace files in `<config>/custom_components/alarm_assistant/`
3. Restart Home Assistant

### HACS Update

1. Open HACS
2. Go to Integrations
3. Find "Voice Alarm Assistant"
4. Click "Update" if available
5. Restart Home Assistant

## Uninstallation

1. Go to **Settings** → **Devices & Services**
2. Find "Voice Alarm Assistant"
3. Click the three dots menu
4. Select "Delete"
5. Delete the `custom_components/alarm_assistant` folder
6. (Optional) Delete `www/alarm_sounds` folder
7. Restart Home Assistant

## Getting Help

If you encounter issues:

1. Check the [README.md](README.md) for usage information
2. Review the [Troubleshooting](README.md#troubleshooting) section
3. Check Home Assistant logs for error messages
4. Open an issue on GitHub with:
   - Home Assistant version
   - Integration version
   - Relevant log messages
   - Steps to reproduce the issue
