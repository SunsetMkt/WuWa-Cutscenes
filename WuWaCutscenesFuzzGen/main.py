# Fuzzy filename matching
# We don't care about DBs, CgFile, EventPath, GirlOrBoy,
# or anything requiring extracted Unreal properties or SQLite databases.
# Just match anything in `Movies` with `WwiseAudio_Generated\txtp`
# The implication is very dirty.
# This is not recommended for production.
import os
import subprocess
import shutil

import ffmpeg

##### Change these #####
MoviesDir = r"C:\PathTo\FModel\Output\Exports\Client\Content\Aki\Movies"
WwiseAudio_GeneratedDir = r"C:\PathTo\FModel\Output\Exports\Client\Content\Aki\WwiseAudio_Generated"
Girl = True  # True will only extract Girl videos, False will only extract Boy videos. Reduces complexity.
########################

OutputDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Output")
TempDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Temp")
TxtpDir = os.path.join(WwiseAudio_GeneratedDir, "txtp")
GirlKeywords = ["(3313202977=2204441813)", "NvZhu"]
BoyKeywords = ["(3313202977=3111576190)", "NanZhu"]

os.makedirs(OutputDir, exist_ok=True)
os.makedirs(TempDir, exist_ok=True)


def list_files_recursive(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for f in filenames:
            files.append(os.path.join(root, f))
    return files


def get_file_name(file):
    return os.path.splitext(os.path.basename(file))[0]


def drop_files_by_keyword(items, kwlist):
    for item in items:
        for kw in kwlist:
            if kw.lower() in item.lower():
                items.remove(item)
    return items


def get_audios_by_name(name):
    TxtpList = []
    for file in list_files_recursive(TxtpDir):
        if name.lower() in get_file_name(file).lower():
            TxtpList.append(file)
        if name.split("_")[0].lower() in get_file_name(file).lower():
            TxtpList.append(file)

    # Remove duplicates
    TxtpList = list(dict.fromkeys(TxtpList))
    return TxtpList


def call_vgmstream(txtp, wav):
    subprocess.run(
        [
            "vgmstream-cli",
            txtp,
            "-o",
            wav,
        ],
        stdout=subprocess.DEVNULL,
    )
    return wav


def txtps_to_wavs(txtps):
    wavs = []
    for txtp in txtps:
        outfile = os.path.join(TempDir, get_file_name(txtp) + ".wav")
        call_vgmstream(txtp, outfile)
        wavs.append(outfile)
    return wavs


def merge_wavs(wavs):
    outfile = os.path.join(TempDir, get_file_name(wavs[0]) + "_merged.wav")
    streams = []
    for wav in wavs:
        streams.append(ffmpeg.input(wav))
    ffmpeg.filter(streams, "amerge", inputs=len(wavs)).output(outfile, ac=2).run(
        quiet=True, overwrite_output=True
    )
    # FIXME: Might shorten audio by the shortest one, not expected
    return outfile


def get_available_filename(file):
    purename = os.path.splitext(os.path.basename(file))[0]
    ext = os.path.splitext(os.path.basename(file))[1]
    folder = os.path.dirname(os.path.realpath(file))
    if os.path.exists(file):
        i = 1
        while True:
            filename = f"{purename}_{i}.{ext}"
            if not os.path.exists(os.path.join(folder, filename)):
                return os.path.join(folder, filename)
            i += 1
    else:
        return file


def merge_video_audio(video, audio):
    outfile = get_available_filename(
        os.path.join(OutputDir, get_file_name(video) + "_merged.mp4")
    )
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            video,
            "-i",
            audio,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            outfile,
            "-y",
            "-loglevel",
            "error",
        ],
    )
    return outfile


if __name__ == "__main__":
    # Girl or not?
    if Girl:
        DropKeywords = BoyKeywords
    else:
        DropKeywords = GirlKeywords

    # Collect movies
    MoviesList = list_files_recursive(MoviesDir)
    MoviesList = drop_files_by_keyword(MoviesList, DropKeywords)

    # For each movie
    for movie in MoviesList:
        print(f"Processing {movie}")

        # Get audios
        TxtpList = drop_files_by_keyword(
            get_audios_by_name(get_file_name(movie)), DropKeywords
        )

        # print(f"Found {len(TxtpList)} audios")
        print(TxtpList)

        if len(TxtpList) == 0:
            print(f"{movie} has no txtp, copying original")
            # Copy original
            outfile = os.path.join(OutputDir, get_file_name(movie) + "_original.mp4")
            shutil.copyfile(movie, outfile)
            continue

        # Convert to wavs
        # print("Converting to wavs")
        WavList = txtps_to_wavs(TxtpList)

        # Merge wavs
        # print("Merging wavs")
        MergedWav = merge_wavs(WavList)

        # Merge to movie
        # print("Merging to movie")
        MergedMovie = merge_video_audio(movie, MergedWav)

    print("Done")
