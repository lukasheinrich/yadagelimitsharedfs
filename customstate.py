import os
import uuid
import shutil

class CustomState(object):
    def __init__(self, global_share, local_workdir):
        self.global_share  = global_share
        self.local_workdir = local_workdir

    @property
    def metadir(self):
        return os.path.join(self.local_workdir, '_packtivity')

    @property
    def readwrite(self):
        return [self.local_workdir]

    @property
    def readonly(self):
        return []

    def ensure(self):
        from packtivity.utils import mkdir_p
        mkdir_p(self.metadir)

    def put_file(self, local_path, global_path):
        print 'putting file from {} to {}'.format(local_path, global_path)
        shutil.copy(local_path, global_path)

    def get_file(self, local_path, global_path):
        shutil.copy(global_path, local_path)
        print 'getting file from {} to {}'.format(global_path,local_path)

    def model(self, p):
        return p

    @property
    def datamodel(self):
        return  {
            'keyword': '$type',
            'types': {
                'File': 'known_types:SimpleFile',
            },
            'literals': {
               'magics': ['global://', 'local://'],
               'parser': 'known_types:parse_literal'
            }
        }
    def json(self):
        return {
            'global_share': self.global_share,
            'local_workdir': self.local_workdir
        }

class CustomStateProvider(object):
    def __init__(self, global_share, local_workdirs):
        self.global_share = os.path.abspath(global_share)
        self.local_workdirs = os.path.abspath(local_workdirs)

    def json(self):
        return {}

    def new_state(self,name, dependencies, readonly = False):
        workdir = str(uuid.uuid4())
        state =  CustomState(self.global_share, os.path.join(self.local_workdirs,'pack-{}'.format(workdir)))
        state.ensure()
        return state

def setup(dataarg,dataopts):
    return CustomStateProvider(global_share = dataarg, local_workdirs = dataopts.get('local','local_workdirs'))
