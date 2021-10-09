import argparse
import logging
import multiprocessing
import os
import subprocess as sp
from typing import BinaryIO, List, NamedTuple, Tuple, cast

import tqdm
import vapoursynth as vs

from .common import Cut


class CutJob(NamedTuple):
    video_path: str
    cut: Cut
    cut_path: str

    global_args: argparse.Namespace


def get_cut_path(args: argparse.Namespace, cut: Cut) -> str:
    # TODO: add output directory override
    # TODO: handle adding prefixes
    cut_path = f'{cut.start}, {cut.end}{" " + cut.name if cut.name else ""}.avi'
    return cut_path


def get_cmd(job: CutJob) -> str:
    # TODO: allow overriding ffmpeg
    # TODO: allow overriding cli
    # TODO: allow overriding output directory
    cmd = f'ffmpeg -hide_banner -loglevel error -i pipe: -c:v ffv1 "{job.cut_path}"'
    return cmd


def get_cut_jobs(args: argparse.Namespace, cuts: list[Cut]) -> list[CutJob]:
    cuts_to_process: list[CutJob] = []
    for cut in cuts:
        cut_path: str = get_cut_path(args, cut)

        # skip existing cuts
        if os.path.exists(cut_path):
            # TODO: handle cuts of size 0MB, which might be faulty and thus we need to recreate them
            logging.warning(f"Skipping cut {str(cut)}: file already exists")
            continue

        cuts_to_process.append(CutJob(args.video_file, cut, cut_path, args))

    return cuts_to_process


def vapoursynth_get_typecut(job: CutJob) -> vs.VideoNode:
    import vapoursynth as vs

    core: vs.Core = vs.core

    # create and trim the video node
    video_node: vs.VideoNode = core.lsmas.LWLibavSource(job.video_path)
    video_node = video_node.std.Trim(job.cut.start, job.cut.end)

    return video_node


def vapoursynth_process(job: CutJob) -> Tuple[CutJob, bool]:
    try:
        # get video node
        # TODO: add option to evaluate script here
        video_node = vapoursynth_get_typecut(job)

        # render the output
        cmd = get_cmd(job)
        with sp.Popen(cmd, stdin=sp.PIPE) as process:
            stdin: BinaryIO = cast(BinaryIO, process.stdin)
            video_node.output(stdin, y4m=True)
            process.communicate()

        return job, True
    except:
        return job, False


def process_cuts(jobs: list[CutJob]) -> List[Tuple[CutJob, bool]]:
    if len(jobs) == None:
        return []

    with multiprocessing.Pool() as pool:
        return list(
            tqdm.tqdm(
                pool.imap_unordered(vapoursynth_process, jobs),
                total=len(jobs),
            )
        )
