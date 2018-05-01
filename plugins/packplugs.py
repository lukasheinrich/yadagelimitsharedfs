from packtivity.typedleafs import TypedLeafs
from packtivity.handlers.process_handlers import process
from packtivity.handlers.execution_handlers import executor
from packtivity.handlers.publisher_handlers import publisher
from packtivity.handlers.environment_handlers import environment

import known_types
import os
import uuid
import copy

def ensure_locality(fileobj, state):
    targetname = 'local-'+str(uuid.uuid4())
    local_path = os.path.join(state.local_workdir, targetname)
    fileobj.local_path = local_path
    remotepath = fileobj.path.format(global_share = state.global_share)
    state.get_file(fileobj.local_path, remotepath)

def ensure_publicity(fileobj, state):
    globalname = 'global-'+str(uuid.uuid4())
    global_path = os.path.join(state.global_share, globalname)
    fileobj.path = global_path
    state.put_file(fileobj.local_path, fileobj.path)

@process('interpolated-script-cmd', 'custom')
def hello(process_spec,parameters, state):
    localpars = copy.deepcopy(parameters)
    for p, v in localpars.leafs():
        if type(v) == known_types.SimpleFile:
            if v.path:
                ensure_locality(v, state)
            v.local_path = v.local_path.format(workdir = state.local_workdir)
            p.set(parameters, v)
            p.set(localpars, v.local_path)

    flattened = {k:v if not (type(v)==list) else ' '.join([str(x) for x in v]) for k,v in localpars.items()}

    return {
        'script':process_spec['script'].format(**localpars),
        'interpreter':process_spec['interpreter']
    }

@publisher('frompar-pub','custom')
def pub(publisher,parameters,state):
    topublish = TypedLeafs(publisher['outputmap'], parameters.leafmodel)
    for p,v in topublish.leafs():
        value = parameters[v]
        if type(value) == known_types.SimpleFile:
            if not value.path:
                ensure_publicity(value,state)
        p.set(topublish, value)
    return topublish

@environment('docker-encapsulated','custom')
def docker(environment,parameters,state):
    return environment
