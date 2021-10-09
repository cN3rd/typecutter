import hashlib
import pathlib
import tempfile

import pytest
import typecutter.app

# Ground truth hashes
hashes_gt = {
    "1010, 1094.avi": b"\xce\x03\xef\xca_k\xb5\xcb\xe0\xc2bu\r{e\\h\xd1\xca\xd8\x98\xd8&<\xdc\x0e\xa0\x85\xcc\x8a\xc8\x0f<nE\xcf4\xdaKM\xeb\xac\xd5\xe7P\xd3\xad\x1fT\xbb\xa3\x85\x8d\xadH\xa4B\x19\xaa\x94\xe1\x80u\xe6",
    "1547, 1677 Logo.avi": b"\xc3\x87\xc4OAz\xd7\x0ee\xc3qc\xa1\xa3\nH\x910\x94R\xac\x96\xf0Z\x96\x10\xf9\xf0\xdd\xa1\xdf\xc7\x03\xe1\xddu\xa1\xdd\xe4\xb5\xe1\x96g\xe9\x0fL:\x02\x8d2\xb9\xa3\xd6\xd7Ht\xeb\x17\x11\x1e\x10d\x89g",
    "9072, 9119.avi": b'v\xff,\xae\xf8\xf3\xa9\x81\xaa^\x94\x1d\xaa\xedj\xda\xaf\xb1\xed\x1bgg\xff\xb5D\x19:6\x0e\xb8\xde\x15\x98\xd4\xb3\xf2\xd46\x15\x99\x88\x13e$\x1b\xed\x94\xafJ\x81C\xaf\xb0(\x9aaE\xba\x89\xee"\xaf\xf7#',
    "12905, 12940.avi": b"\xe9\xf4\xe1z\xfe;EN\xd8\x1c\xbc\xbfHm\xfe\xe1\xcd\xa3\x82\xa9\xadEH]T\xb9b\x02\x15\xb2\xa7\x17\xf8\xf6\xb4\x12\xb2\x00|\x1c\x19z>\x81\x0c}\xca\xf9\xa4U\xd9\xf3\x84|\x19f\xf0h\x16\xcf#\xbcZ\xe1",
    "14146, 14256 Credits1.avi": b'\xa4o\xf6\x81\x89>\x99\xc7.\xda\xa9\xbc[\x17Z\x1c\xadR;\x1f\x8a\xa3\xda\x17\x95H\r\x1e\xaf\xd1\xa9\xf8P\x17>|\xae\xf3\xc1"\xa5\x05uIo_\xd5\xd5\xd5\xa6G\xb4\xe7\xbe\xd4\x8bWK\xc5Aie?\xb2',
    "14268, 14341 Credits2.avi": b'\xeci\x88\xfboh\xd8\x15\xb6\x8c\x8cM\xbc\x0c\xf3j\n\xf3\xb5\xb3\x08\x9dK7\x89f.dr\x8c\xc4\xda\xcc\xa5\x06n\x85\x8d\xda\x92\x1b\x92S\xfe\xb4bX\x06\x1aT\x96M\xbc\xd8\xbb"w\xf0B\xfd\xbd\x1b$p',
}

random_text = "This is some random text, I swear"
hash_gt_randomtext = b"\xbf2%\xa1L[\xa66\x8c[f\xc6\x7fp5\xa8\xfbD\xa0\xa5\xdd3\x1a\xd1e{\xf4;\xd3\xbe\x04\xf9\xd3;\x06$osp\xb1L\t1\xab\xee:\xfa\xfa\xaem-@(\xf1S\x14\xa3S\xe0>[a\xb5\xe3"


def test_ffmpeg_in_path():
    import shutil

    assert shutil.which("ffmpeg") is not None


def test_vspipe_in_path():
    import shutil

    assert shutil.which("vspipe") is not None


def test_run():
    assets_directory: pathlib.Path = (
        pathlib.Path(__file__).parent.resolve().joinpath("assets")
    )
    video_file: pathlib.Path = assets_directory.joinpath("tos-source-vp9.mkv")
    cut_file: pathlib.Path = assets_directory.joinpath("cutfile.txt")

    with tempfile.TemporaryDirectory() as tempdir:
        with pytest.helpers.change_working_directory(tempdir):
            tempdir = pathlib.Path(tempdir)

            # manuall call to app
            typecutter.app.main_with_args([str(video_file), "-c", str(cut_file)])

            # glob avi files for hashes
            aviglob = tempdir.rglob("*.avi")
            hashes = {
                file.name: hashlib.sha512(file.read_bytes()).digest()
                for file in aviglob
            }

            # verify hashes
            assert len(hashes) == 6
            assert hashes["1010, 1094.avi"] == hashes_gt["1010, 1094.avi"]
            assert hashes["1547, 1677 Logo.avi"] == hashes_gt["1547, 1677 Logo.avi"]
            assert hashes["9072, 9119.avi"] == hashes_gt["9072, 9119.avi"]
            assert hashes["12905, 12940.avi"] == hashes_gt["12905, 12940.avi"]
            assert (
                hashes["14146, 14256 Credits1.avi"]
                == hashes_gt["14146, 14256 Credits1.avi"]
            )
            assert (
                hashes["14268, 14341 Credits2.avi"]
                == hashes_gt["14268, 14341 Credits2.avi"]
            )


def test_run_some_exist():
    assets_directory: pathlib.Path = (
        pathlib.Path(__file__).parent.resolve().joinpath("assets")
    )
    video_file: pathlib.Path = assets_directory.joinpath("tos-source-vp9.mkv")
    cut_file: pathlib.Path = assets_directory.joinpath("cutfile.txt")

    with tempfile.TemporaryDirectory() as tempdir:
        with pytest.helpers.change_working_directory(tempdir):
            tempdir = pathlib.Path(tempdir)

            # create some manual files
            tempdir.joinpath("14146, 14256 Credits1.avi").write_text(random_text)
            tempdir.joinpath("14268, 14341 Credits2.avi").write_text(random_text)

            # manuall call to app
            typecutter.app.main_with_args([str(video_file), "-c", str(cut_file)])

            # glob avi files for hashes
            aviglob = tempdir.rglob("*.avi")
            hashes = {
                file.name: hashlib.sha512(file.read_bytes()).digest()
                for file in aviglob
            }

            # verify hashes
            assert len(hashes) == 6
            assert hashes["1010, 1094.avi"] == hashes_gt["1010, 1094.avi"]
            assert hashes["1547, 1677 Logo.avi"] == hashes_gt["1547, 1677 Logo.avi"]
            assert hashes["9072, 9119.avi"] == hashes_gt["9072, 9119.avi"]
            assert hashes["12905, 12940.avi"] == hashes_gt["12905, 12940.avi"]
            assert hashes["14146, 14256 Credits1.avi"] == hash_gt_randomtext
            assert hashes["14268, 14341 Credits2.avi"] == hash_gt_randomtext
