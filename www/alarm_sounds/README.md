# Alarm Sounds

Place your alarm sound files in this directory. The following files are expected:

- `default.mp3` - Default alarm sound
- `gentle.mp3` - Gentle wake-up sound
- `beep.mp3` - Simple beep sound
- `chime.mp3` - Chime sound
- `bell.mp3` - Bell sound

## Format

The alarm sounds should be in MP3, WAV, or any audio format supported by your Home Assistant media player.

## Free Alarm Sound Resources

You can find free alarm sounds from these resources:

- [Freesound.org](https://freesound.org/) - Community sound library
- [Zapsplat](https://www.zapsplat.com/) - Free sound effects
- [BBC Sound Effects](https://sound-effects.bbcrewind.co.uk/) - BBC archive sounds
- [Pixabay](https://pixabay.com/sound-effects/) - Royalty-free sound effects

## Testing

After adding sound files, you can test them by:

1. Setting an alarm through the voice assistant
2. Manually triggering the media player with the sound file path:
   `/local/alarm_sounds/default.mp3`

## Custom Sounds

You can add additional custom sounds and modify the integration code in:
```
custom_components/alarm_assistant/const.py
```

Add your custom sound name to the `ALARM_SOUNDS` list and update the sound mapping in:
```
custom_components/alarm_assistant/alarm_manager.py
```
