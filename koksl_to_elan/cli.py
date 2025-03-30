import json
from pathlib import Path
import os
import sys
import time
from koksl_to_elan.generate import to_eaf
from koksl_to_elan.convert import to_elan_obj
from pprint import pp


def main():
    try:
        dir_path = sys.argv[1]
    except:
        print("말뭉치 경로가 입력되지 않았습니다.")
        print("다음과 같이 명령어와 함께 말뭉치 경로를 입력해주세요.")
        print("> koksl <path_of_corpus>")
        exit()

    time_stamp = str(time.time())

    koksl_dir = Path(dir_path)

    """
    exception_dir = Path("../koksl.exception/")
    stopped_dir = Path.joinpath(koksl_dir, "EAF-stopped/")
    stopped_paths = list(stopped_dir.glob("**/*.eaf"))
    stopped_stems = list(map(lambda path: path.stem, stopped_paths))"
    """

    print()
    print("경로에서 말뭉치 주석 파일과 영상 파일을 찾고 있습니다.")

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

    print()
    print("경로 탐색을 마치고 변환 중입니다.")
    print()

    for json_path in json_paths:
        """
        if json_path.stem in stopped_stems:
            compl_num = compl_num + 1
            continue
        """

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
        print(f"[완료율: {rate:.2f}%] [변환: {output_path}]", end="\r")

    print()
    print("변환이 모두 완료되었습니다.")
    print()
    print("아래 경로에 변환된 eaf 파일이 저장되었습니다.")
    print()
    print(f"{output_dir.resolve()}")
    print()


if __name__ == "__main__":

    main()  # "D:/data/"
