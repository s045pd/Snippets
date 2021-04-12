from subprocess import DEVNULL, PIPE, Popen

error = lambda _: print(f"\x1b[1;31;40m{str(_)}\x1b[0m")
info = lambda _: print(f"\033[3;32;36m{str(_)}\033[0m")

def run_cmd(code, sync: bool = True) -> None:
    p = Popen(
        code,
        shell=True,
        **(
            {"stdout": PIPE, "stderr": PIPE}
            if sync
            else {
                "stdin": None,
                "stdout": DEVNULL,
                "stderr": DEVNULL,
                "close_fds": True,
            }
        ),
    )
    info(f"[PID:{p.pid} Sync:{sync}]\t{code}")
    if not sync:
        return
    stdout, stderr = list(map(bytes.decode, p.communicate()))
    if stderr:
        error(stderr)
    info(stdout)
    return stdout


def main():
    # sync
    run_cmd('ps -ef|grep sys|head -n 2')

    # async
    run_cmd('ping bing.com',False)


if __name__ == '__main__':
    main()