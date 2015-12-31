from fabric.api import run, sudo, hosts, env, cd, put
from fabric.contrib import files

system_packages = ("git python-pip apache2 libapache2-mod-wsgi libpq-dev "
                  "python-dev postfix-policyd-spf-python postfix-pgsql "
                  "nfs-kernel-server python2.7-dev libmemcached-dev "
                  "zlib1g-dev libssl-dev build-essential dovecot-common "
                  "opendkim opendkim-tools postfix libtiff4-dev libjpeg8-dev "
                  "libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev "
                  "tk8.5-dev python-tk cmake")

env.hosts = ['main-server']
env.use_ssh_config = True

@hosts('main-server',)
def config_filesystem():
    if not sudo("getent group django"):
        sudo("groupadd django")
    if not sudo("getent passwd django"):
        sudo("useradd -g django django")
    if not files.exists("/webserver"):
        sudo("mkdir /webserver")
        sudo("chown django:django /webserver")
    if not files.exists("/email"):
        sudo("mkdir /email")
        sudo("chown django:django /email")
    if not files.exists("/export"):
        sudo("mkdir -p /export/{webserver,email}")
        sudo("chown django:django /export /export/webserver /export/email")
    prepare_webdir()
    sudo("ln -fs /webserver/conf/fstab /etc/fstab")
    sudo("mount -a")
    sudo("ln -fs /webserver/conf/exports /etc/exports")
    sudo("service nfs-kernel-server restart")


def install_packages():
    sudo("apt-get update")
    sudo("apt-get install %s" % system_packages)
    sudo("pip install -r /webserver/requirements.txt")


def prepare_webdir():
    with cd("/webserver"):
        sudo("git clone https://github.com/moiseshiraldo/inviMarket.git .",
             user="django")


@hosts('main-server',)
def pull_webfiles():
    with cd("/webserver"):
        sudo("git pull origin master", user="django")
    sudo("python /webserver/manage.py migrate")
    sudo("python /webserver/manage.py collectstatic")
    sudo("service apache2 restart")


def config_apache():
    sudo("ln -fs /webserver/conf/apache/invimarket "
         "/etc/apache2/sites-available/invimarket.conf")
    sudo("a2ensite invimarket")
    sudo("a2enmod rewrite")
    sudo("service apache2 restart")


@hosts('main-server',)
def install_postsrsd():
    run("git clone https://github.com/roehling/postsrsd.git")
    with cd("~/postsrsd"):
        run("make")
        sudo("make install")
    sudo("rm -rf ~/postsrsd/")
    sudo("service postsrsd start")


@hosts('main-server',)
def config_postfix():
    with cd("/webserver/conf/postfix"):
        sudo("cp -f main.cf /etc/postfix/main.cf")
        sudo("cp -f master.cf /etc/postfix/master.cf")
        sudo("cp -f access.cf /etc/postfix/access.cf")
        sudo("cp -f virtual_forwards.cf /etc/postfix/virtual_forwards.cf")
        sudo("cp -f virtual_maildir.cf /etc/postfix/virtual_maildir.cf")
        sudo("cp -f invimarket.rules /etc/postfix/invimarket.rules")
        sudo("cp -f sasl_access /etc/postfix/sasl_access")
        sudo("cp -f controlled_envelope_senders "
             "/etc/postfix/controlled_envelope_senders")
        sudo("postmap /etc/postfix/invimarket.rules")
        sudo("postmap /etc/postfix/sasl_access")
        sudo("postmap /etc/postfix/controlled_envelope_senders")
        sudo("service opendkim.conf restart")
        sudo("service postfix restart")


@hosts('main-server',)
def config_opendkim(key):
    put(key, "/etc/postfix/", use_sudo=True)
    sudo("chown root:root /etc/postfix/dkim.key")
    sudo("chmod 600 /etc/postfix/dkim.key")
    sudo("ln -fs /webserver/conf/postfix/opendkim.conf /etc/opendkim.conf")
    sudo("ln -fs /webserver/conf/postfix/dkimTrustedHosts "
         "/etc/postfix/dkimTrustedHosts")
    sudo("service postfix reload")
    sudo("service opendkim restart")


@hosts('main-server',)
def config_dovecot():
    with cd("/webserver/conf/dovecot"):
        sudo("cp -f 10-auth.conf /etc/dovecot/conf.d/10-auth.conf")
        sudo("cp -f 10-master.conf /etc/dovecot/conf.d/10-master.conf")
    sudo("service dovecot restart")


@hosts('main-server',)
def add_dovecot_user(user, password):
    sudo("echo -n %s: > /etc/dovecot/users" % user)
    sudo("doveadm pw -s CRYPT -p %s -u %s >> "
         "/etc/dovecot/users" % (user, password))
    sudo("chown dovecot:dovecot /etc/dovecot/users")


@hosts('main-server',)
def add_cronjobs():
    sudo("crontab -u django /webserver/conf/crontab")