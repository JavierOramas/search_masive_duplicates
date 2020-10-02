from typer import Typer, Argument
from files_to_db import walk_dir
from generate_checksums import generate_checksums
from generate_checksums_multitheard import generate_multithreaded
app = Typer()

@app.command(name='generate', help='generate sha256 checksum of all the files on a dyrectory')
def generate(path=Argument('.')):
    walk_dir(path)
    generate_multithreaded()

if __name__ == '__main__':
    app()