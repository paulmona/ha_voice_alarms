# Quick Start Guide

Get your Voice Alarm Assistant up and running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- [ ] Home Assistant installed and running
- [ ] Access to your Home Assistant configuration directory
- [ ] A working voice assistant (Settings → Voice Assistants)
- [ ] At least one media player (Settings → Devices & Services)

## Installation Steps

### 1. Copy Files (2 minutes)

Copy the integration to your Home Assistant:

```bash
# Navigate to your Home Assistant config directory
cd /config  # or wherever your HA config is located

# Copy the integration
cp -r /path/to/custom_components/alarm_assistant ./custom_components/
```

### 2. Add Alarm Sounds (2 minutes)

```bash
# Create sounds directory
mkdir -p /config/www/alarm_sounds

# Copy or download your alarm sounds (MP3 files)
# You need at least one sound file named default.mp3
```

**Quick Download** (if you have wget/curl):
```bash
# Example: Download free sounds from freesound.org
# (You'll need to find actual URLs for free alarm sounds)
cd /config/www/alarm_sounds
# Download your chosen alarm sounds here
```

**Or find free sounds:**
- [Freesound.org](https://freesound.org/search/?q=alarm)
- [Zapsplat](https://www.zapsplat.com/sound-effect-category/alarms/)
- [Pixabay Sounds](https://pixabay.com/sound-effects/search/alarm/)

Required files:
- `default.mp3` (minimum required)
- `gentle.mp3` (optional)
- `beep.mp3` (optional)
- `chime.mp3` (optional)
- `bell.mp3` (optional)

### 3. Restart Home Assistant (1 minute)

1. Go to **Settings** → **System**
2. Click **Restart** (top right)
3. Wait for restart to complete

### 4. Configure Integration (1 minute)

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration** (bottom right)
3. Search for **"Voice Alarm Assistant"**
4. Fill in the form:
   - ✓ Enable Alarm Management: **ON**
   - Media Player: **Select your speaker/media player**
   - Default Alarm Sound: **default**
   - Alarm Volume: **0.5** (50%)
5. Click **Submit**

### 5. Test It! (30 seconds)

Try these commands with your voice assistant:

1. "Set an alarm for 2 minutes from now called test"
2. "What alarms do I have?"
3. Wait 2 minutes... 🎵
4. "Delete my test alarm"

## Verification

### Check Integration Status

**Settings** → **Devices & Services** → Look for "Voice Alarm Assistant"
- Should show status: **Configured** ✓

### Check Logs (Optional)

**Settings** → **System** → **Logs**
- Search for: `alarm_assistant`
- Should see: "Setting up Voice Alarm Assistant integration" ✓
- Should see: "Alarm manager started" ✓

## Common First-Time Issues

### "Integration not found"
**Fix**: Ensure files are in `<config>/custom_components/alarm_assistant/` and restart HA

### "No media players available"
**Fix**: Set up a media player first (Chromecast, Sonos, etc.) then configure integration

### "Alarm doesn't play sound"
**Fix**:
1. Check file exists: `/config/www/alarm_sounds/default.mp3`
2. Test media player manually
3. Check volume isn't 0

### "Voice commands don't work"
**Fix**:
1. Ensure voice assistant is configured
2. Try the exact phrase: "Set an alarm for 7:30 AM"
3. Check integration is enabled

## Next Steps

Once you've confirmed it works:

1. **Set Real Alarms**
   - "Set an alarm for 7:00 AM called wake up"
   - "Set a repeating alarm for 8:00 on weekdays called work"

2. **Customize Sounds**
   - Add your preferred alarm sounds to `/config/www/alarm_sounds/`
   - Update default sound in integration options

3. **Adjust Settings**
   - Settings → Devices & Services → Voice Alarm Assistant → Configure
   - Change volume, default sound, or media player

4. **Read Full Docs**
   - [README.md](README.md) - Complete documentation
   - [EXAMPLES.md](EXAMPLES.md) - More voice command examples
   - [INSTALLATION.md](INSTALLATION.md) - Detailed installation guide

## Troubleshooting

If something isn't working:

1. **Check Logs**: Settings → System → Logs → Search "alarm_assistant"
2. **Restart Integration**: Settings → Devices & Services → Voice Alarm Assistant → Restart
3. **Check File Permissions**: Ensure HA can read all files
4. **Test Media Player**: Try playing something manually first

## Getting Help

- Check [README.md](README.md#troubleshooting) Troubleshooting section
- Review [INSTALLATION.md](INSTALLATION.md#troubleshooting-installation)
- Check Home Assistant logs for error messages
- Open a GitHub issue with logs and HA version

## Success Checklist

You're all set when you can:
- [x] See "Voice Alarm Assistant" in Integrations
- [x] Set an alarm with voice: "Set an alarm for [time]"
- [x] List alarms: "What alarms do I have?"
- [x] Hear alarm sound when it triggers
- [x] Delete alarms: "Delete my [alarm name]"

## What You Can Do Now

Try these realistic scenarios:

**Morning Routine**
```
"Set an alarm for 6:30 AM called wake up"
"Set an alarm for 7:00 AM called breakfast"
"Set an alarm for 7:45 AM called leave for work"
```

**Weekday Schedule**
```
"Set a repeating alarm for 7:00 on Monday, Tuesday, Wednesday, Thursday, Friday called workday"
```

**Medication Reminders**
```
"Set an alarm for 8:00 AM called morning meds"
"Set an alarm for 8:00 PM called evening meds"
```

**Flexible Management**
```
"What alarms do I have?"
"Delete my breakfast alarm"
"Delete all alarms"
```

Enjoy your voice-controlled alarm system! 🎉
