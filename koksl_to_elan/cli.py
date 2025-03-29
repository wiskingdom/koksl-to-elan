import json
from pathlib import Path
import os
import sys
import time
from koksl_to_elan.generate import to_eaf
from koksl_to_elan.convert import to_elan_obj
from pprint import pp


def main(dir_path):
    time_stamp = str(time.time())

    koksl_dir = Path(dir_path)
    exception_dir = Path("../koksl.exception/")

    json_paths = list(koksl_dir.glob("**/*.json"))
    mp4_paths = list(koksl_dir.glob("**/*.mp4"))
    output_dir = Path.joinpath(koksl_dir, f"EAF-{time_stamp}/")

    json_num = len(json_paths)
    compl_num = 0

    os.mkdir(output_dir)

    def get_url_map(path: Path):
        file_name = path.stem
        header = r"file:///"
        abs_path = path.as_posix()
        return (file_name, f"{header}{abs_path}")

    url_map = dict(map(get_url_map, mp4_paths))

    for json_path in json_paths:

        with open(json_path, "r", encoding="utf8") as file:
            obj = json.loads(file.read())

        vfile_id = obj["vido_file_nm"]
        media_url = url_map[vfile_id]
        elan_obj = to_elan_obj(obj)
        eaf = to_eaf(media_url, elan_obj)

        output_path = Path.joinpath(output_dir, f"{vfile_id}.eaf/")

        with open(output_path, "w", encoding="utf8") as file:
            file.write(eaf)

        compl_num = compl_num + 1
        rate = compl_num / json_num * 100
        print(f"[완료율: {rate:.2f}%] [변환: {output_path}]")
    print()
    print("변환이 모두 완료되었습니다.")
    print()
    print("eaf 파일 경로:")
    print(f"{output_dir.resolve()}")
    print()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])  # "D:/data/"
    else:
        print("말뭉치 폴더의 경로를 입력해주세요.")
