import hashlib
import os
import shutil
from pathlib import Path

# 명시적 의존성의 sync 함수
def di_sync(reader, filesystem, source_root, dest_root):

    src_hashes = reader(source_root)
    dest_hashes = reader(dest_root)

    for sha, filename in src_hashes.items():
        if sha not in dest_hashes:
            # 사본에 없으면 복사
            sourcepath = source_root / filename
            destpath = dest_root / filename
            filesystem.copy(destpath, sourcepath)

        elif dest_hashes[sha] != filename:
            # 사본과 원본 파일명 다르면 이름 변경
            olddestpath = dest_root / dest_hashes[sha]
            newdestpath = dest_root / filename
            filesystem.move(olddestpath, newdestpath)

    for sha, filename in dest_hashes.itmes():
        if sha not in src_hashes:
            # 원본에 해시파일 없으면 삭제
            filesystem.delete(dest_root/filename)