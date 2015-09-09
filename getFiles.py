__author__ = 'ymo'

import json
from io import BytesIO
from os.path import join, exists
from os import makedirs, remove, listdir
from shutil import rmtree
from urllib import urlretrieve
import zipfile
import urllib2
from urllib import urlopen


def fetch_file(data_url, data_home='/tmp/drive/', verbose=False, cache_name = None,
                         redownload=False):
    if not exists(data_home):
        makedirs(data_home)
    try:
        fhandle = urlopen(data_url)
        findex = fhandle.read()
        meta = json.loads(findex)
        cache_name = meta['dataset_name']
        proj_home = data_home + cache_name + '/'
        if not exists(proj_home + '_SUCCESS') or redownload:
            if exists(proj_home):
                 rmtree(proj_home)
            makedirs(proj_home)
            for mfile in meta['files']:
                sfile = proj_home + mfile
                if not exists(sfile):
                    print ('Downloading %s ...' % mfile)
                    urlretrieve(meta['files'][mfile], sfile)
                    if mfile.endswith('.zip'):
                        print ('Extracting files from %s ...' % mfile)
                        with zipfile.ZipFile(sfile, "r") as z:
                            z.extractall(proj_home)
                        remove(sfile)
            open(proj_home + '_SUCCESS', 'w').close()
    except urllib2.URLError:
        print('Failed to Connect')
    except ValueError as e:
        print e
        print('Index Format Error:\n%s' % findex)
    except Exception as e:
        print e
        print('Failed to preload from %s into %s'
              % (data_url, data_home))
    finally:
        if cache_name:
            proj_home = data_home + cache_name + '/'
            if exists(proj_home):
                #print '=== File List ==='
                #print json.dumps(listdir(proj_home))
                #print '=== EOF ==='
                print 'Done fetching files into [ {proj_home} ]'.format(proj_home = proj_home)
                return proj_home
if __name__ == "__main__":
    fetch_file('https://onedrive.live.com/download?resid=CAE73F546D5A29CD!7648&authkey=!AHl2uuiWydzT6RI&ithint=file%2cjson')