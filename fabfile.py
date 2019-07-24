# This file is part of sdsample
#
# sdsample is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sdsample is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with sdsample.  If not, see <http://www.gnu.org/licenses/>.

#encoding:UTF-8
import os 
from fabric import Connection, task
from patchwork.transfers import rsync
#cd, lcd
#from fabric.operations import run, local, prompt, put, sudo
#from fabric.network import needs_host
#from fabric.state import env, output
#from fabric.contrib import files

env = {}
env['project_local'] = 'investment_bot'
env['project_remote'] = 'investment_bot'

# the db name must be at most 16 chars
env['dbname'] = env['project_remote']
env['dbpass'] = '_mysql_PASSWORD'

# env['hosts'] = ['iot.cs.ucl.ac.uk'] # list of hosts for deployment here
env['host'] = 'localhost:2222' # list of hosts for deployment here
env['remote_host'] = 'iot.cs.ucl.ac.uk'
#env['hostpath'] = '/srv/django-projects/'+env['project_remote+'/'']

env['activate'] = 'source /srv/pve/' + env['project_remote'] + '/bin/activate'


def virtualenv(c, command):
    c.run(env['activate'] + ' && ' + command)

def set_user():
    #run('uname -s')
    #env['user'] = prompt("Please specify username for server: ")
    pass

@task
def touch(c):
    with c.cd('/srv/django-projects/' + env['project_remote'] + '/' + env['project_remote'] + '/'):
        c.run('touch wsgi.py')

@task
def sync(c):
    rsync(c, './', "/srv/django-projects/" + env['project_remote'] + "/",
                   exclude=("fabfile.py", "*.pyc",".git*","*.db", "*.log", "venv",
                            "uploads", 'media'),
                   delete=False,
                   rsync_opts="",
                  )
    # TODO: consider/test instead passing rsync_opts="--no-perms" -- see https://unix.stackexchange.com/questions/65621/rsync-is-changing-my-directory-permissions
    c.sudo('chmod -R g+w /srv/django-projects/' + env['project_remote'])

@task
def collect_static(c):
    with c.cd('/srv/django-projects/' + env['project_remote'] + '/'):
        virtualenv(c, 'python manage.py collectstatic --noinput')

@task
def migrate(c):
    with c.cd('/srv/django-projects/' + env['project_remote'] + '/'):
        virtualenv(c, 'python manage.py migrate')

@task
def deploy(c):
    sync(c)
    collect_static(c)
    migrate(c)
    restart_gunicorn(c)

@task
def reset_db(c):
    with c.cd('/srv/django-projects/' + env['project_remote'] + '/'):
        virtualenv(c, 'python manage.py syncdb')

@task
def restart_gunicorn(c):
    #c.sudo('systemctl daemon-reload')
    #c.sudo('systemctl restart gunicorn-' + env['project_remote'])
    c.sudo('systemctl restart gunicorn-%(project_remote)s.socket' % env)

@task
def restart_rasa(c):
    #c.sudo('systemctl daemon-reload')
    #c.sudo('systemctl restart gunicorn-' + env['project_remote'])
    c.sudo('systemctl restart rasa-actions-%(project_remote)s.service' % env)
    c.sudo('systemctl restart rasa-%(project_remote)s.service' % env)

@task
def pull_data(c):
    with c.cd('/srv/django-projects/' + env['project_remote'] + '/'):
        virtualenv(c, 'python manage.py pull_protected_store_data')

#####

@task
def setup_virtualenv(c):
    #with lcd("../" + env['project_local'] + "/"):
#     c.put("requirements_srv.txt", "/tmp/")

#     with c.cd('/srv/pve/'):
#         c.run('virtualenv -p python3 --no-site-packages %(project_remote)s' % env)

#     virtualenv(c, 'pip install -r /tmp/requirements_srv.txt')
        pass
        # TODO: check if python3.7 is available, if not install it via apt
        # then use something like c.run('virtualenv -python=/usr/bin/python3.7 %(project_remote)s' % env)
        # then install rasa via 
        # pip install rasa --extra-index-url https://pypi.rasa.com/simple
        # then 
        # pip install spacy 
        # then python -m spacy download en

@task
def setup_db(c):
    command = """echo "create database if not exists %(dbname)s; GRANT ALL ON %(dbname)s.* TO '%(dbname)s'@'localhost' IDENTIFIED BY '%(dbname)s@%(dbpass)s'; " | mysql -u root -p%(dbpass)s""" % env
    c.run(command)

@task
def setup_project(c):
    with c.cd('/srv/django-projects/'):
        virtualenv(c, 'django-admin.py startproject %(project_remote)s' % env)

@task
def setup_logfile(c):
    c.sudo('mkdir -p /srv/log/')
    c.sudo('mkdir -p /srv/log/' + env['project_remote'])
    c.sudo('chown www-data:sudo /srv/log/' + env['project_remote'])
    c.sudo('chmod g+rws /srv/log/' + env['project_remote'])
    c.sudo("echo 'start' > /srv/log/" + env['project_remote'] + '/usage.log')
    c.sudo('chown www-data:sudo /srv/log/' + env['project_remote'] + '/usage.log')
    c.sudo('chmod g+rw /srv/log/' + env['project_remote'] + '/usage.log')
    # with c.cd('/srv/log/'):

    # for older ubuntu (or updates from its existing installation) use:
    #sudo('chown www-data:admin ' + env['project_remote'] + '/usage.log')
    # for ubuntu 12.04 use:

@task
def setup_directories(c):
    with c.cd('/srv/django-projects/' + env['project_remote'] + '/'):
        c.run('mkdir templates')
        c.run('mkdir media')

@task
def setup_nginx(c):
    # TODO: this needs to be modified if non HTTPs setup is needed
    # TODO: change to server name?? CHECK!
    nginxConf_http = """
    location /%(project_remote)s {
        rewrite (.*) https://%(project_remote)s/$1 permanent;
    }
    """ % env

    nginxConf_https = """
    location /%(project_remote)s/static/ {
        alias /srv/django-projects/%(project_remote)s/media/;
    }

    location /%(project_remote)s/admin-media/ {
        alias /srv/pve/%(project_remote)s/lib/python3.5/site-packages/django/contrib/admin/media/;
    }

    location /%(project_remote)s/ {
        #proxy_pass http://localhost:8080;
        #include /etc/nginx/proxy.conf;
        rewrite /%(project_remote)s(.*) $1 break;
        include proxy_params;
        proxy_pass http://unix:/srv/django-projects/%(project_remote)s/%(project_remote)s.sock;
    }""" % env

    fname = env['project_remote'] + '.http'
    open(fname, 'w').write(nginxConf_http)
    c.put(fname, '/tmp/')
    c.sudo('mv /tmp/' + fname + ' /etc/nginx/django-projects/' + fname)
    os.remove(fname)

    fname = env['project_remote'] + '.https'
    open(fname, 'w').write(nginxConf_https)
    c.put(fname, '/tmp/')
    c.sudo('mv /tmp/' + fname + ' /etc/nginx/django-projects/' + fname)
    os.remove(fname)

    c.sudo('/etc/init.d/nginx restart')

@task
def setup_gunicorn(c):
    # TODO: test this

    gunicornServiceConf = """
[Unit]
Description=gunicorn daemon for %(project_remote)s
Requires=gunicorn-%(project_remote)s.socket
After=network.target

[Service]
PIDFile=/run/gunicorn/pid
User=costanza
Group=www-data
RuntimeDirectory=gunicorn
WorkingDirectory=/srv/django-projects/%(project_remote)s
ExecStart=/srv/pve/%(project_remote)s/bin/gunicorn --pid /srv/django-projects/%(project_remote)s/gunicorn.pid \
         --bind unix:/srv/django-projects/%(project_remote)s/%(project_remote)s.sock %(project_remote)s.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
""" % env

    fname = 'gunicorn-%(project_remote)s.service' % env
    open(fname, 'w').write(gunicornServiceConf)
    # TODO: test this
    #gunicorn_config_filename = 'gunicorn-%(project_remote)s.service' % env

    c.put(fname, '/tmp/')
    c.sudo('mv /tmp/' + fname + ' /etc/systemd/system/' + fname)
    os.remove(fname)

    gunicornSocketConf = """
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/srv/django-projects/%(project_remote)s/%(project_remote)s.sock

[Install]
WantedBy=sockets.target""" % env

    fname = 'gunicorn-%(project_remote)s.socket' % env
    open(fname, 'w').write(gunicornSocketConf)
    c.put(fname, '/tmp/')
    c.sudo('mv /tmp/' + fname + ' /etc/systemd/system/' + fname)
    os.remove(fname)

    # restart things
    restart_gunicorn(c)

@task
def setup_rasa(c):
    # TODO: test this
    # based on https://unix.stackexchange.com/questions/409609/how-to-run-a-command-inside-a-virtualenv-using-systemd
    rasaServiceConf = """
[Unit]
Description=rasa daemon for %(project_remote)s 
After=network.target

[Service]
PIDFile=/run/rasa_%(project_remote)s/pid
User=costanza
Group=www-data
RuntimeDirectory=rasa_%(project_remote)s
WorkingDirectory=/srv/django-projects/%(project_remote)s/rasachat
ExecStart=/bin/bash -c 'source  /srv/pve/%(project_remote)s/bin/activate && \
        /srv/pve/%(project_remote)s/bin/rasa \
        run -m models -p 5500 --enable-api'
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
""" % env

    fname = 'rasa-%(project_remote)s.service' % env
    open(fname, 'w').write(rasaServiceConf)
    # TODO: test this
    #gunicorn_config_filename = 'gunicorn-%(project_remote)s.service' % env

    c.put(fname, '/tmp/')
    c.sudo('mv /tmp/' + fname + ' /etc/systemd/system/' + fname)
    os.remove(fname)

    rasaActionsSocketConf = """
[Unit]
Description=rasa actions daemon for %(project_remote)s 
After=network.target

[Service]
PIDFile=/run/rasa_actions_%(project_remote)s/pid
User=costanza
Group=www-data
RuntimeDirectory=rasa_actions_%(project_remote)s
WorkingDirectory=/srv/django-projects/%(project_remote)s/rasachat
ExecStart=/bin/bash -c 'source  /srv/pve/%(project_remote)s/bin/activate && \
        /srv/pve/%(project_remote)s/bin/rasa \
        run actions'
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
""" % env

    fname = 'rasa-actions-%(project_remote)s.service' % env
    open(fname, 'w').write(rasaActionsSocketConf)
    c.put(fname, '/tmp/')
    c.sudo('mv /tmp/' + fname + ' /etc/systemd/system/' + fname)
    os.remove(fname)

    # TODO: restart things
    restart_rasa(c)

@task
def setup(c):
    setup_virtualenv(c)
    setup_db(c)
    setup_project(c)
    setup_directories(c)
    setup_nginx(c)
    setup_gunicorn(c)
    setup_logfile(c)

