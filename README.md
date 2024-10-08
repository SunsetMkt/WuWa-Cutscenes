# WuWa-Cutscenes

A method to export Wuthering Waves cutscenes/movies.

**Currently, there's only manual exports available. But it's not hard to automate. PRs are welcome.**

## Steps

### Install the game

[Epic Games Store](https://store.epicgames.com/en-US/p/wuthering-waves-76ebc5)

Download and run the launcher. Download the full game and **run it for fully download**.

Make sure the game is able to show login interface, otherwise the resources may not be downloaded completely. You may need to log in and change the voice language to download other voice packs.

### Unpack the resources

Run [FModel](https://github.com/4sval/FModel), select the game folder `C:\PathTo\Epic Games\WutheringWavesj3oFh\Wuthering Waves Game` (Make sure it's `Wuthering Waves Game`, not any subfolders). [Find the AES key](https://github.com/ClostroOffi/wuwa-aes-archive) to the game and load the packs.

Export the following folders (as raw files):

- `Client/Content/Aki/Movies`
- `Client/Content/Aki/WwiseAudio_Generated`

You may also need `Client/Content/Aki/ConfigDB` to know which audio is needed for the video (the videos do not have audio). But it's easy to guess from the filenames. So we just skip it. If you are curious, they are just standard SQLite database files. Use [sqlitebrowser](https://github.com/sqlitebrowser/sqlitebrowser) to open them.

Or, easier, just check the publicly available [unpacked data](https://github.com/Arikatsu/WutheringWaves_Data/blob/1.3/BinData/cgVedio/videosound.json).

Also, `Client/Content/Aki/Sequence` (as properties `json`) can be used to match `CgFile` with real file path. Besides, you can guess by filename.

### Parse Wwise `.bnk`

Get [wwiser](https://github.com/bnnm/wwiser). Select `WwiseAudio_Generated` and generate `.txtp`.

If the `.txtp` filename contains `(3313202977=2204441813)`, it contains Girl (as main character) voice. Otherwise, it contains Boy voice.

### Match videos with audios

Check the DB by yourself or [use public data](https://github.com/Arikatsu/WutheringWaves_Data/blob/1.3/BinData/cgVedio/videodata.json).

Match `CgName`-[`CgFile`](https://github.com/Arikatsu/WutheringWaves_Data/blob/1.3/BinData/cgVedio/videodata.json)-[`EventPath`](https://github.com/Arikatsu/WutheringWaves_Data/blob/1.3/BinData/cgVedio/videosound.json).

### Generate captions

For captions, `CgName`-[`ShowMoment`](https://github.com/Arikatsu/WutheringWaves_Data/blob/1.3/BinData/cgVedio/videocaption.json)-[`CaptionText`](https://github.com/Arikatsu/WutheringWaves_Data/blob/1.3/Textmaps/zh-Hans/multi_text/MultiText.json).

Check `WuWaCaptionsGen` for automatic generation.

### Let's try it out

For example, we want to export `M0206_Nvzhu`.

In `videodata.json`:

```json
{
  "CgId": 102,
  "CgName": "Start",
  "GirlOrBoy": 0,
  "CgFile": "/Game/Aki/Sequence/LevelA_Seq/Main/01/M0206/M0206_nvzhu_Mp4.M0206_nvzhu_Mp4",
  "CanSkip": true
}
```

Find `M0206_Nvzhu.mp4` in `Movies/LevelA_Seq`.

In `videosound.json`:

```json
  {
    "CaptionId": 1,
    "CgName": "Start",
    "GirlOrBoy": 2,
    "EventPath": "/Game/Aki/WwiseAudio/Events/play_sequence_music_m0206.play_sequence_music_m0206"
  },
  {
    "CaptionId": 2,
    "CgName": "Start",
    "GirlOrBoy": 2,
    "EventPath": "/Game/Aki/WwiseAudio/Events/play_sfx_lva_m0206.play_sfx_lva_m0206"
  }
```

Find `play_sequence_music_m0206.txtp`(`../Media/633609165.wem #i #b 115.654395833333`) and `play_sfx_lva_m0206.txtp`(`../Media/988310690.wem #i`).

### Decode audios

Get [vgmstream-cli](https://github.com/vgmstream/vgmstream).

In `txtp` folder, run the command:

```shell
vgmstream-cli <TXTP Filename>.txtp -o <Output Filename>.wav
```

### Combine videos and audios

Now you have one video and several audios. The easier way is to use Adobe Premiere or any video editing software. Put each audio in a separate track, and put the video in the track with audio. You may use `ffmpeg` but the command may be more complicated.

### Export the final video

Congratulations, you now have a video with audio.
