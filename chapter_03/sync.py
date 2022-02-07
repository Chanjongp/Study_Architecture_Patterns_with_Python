import hashlib
import os
import shutil
from pathlib import Path


def sync(source, dest):
    # 명령형 셸 1단계: 입력 수집
    source_hashes = read_paths_and_hashes(source)
    dest_hashes = read_paths_and_hashes(dest)

    # 명령형 셸 2단계: 함수형 핵 호출
    actions = determine_actions(source_hashes, dest_hashes, source, dest)

    # 명령형 셸 3단계: 출력 적용
    for action, *paths in actions:
        if action == "COPY":
            shutil.copyfile(*paths)
        if action == "MOVE":
            shutil.move(*paths)
        if action == "DELETE":
            os.remove(paths[0])


BLOCKSIZE = 65536


def hash_file(path):
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
    return hasher.hexdigest()


def read_paths_and_hashes(root):
    hashes = {}
    # 원본 폴더의 자식들을 순회하면서 파일 이름과 해시의 사전을 만든다.
    for folder, _, files in os.walk(root):
        # files: folder 안에 있는 file 이름을 배열로 반환
        # ['sync.py', 'test_sync.py', 'Makefile', 'mypy.ini', '.gitignore', 'before_sync.py', 'license.txt']
        for fn in files:
            # Path(folder) / fn) == chapter_03/before_sync.py
            hashes[hash_file(Path(folder) / fn)] = fn
    return hashes


def determine_actions(source_hashes, dest_hashes, source_folder, dest_folder):
    # sha : 해시된 파일, #filename : 파일명
    for sha, filename in source_hashes.items():
        # 해시된 파일값이 사본에 없으면
        # 원본의 경로에 있는 파일을
        # 사본의 경로로 
        # 복사한다.
        if sha not in dest_hashes:
            sourcepath = Path(source_folder) / filename
            destpath = Path(dest_folder) / filename
            yield "COPY", sourcepath, destpath

        # 사본의 해시된 파일이 원본의 파일명과 일치하지 않으면
        # 기존 사본의 경로에 있는 해시값의 다른 파일명을
        # 새로운 경로에 원본과 똑같은 파일명으로
        # 이동한다.
        elif dest_hashes[sha] != filename:
            olddestpath = Path(dest_folder) / dest_hashes[sha]
            newdestpath = Path(dest_folder) / filename
            yield "MOVE", olddestpath, newdestpath
    
    for sha, filename in dest_hashes.items():
        # 사본에 있는 파일이 원본에 없으면
        # 삭제한다.
        if sha not in source_hashes:
            yield "DELETE", dest_folder / filename
