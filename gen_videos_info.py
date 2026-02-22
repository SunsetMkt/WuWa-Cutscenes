"""
This script is used to generate the videos_info.json file.

For each video, there's:

CgName: Str
GirlOrBoy: Str
CgFile: Str, real local path to mp4
Sound: List [Str, Str], real local path to txtp

These info are necessary to generate videos in last step.
"""

import copy
import json
import os
from functools import lru_cache

###### Change these paths ######
Movies_path = "../Movies"
WwiseAudio_Generated_txtp_path = "../WwiseAudio_Generated/txtp"

videos_info = []

video_template = {
    "CgName": "",
    "GirlOrBoy": "Girl",
    "CgFile": "",
    "Sound": [],
}


def load_json(abspath):
    with open(abspath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(abspath, data):
    with open(abspath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_abs_path(rel_path):
    if not rel_path:
        # Could be None by search_file()
        return None
    script_path = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(script_path, rel_path)
    norm_path = os.path.normpath(full_path)

    if not os.path.exists(norm_path):
        # Check existence
        return None
    return norm_path


def get_all_items_by_CgName(CgName, list):
    items = []
    for item in list:
        if item["CgName"] == CgName:
            items.append(item)
    return items


def get_filename_by_CgFile(CgFile):
    """
    CgFile is like: /Game/Aki/Sequence/LevelA_Seq/Main/01/M0206/M0206_nvzhu_Mp4.M0206_nvzhu_Mp4

    Only the last filename without extension is useable
    """
    fixup_map = {
        # These names are fixed manually since Sequence data is too large to extract
        "M0206_Mp4": "M0206_Nanzhu",
        "M0206_nvzhu_Mp4": "M0206_Nvzhu",
        "DaPaoPoJieJIe_Mp4": "DaPaoPoJieJie",
        "M2_12_20_Nan": "M2_12_20_Seq_Nan",
        "M2_12_20_Nv": "M2_12_20_Seq_Nv",
        "M2_12_23_Nvzhu": "M2_12_23_Nv",
        "M2_12_23_Nanzhu": "M2_12_23_Nan",
    }
    fn = CgFile.split("/")[-1].split(".")[0]
    return fixup_map.get(fn, fn)


@lru_cache(maxsize=32)
def _index_directory(root_dir):
    """
    Cache os.walk result
    """
    result = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            result.append(os.path.join(root, file))
    return result


def search_all_files(root_dir, target_name, case_sensitive=False):
    files = _index_directory(root_dir)
    results = []
    if not case_sensitive:
        target_name = target_name.lower()
    for path in files:
        name = os.path.basename(path)
        if case_sensitive:
            if target_name in name:
                results.append(path)
        else:
            if target_name in name.lower():
                results.append(path)
    return results


def search_file(root_dir, target_name, case_sensitive=False):
    files = search_all_files(root_dir, target_name, case_sensitive)
    if not files:
        return None
    return files[0]


def get_path_by_CgFile(CgFile):
    fn = get_filename_by_CgFile(CgFile)
    fp = search_file(Movies_path, fn)
    if not fp:
        print(f"Warning: {CgFile} not found in {Movies_path}")
        return None
    fp = get_abs_path(fp)
    return fp


def get_events_by_CgName(CgName):
    items = get_all_items_by_CgName(CgName, videosound)
    events = []
    fixup_map = {
        # These names are fixed manually since the matching does not always work
        "play_story_music_3_0_b_m3_1_11_c": "play_story_music_3_0_b_m3_1_11 (4135626798=84696444)"
    }

    for i in items:
        event = i["EventPath"].split("/")[-1].split(".")[0]
        events.append(fixup_map.get(event, event))
    return events


def get_all_sounds_by_CgName(CgName, GirlOrBoy=0):
    events = get_events_by_CgName(CgName)
    files = []

    # Girl: 0, Boy: 1
    param_map = {0: "(3313202977=2204441813)", 1: "(3313202977=3111576190)"}

    for event in events:
        # Search for all txtp with the event name
        txtp_list = search_all_files(WwiseAudio_Generated_txtp_path, event)

        # If no result, continue
        if not txtp_list:
            print(f"Warning: {event} not found in {WwiseAudio_Generated_txtp_path}")
            continue

        # If one result, use it
        if len(txtp_list) == 1:
            files.append(get_abs_path(txtp_list[0]))
            continue

        # If more than one result, use the one with the parameter
        for txtp in txtp_list:
            if param_map[GirlOrBoy] in txtp:
                files.append(get_abs_path(txtp))
                break

    return files


if __name__ == "__main__":
    videodata = load_json("videodata.json")
    videosound = load_json("videosound.json")

    print("Generating videos_info.json")

    for item in videodata:
        video = copy.deepcopy(video_template)

        # print(f"Parsing {item["CgName"]}")
        video["CgName"] = item["CgName"]

        char_map = {0: "Girl", 1: "Boy"}
        video["GirlOrBoy"] = char_map.get(item["GirlOrBoy"], "Girl")

        video["CgFile"] = get_path_by_CgFile(item["CgFile"])

        video["Sound"] = get_all_sounds_by_CgName(item["CgName"], item["GirlOrBoy"])

        videos_info.append(video)

    # Check and drop any item which CgFile is None
    videos_info = [item for item in videos_info if item["CgFile"]]

    save_json("videos_info.json", videos_info)

    print("Done")
