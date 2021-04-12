from pathlib import Path
from tqdm import tqdm


def get_groups(f_src: Path) -> dict:
    groups = {}
    last_indexs = last_positon = 0
    with f_src.open("r") as src:
        for line in tqdm(iter(src.readline, ""), desc="get_groups"):
            ID, *_ = line.rstrip().split("\t")
            if ID not in groups:
                groups[ID] = {"pos": last_positon, "seq": set()}
            groups[ID]["seq"].add(last_indexs)
            last_indexs += 1
            last_positon = src.tell()
    return groups


def get_offset(keys: dict) -> dict:
    for ID, val in tqdm(keys.items(), desc="get_offset"):
        min_val = min(val["seq"])
        keys[ID]["seq"] = {i - min_val for i in val["seq"]}
    return keys


def save_results(keys: dict, f_src: Path, f_dst: Path) -> None:
    with f_src.open("r") as src, f_dst.open("w") as dst:
        for key, val in tqdm(keys.items(), desc="save_results"):
            max_indexs = max(val["seq"])
            pos = val["pos"]
            src.seek(pos)
            for i, line in enumerate(src):
                if i > max_indexs:
                    break
                if i in val["seq"]:
                    dst.write(line.rstrip() + "\n")


def main():
    # codex	xxxxx
    # code1	xxxxxx
    # code2	xxxx
    # code1	xxxxxxx
    # codex	xxxxx
    f_src = Path("input.txt")
    f_dst = Path("output.txt")
    save_results(get_offset(get_groups(f_src)), f_src, f_dst)
    # codex	xxxxx
    # codex	xxxxx
    # code1	xxxxxx
    # code1	xxxxxxx
    # code2	xxxx


if __name__ == "__main__":
    main()
