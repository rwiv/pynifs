import json
import threading
import time
from datetime import datetime
from io import IOBase

from pynifs import LocalFsAccessor, S3FsAccessor, FileInfo
from pynifs.s3.s3_config import S3Config
from pynifs.utils import path_join
from tests.utils import find_project_root

with open(path_join(find_project_root(), "dev", "test_conf.json"), "r") as file:
    base_path: str = json.loads(file.read())["out_dir_path"]
with open(path_join(find_project_root(), "dev", "s3_conf.json"), "r") as file:
    s3_conf = S3Config(**json.loads(file.read()))

# ac = S3FsAccessor(s3_conf)
ac = LocalFsAccessor()
s3 = S3FsAccessor(s3_conf)

target = path_join(find_project_root(), "dev", "test_fs_conf.yaml")


def test_s3_fs():
    print()

    # start_time = time.time()
    # s3.mkdir("ts")
    # for f in ac.get_list(path_join(base_path, "ts")):
    #     with open(f.path, "rb") as file:
    #         s3.write(f"ts/{f.name}", file)
    # elapsed_time = time.time() - start_time
    # print(f"실행 시간: {elapsed_time:.6f}초")

    # parallel = 10
    # start_time = time.time()
    # s3.mkdir("ts")
    # for sub in sublist(ac.get_list(path_join(base_path, "ts")), parallel):
    #     reqs: list[tuple[str, bytes]] = []
    #     for f in sub:
    #         with open(f.path, "rb") as file:
    #             reqs.append((f"ts/{f.name}", file.read()))
    #     # write_batch(reqs)
    #     write_batch(reqs)
    # elapsed_time = time.time() - start_time
    # print(f"실행 시간: {elapsed_time:.6f}초")

    create_hierarchy()
    s3.walk(root(), lambda f: print(f.path))

    start_time = time.time()
    s3.rmdir("/")
    elapsed_time = time.time() - start_time
    print(f"실행 시간: {elapsed_time:.6f}초")

    # ac.mkdir(path_join(base_path, "zxc"))
    # ac.delete(path_join(base_path, "zxc"))
    # ac.rmdir(path_join(base_path, "zxc"))
    # 
    # stream = ac.read(path_join(find_project_root(), "dev", "s3_conf.yaml"))
    # chunk_size = 4096
    # while True:
    #     data = stream.read(chunk_size)
    #     if not data:
    #         break
    #     print(data)


def create_hierarchy():
    s3.mkdir("/a1")
    s3.mkdir("/a1/b1")
    s3.mkdir("/a1/b2")
    s3.mkdir("/a2")
    s3.mkdir("/a2/b1")
    s3.mkdir("/a2/b2")
    s3.write("/a1/b1/test1.txt", b"test")
    s3.write("/a1/b1/test2.txt", b"test")
    s3.write("/a1/b2/test1.txt", b"test")
    s3.write("/a1/b2/test2.txt", b"test")
    s3.write("/a2/b1/test1.txt", b"test")
    s3.write("/a2/b1/test2.txt", b"test")
    s3.write("/a2/b2/test1.txt", b"test")
    s3.write("/a2/b2/test2.txt", b"test")


def root():
    return FileInfo(name="/", path="/", is_dir=True, size=0, mtime=datetime.now())


def write_batch(reqs: list[tuple[str, bytes | IOBase]]):
    threads = []
    for path, data in reqs:
        thread = threading.Thread(target=s3.write, args=(path, data))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
