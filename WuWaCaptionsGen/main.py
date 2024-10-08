# Download the following files:
# https://github.com/Arikatsu/WutheringWaves_Data/blob/1.3/BinData/cgVedio/videocaption.json
# https://github.com/Arikatsu/WutheringWaves_Data/blob/1.3/Textmaps/zh-Hans/multi_text/MultiText.json
# Place them in the same folder as this script.
import json
import os

import pysrt

##### Config #####
CgName = "C0002"  # The CgName of the subtitle you want to export.

##### (Basically) Static #####
CgFPS = 30  # The FPS of the video you want to export, usually 30 for WuWa.


def load_json(filename):
    script_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(script_path, filename)
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filename, data):
    script_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(script_path, filename)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_srt(filename, srt):
    script_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(script_path, filename)
    srt.save(filename)


def lookup_text(id):
    for text in MultiText:
        if text["Id"] == id:
            return text["Content"]
    return None


def frame_to_sec(frame):
    secPerFrame = 1 / CgFPS
    return frame * secPerFrame


def frame_to_ms(frame):
    msPerFrame = 1000 / CgFPS
    return frame * msPerFrame


VideoCaption = load_json("videocaption.json")
MultiText = load_json("MultiText.json")

# Filter captions
DestCaption = []
for caption in VideoCaption:
    if caption["CgName"] == CgName:
        DestCaption.append(caption)

# Sort the list by CaptionId
DestCaption.sort(key=lambda x: x["CaptionId"])

# Get the real caption text
for caption in DestCaption:
    caption["CaptionText"] = lookup_text(caption["CaptionText"])

# New subtitle
new_srt = pysrt.SubRipFile()

# Add captions
count = 0
for caption in DestCaption:
    new_srt.append(
        pysrt.SubRipItem(
            index=count,
            start=pysrt.SubRipTime(
                milliseconds=frame_to_ms(caption["ShowMoment"]),
            ),
            end=pysrt.SubRipTime(
                milliseconds=frame_to_ms(caption["ShowMoment"] + caption["Duration"]),
            ),
            text=caption["CaptionText"],
        )
    )
    count += 1

# Save
save_srt(f"{CgName}.srt", new_srt)
