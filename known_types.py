class SimpleFile(object):
    def __init__(self, path = None, local_path = None):
        self.path = path
        self.local_path = local_path

    def json(self):
        return {
            'path': self.path,
            'local_path': self.local_path
        }

    @classmethod
    def fromJSON(cls, data):
        return cls(**data)

def parse_literal(literal):
    if literal.startswith('local://'):
        return {'$type': 'File', 'local_path': literal.replace('local://','')}
    if literal.startswith('global://'):
        return {'$type': 'File', 'path': '{global_share}/public0001.dat'}
    raise NotImplementedError(literal)
