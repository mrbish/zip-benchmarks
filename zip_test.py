from __future__ import with_statement
import bz2
import commands
import gzip
import os
import timeit
import zipfile


tmp_dir = 'tmp_benchmark_zip'
if not os.path.exists(tmp_dir):
    os.system('mkdir {0}'.format(tmp_dir))
os.chdir(tmp_dir)


def make_tmp_file():
    with open('tmp_file', 'w') as f:
        for i in xrange(10000000):
            f.write('line\n')


def print_results(zipper, timer_object, filename):
    print('{zipper}:\n\ttime: {time}\n\tsize: {size}'.format(
        zipper=zipper,
        time=timer_object.timeit(number=1),
        size=os.stat(filename).st_size))


def bz2_compress(filename):
    with open(filename, 'rb') as source, \
            open('tmp_file_python.bz2', 'wb') as dest:
        dest.write(bz2.compress(source.read()))


def bz2_decompress(filename):
    with open(filename, 'rb') as source, \
            open('tmp_file_python_bz2.out', 'wb') as dest:
        dest.write(bz2.decompress(source.read()))


def gzip_compress(filename):
    with open(filename, 'rb') as source, \
            gzip.open('tmp_file_python.gz', 'wb') as dest:
        dest.write(source.read())


def gzip_decompress(filename):
    with gzip.open(filename, 'rb') as source, \
            open('tmp_file_python_gz.out', 'wb') as dest:
        dest.write(source.read())


def zip_compress(filename):
    with zipfile.ZipFile('tmp_file_python.zip', 'w') as dest:
        dest.write(filename, filename, zipfile.ZIP_DEFLATED)


def zip_decompress(filename):
    with zipfile.ZipFile(filename, "r") as source:
        source.extractall(os.getcwd() + '/tmp_zip/python')

if __name__ == '__main__':
    make_tmp_file()

    unix_bzip2 = timeit.Timer('os.system("bzip2 -fk tmp_file")', 'import os')
    unix_bunzip2 = timeit.Timer(
        'os.system("bunzip2 -fkc tmp_file.bz2 > tmp_file_bz2.out")',
        'import os')
    bz2_python = timeit.Timer('bz2_compress("tmp_file")',
                              'from __main__ import bz2_compress')
    unbz2_python = timeit.Timer('bz2_decompress("tmp_file_python.bz2")',
                                'from __main__ import bz2_decompress')

    unix_gzip = timeit.Timer('os.system("gzip -fk tmp_file")', 'import os')
    unix_gunzip = timeit.Timer(
        'os.system("gunzip -fkc tmp_file.gz > tmp_file_gz.out")',
        'import os')
    gzip_python = timeit.Timer(
        'gzip_compress("tmp_file")',
        'from __main__ import gzip_compress')
    gunzip_python = timeit.Timer(
        'gzip_decompress("tmp_file_python.gz")',
        'from __main__ import gzip_decompress')

    unix_zip = timeit.Timer('os.system("zip tmp_file tmp_file")', 'import os')
    unix_unzip = timeit.Timer(
        'os.system("unzip tmp_file.zip -d {0}")'
        .format(os.getcwd() + '/tmp_zip'),
        'import os')
    zip_python = timeit.Timer(
        'zip_compress("tmp_file")',
        'from __main__ import zip_compress')
    unzip_python = timeit.Timer(
        'zip_decompress("tmp_file_python.zip")',
        'from __main__ import zip_decompress')

    print('initial file - \'tmp_file\', size - {0}'.format(
        os.stat('tmp_file').st_size))
    print_results('UNIX bzip2', unix_bzip2, 'tmp_file.bz2')
    print_results('UNIX bunzip2', unix_bunzip2, 'tmp_file_bz2.out')
    print_results('python bzip2', bz2_python, 'tmp_file_python.bz2')
    print_results('python bunzip2', unbz2_python, 'tmp_file_python_bz2.out')

    print_results('UNIX gzip', unix_gzip, 'tmp_file.gz')
    print_results('UNIX gunzip', unix_gunzip, 'tmp_file_gz.out')
    print_results('python gzip', gzip_python, 'tmp_file_python.gz')
    print_results('python gunzip', gunzip_python, 'tmp_file_python_gz.out')

    print_results('UNIX zip', unix_zip, 'tmp_file.zip')
    print_results('UNIX unzip', unix_unzip,
                  '{0}/tmp_file'.format(os.getcwd() + '/tmp_zip'))
    print_results('python zip', zip_python, 'tmp_file_python.zip')
    print_results('python unzip', unzip_python,
                  '{0}/tmp_file'.format(os.getcwd() + '/tmp_zip/python'))

    os.system('rm -rf {0}'.format(os.getcwd()))
