from fabric.api import run, cd, env, roles

env.roledefs['backend'] = [
    'vox.mediacru.sh'
]

env.roledefs['cdn'] = [
    'cdn-us-1.mediacru.sh',
    'cdn-us-2.mediacru.sh',
    'cdn-us-3.mediacru.sh',
    'cdn-asia-1.mediacru.sh',
    'cdn-eu-1.mediacru.sh',
]

@roles('backend')
def backend_hello():
    run("hostname")

def hello():
    print("hello, world!")

