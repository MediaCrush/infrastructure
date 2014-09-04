import PyCrush
import md5

from fabric.api import run, cd, env, roles, execute

def run_as(command, user="root"):
    run("sudo -u %s sh -c '%s'" % (user, command))

def compute_md5(string):
    m = md5.new()
    m.update(string)
    return m.hexdigest()

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

api = PyCrush.API()

@roles('backend')
def backend_delete(hash):
    run_as(
        "cd /home/service/MediaCrush && source bin/activate && python mcmanage.py files delete %s" % hash, user="service")

@roles('cdn')
def cdn_delete(hash):
    result = api.single(hash=hash)[0]
    files = map(lambda file: "/" + file['url'].split("/")[3], result['files']) + ["/" + hash]
    md5_list = map(lambda url: compute_md5(url), files)

    for md5 in md5_list:
        run_as("rm -f /var/nginx/cache/" + md5)

def delete_file(hash):
    execute(cdn_delete, hash)
    execute(backend_delete, hash)
