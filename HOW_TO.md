# How to use these scripts

Read README.md first.

## Requirements

```pwsh
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
scoop install main/vgmstream
scoop install main/ffmpeg
scoop bucket add games
scoop install games/fmodel
```

## Download unpacked data

You may export ConfigDB from the game, or download the data from GitHub.

### For videos generation

- <https://github.com/Arikatsu/WutheringWaves_Data/blob/3.1/BinData/cgVedio/videodata.json>
- <https://github.com/Arikatsu/WutheringWaves_Data/blob/3.1/BinData/cgVedio/videosound.json>

### For captions generation

- <https://github.com/Arikatsu/WutheringWaves_Data/blob/3.1/Textmaps/zh-Hans/multi_text/MultiText.json>
- <https://github.com/Arikatsu/WutheringWaves_Data/blob/3.1/BinData/cgVedio/videocaption.json>

## Unpack the media resources

[FModel](https://github.com/4sval/FModel) [wuwa-aes-archive](https://github.com/ClostroOffi/wuwa-aes-archive)

Export the following folders (as raw files):

- `Client/Content/Aki/Movies`
- `Client/Content/Aki/WwiseAudio_Generated`

<!--
Export the following folders (as properties `json`):

- `Client/Content/Aki/Sequence/LevelA_Seq`
- `Client/Content/Aki/Sequence/LevelB_Seq`

Too big. And the filenames are already in `videodata.json`, though may not the exact name.
-->

## Parse Wwise `.bnk`

[wwiser](https://github.com/bnnm/wwiser)

Select `WwiseAudio_Generated` and generate `.txtp`.

## Generate `videos_info.json`

Run `gen_videos_info.py`.

## Generate final videos

Run `gen_final_videos_by_info.py`.
