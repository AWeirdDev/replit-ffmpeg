import os
import shutil
import time
import requests

from rich.console import Console
from rich.markdown import Markdown

def main():
    console = Console()
    
    console.print()
    console.print(
        "  I will install [blue]ffmpeg, opus and youtube dl (opt)[/blue] for you."
    )
    console.print(
        "  Make sure this REPL is clear so that nothing will be overwritten."
    )
    console.print()
    _next: str = console.input(
        "  [green]?[/green] Continue? [blue](Yn)[/blue] "
    )
    console.print()
    
    if _next.lower() not in ["y", "yes"]:
        exit(1)
    
    _plain_ans_with_ytdl = console.input(
        "  [green]?[/green] Would you also like me to install "
        "[red]youtube dl[/red]? [blue](Yn)[/blue] "
    )
    console.print()
    
    with_ytdl: bool = _plain_ans_with_ytdl.lower() in ["y", "yes"]
    
    r = None
    
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0 (Edition GX-CN)"
    }
    
    def download_ffmpeg():
        global r
        r = requests.get("https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz", headers=headers)
    
    console.print(
        "[blue]install[/blue] ffmpeg static "
        "[d white](2x attempts)[/d white]"
    )
    
    START = time.time()
    
    for _ in range(2):
        try:
            download_ffmpeg()
            break
        except requests.exceptions.SSLError:
            console.print(
                "[d red]error  [/d red][d] SSL error: retrying[/d]"
            )
    
    console.print(
        "[blue]unpack [/blue] ffmpeg static "
        "[d white]@ ffmpeg.tar.xz[/d white]"
    )
    with open('ffmpeg.tar.xz', 'wb') as f:
        f.write(r.content)
    
    os.system('tar -xf ffmpeg.tar.xz')
    
    console.print(
        "[blue]moving [/blue] ffmpeg, ffprobe"
    )
    os.system('mv ffmpeg-6.0-amd64-static/ffmpeg ffmpeg')
    os.system('mv ffmpeg-6.0-amd64-static/ffprobe ffprobe')
    
    console.print("[red]remove [/red] ffmpeg.tar.xz")
    os.remove('ffmpeg.tar.xz')
    
    # https://www.linuxfromscratch.org/blfs/view/svn/multimedia/opus.html
    
    console.print(
        "[blue]install[/blue] opus archive"
    )
    
    opus_r = requests.get("https://archive.mozilla.org/pub/opus/opus-1.3.1.tar.gz", headers=headers)
    
    with open("opus-1.3.1.tar.gz", "wb") as f:
        f.write(opus_r.content)
    
    console.print(
        "[blue]unpack [/blue] opus archive "
        "[d white]@ opus-1.3.1.tar.gz[/d white]"
    )
    
    os.system('tar -xf opus-1.3.1.tar.gz')
    os.remove("opus-1.3.1.tar.gz")
    
    console.print(
        "[blue]command[/blue] 'configure' & 'make'"
    )
    console.print()
    
    os.system("""cd opus-1.3.1 && ./configure --prefix=/usr    \
                --disable-static \
                --docdir=/usr/share/doc/opus-1.3.1 && make""")
    
    console.print()
    console.print(
        "[green]success[/green] built opus"
    )
    os.system("""mkdir opus && mv opus-1.3.1/.libs/* opus/""")
    console.print(
        "[blue]moving [/blue] 'libopus.so', 'libopus.so.0', and many other."
    )
    
    console.print()
    
    console.print(Markdown(
        """
    # It's DONE!
    Congratulations! We've installed ffmpeg and opus for your REPL!
    
    In constrast, I've:
    
    - Installed `ffmpeg` and `ffprobe` in this directory
    - Installed `opus`
    - Created a dir named `opus` that contains `libopus.so` files
    
    ...that's pretty much it!
    
    If you're making a Discord bot, whether it's `py-cord` or `discord.py`, use:
    
    ```python
    import discord
    
    discord.opus.load_opus("opus/libopus.so")
    ```
    
    That's it, and have fun hacking! <3
        """,
        "one-dark"
    ))
    
    console.print()
    
    if with_ytdl:
        console.print(
            "[d blue]extra  [/d blue][d] downloading yt-dlp[/d]..."
        )
        os.system('pip install yt-dlp --quiet')
        console.print(
            "[d blue]extra  [/d blue][d] installed yt-dlp. "
            "Use `import yt_dlp` instead of `import youtube_dl`.[/d]"
        )
        console.print()
    
    console.print(
        f"[blue]took {(time.time() - START):.2f}s[/blue]"
    )
    console.print()
    console.print(
        "  If you want to save some space for your REPL, this might help:"
    )
    console.print()
    console.input(
        "  [green]?[/green] Cleanup installed contents? [blue](Yn)[/blue] "
    )
    
    def rmdir(folder: str):
        # https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                console.print(
                    '[red]failed [/red] '
                    'cannot delete %s. Reason: %s' % (file_path, e)
                )
        os.rmdir(folder)
    
    rmdir('opus-1.3.1')
    rmdir('ffmpeg-6.0-amd64-static')
    
    console.print("[blue]all done![/blue]")
    