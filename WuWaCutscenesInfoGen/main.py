# Download the following files:
# https://github.com/Arikatsu/WutheringWaves_Data/blob/1.3/BinData/cgVedio/videodata.json
# https://github.com/Arikatsu/WutheringWaves_Data/blob/1.3/BinData/cgVedio/videosound.json
# Place them in the same folder as this script.
import json
import os


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


VideoData = load_json("videodata.json")
VideoSound = load_json("videosound.json")

Cgs = []

for video in VideoData:
    Cg = {
        "CgId": 101,
        "CgName": "Start",
        "GirlOrBoy": 1,
        "CgFile": "M0206_Mp4",
        "EventPath": [],
    }
    Cg["CgId"] = video["CgId"]
    Cg["CgName"] = video["CgName"]
    Cg["GirlOrBoy"] = video["GirlOrBoy"]
    Cg["CgFile"] = video["CgFile"].rsplit("/", 1)[-1].rsplit(".", 1)[0]
    for item in VideoSound:
        if item["CgName"] == video["CgName"]:
            Cg["EventPath"].append(
                item["EventPath"].rsplit("/", 1)[-1].rsplit(".", 1)[0]
            )
    Cgs.append(Cg)

save_json("cgs.json", Cgs)
