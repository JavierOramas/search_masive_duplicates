import os
import sqlite3
import hashlib
import threading
import time
from os import cpu_count
import pandas

HILOS = cpu_count()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def getSize(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    return size


def gen_checksums(num_hilo, **datos):
    # print("Hilo {0} files_num_segment: {1}, contador {2}".format(num_hilo,datos['files_num_segment'],datos['contador']))
    bd = sqlite3.connect('dropbox.db')
    bd.row_factory = dict_factory
    path_files = bd.execute(" SELECT * FROM archivos WHERE checksum IS NULL LIMIT {limit} OFFSET {end}" 
                                                .format(limit=datos['files_num_segment'],end=datos['contador']))
    data = []
    for row in path_files.fetchall():
        # os.system("clear")
        file = open(row['archivo'],'rb')
        cs = hashlib.sha256(file.read()).hexdigest()
        data.append([row['archivo'], cs])
        # bd.execute("UPDATE archivos set checksum = '{checksum}' WHERE id = {id}".format(checksum=cs, id=row['id']))
        # bd.commit()
        # print("Hilo {0} calculó el Checksum {1} que tiene un tamaño de: {2}, tardó: {3} segundos".format(num_hilo, row['id'], getSize(file), time.clock() - start_time))
    df = pandas.DataFrame(data, columns=['Path', 'checksum'])
    df.to_csv(open('checksums.csv','w'), sep=';')
    
def generate_multithreaded():        
    db = sqlite3.connect('dropbox.db')
    db.row_factory = dict_factory
    fn = db.execute("SELECT COUNT(id) FROM archivos WHERE checksum IS NULL")

    files_num = fn.fetchone()
    db.close()
    files_num_segment = files_num['COUNT(id)']//HILOS

    contador = 0

    for num_hilo in range(HILOS):


        hilo = threading.Thread(target=gen_checksums, 
                                args=(num_hilo,),
                                kwargs={'files_num_segment':files_num_segment, 
                                        'contador':contador})
        hilo.start()

        contador = contador + files_num_segment + 1