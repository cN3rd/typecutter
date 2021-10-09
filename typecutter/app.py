__all__ = ["setup_argparser", "validate_args", "run", "main"]


import argparse
import logging
from os.path import exists as path_exists
from typing import List

from .common import Cut
from .parser import parse_typecuts
from .processor import CutJob, get_cut_jobs, process_cuts


def setup_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    # required arguments
    parser.add_argument(
        dest="video_file",
        type=str,
        help="the video file (or Vapoursynth file)",
    )
    parser.add_argument(
        "--cutfile", "-c", dest="cut_file", help="the cuts text file", required=True
    )
    return parser


def validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if not path_exists(args.video_file):
        parser.error(f'Video file "{args.video_file}" does not exist.')

    if not path_exists(args.cut_file):
        parser.error(f'Cut file "{args.cut_file}" does not exist.')


def run(args: argparse.Namespace) -> None:
    # read cuts
    cuts: list[Cut] = []
    with open(args.cut_file, encoding="utf8") as cut_file:
        cuts = parse_typecuts(cut_file.read())

    # start processing
    cut_jobs: list[CutJob] = get_cut_jobs(args, cuts)
    if len(cut_jobs) == 0:
        return

    # iterate over all cuts
    processed_jobs: List[CutJob, bool] = process_cuts(cut_jobs)


def main_with_args(args: list[str]) -> None:
    logging.basicConfig(format="%(name)s: %(levelname)s: %(message)s")

    argparser = setup_argparser()
    parsed_args = argparser.parse_args(args=args)

    validate_args(argparser, parsed_args)
    run(parsed_args)


def main() -> None:
    import sys

    main_with_args(sys.argv)
