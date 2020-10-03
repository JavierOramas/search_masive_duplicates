from typer import Typer, Argument
from files_to_db import walk_dir
from generate_checksums import generate_checksums
from generate_checksums_multitheard import generate_multithreaded
app = Typer()

@app.command(name='generate', help='generate sha256 checksum of all the files on a dyrectory')
def generate(path=Argument('.')):
    
    user = input('login username ')
    password = input('login password ')
    spl_path = repr(path).split("/")
    host = spl_path[0].replace("'", '')
    path = path[len(host):]
    folder = walk_dir(path,user,password,host)
    generate_multithreaded(folder)

if __name__ == '__main__':
    app()