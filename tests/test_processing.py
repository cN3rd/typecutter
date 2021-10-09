import argparse

from typecutter.common import Cut
import typecutter.processor

######################################
# get_cut_path
######################################


def test_get_cut_path_no_name():
    cut = Cut(123, 456, None)
    args = argparse.Namespace()
    cut_path = typecutter.processor.get_cut_path(args, cut)

    assert cut_path == "123, 456.avi"


def test_get_cut_path_with_name():
    cut = Cut(123, 456, "Random")
    args = argparse.Namespace()
    cut_path = typecutter.processor.get_cut_path(args, cut)

    assert cut_path == "123, 456 Random.avi"


######################################
# get_cmd
######################################


def test_get_cmd_defualt():
    cut = Cut(123, 456, "Random")
    args = argparse.Namespace()
    cut_path = "123, 456 Random.avi"

    job = typecutter.processor.CutJob(None, cut, cut_path, args)
    cmd_gt = (
        f'ffmpeg -hide_banner -loglevel error -i pipe: -c:v ffv1 "123, 456 Random.avi"'
    )

    assert typecutter.processor.get_cmd(job) == cmd_gt


######################################
# get_cut_jobs
######################################

# TODO


######################################
# vapoursynth_get_typecut
#####################################

# TODO


######################################
# vapoursynth_process
#####################################

# TODO


######################################
# process_cuts
#####################################

# TODO
