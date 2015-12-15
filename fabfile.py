# -*- coding: utf-8 -*-

import os
import sys

from fabric.colors import blue, cyan, green, magenta, red, yellow
from fabric.decorators import task
from fabric.operations import local
from fabric.state import env
from fabric.utils import puts


env.version = '0.6'


# ============
# =  Hello   =
# ============
@task(default=True, alias='别名测试')
def hello():
    puts('*' * 50)
    puts(cyan('  Fabric 使用指南\n'))
    puts(green('  查看所有命令: fab -l'))
    puts(green('  查看命令: fab -d 命令'))
    puts(yellow('  带参数命令请输入: fab 命令:参数'))
    puts('*' * 50)


@task
def setup(proxy=True):
    """初始化工具包"""
    puts(green('配置 Homebrew'))
    if not os.path.exists('/usr/local/bin/brew'):
        local('ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
    puts(green('配置 代理'))
    local('brew install proxychains-ng')
    local('sed -i "" "s/socks4 	127.0.0.1 9050/socks5 	127.0.0.1 1080/g" /usr/local/Cellar/proxychains-ng/4.10/etc/proxychains.conf')
    local_proxy('brew install bash-completion go python3 ruby mysql memcached libmemcached redis gettext tree', proxy)
    puts(green('配置 RubyGems'))
    local('gem sources --remove https://rubygems.org/')
    local('gem sources -a https://ruby.taobao.org/')
    local('gem sources -l')
    puts(green('安装 CocoaPods'))
    local('sudo gem install cocoapods')
    puts(green('安装 virtualenvwrapper'))
    local('sudo pip3 install virtualenvwrapper -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com')
    puts(green('配置 .bash_profile'))
    local('curl -fsSL https://raw.githubusercontent.com/nypisces/Free/master/bash_profile > ~/.bash_profile')
    update()


@task
def update(proxy=True):
    """更新工具包"""
    puts(green('更新自己 当前版本 {} 更新在下次执行时生效'.format(env.version)))
    local('curl --compressed -fsSL https://raw.githubusercontent.com/nypisces/Free/master/fabfile.py > ~/fabfile.py')
    puts(green('更新 Homebrew'))
    local_proxy('brew update', proxy)
    local_proxy('brew upgrade', proxy)
    local('brew cleanup')
    puts(green('更新 RubyGems'))
    local('sudo gem update --system')
    local('sudo gem update')
    local('sudo gem clean')


@task
def update_pip(pip='pip3', source=' -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com'):
    local('{0} freeze --local | cut -d = -f 1 | grep -v "^\(bonjour\|pyOpenSSL\|pyobjc-framework-Message\|pyobjc-framework-ServerNotification\|xattr\)" | sudo xargs {0} install -U{1}'.format(pip, source))


def local_proxy(command, proxy):
    local('{}{}'.format('proxychains4 ' if proxy else '', proxy))


def get_function_name():
    return sys._getframe(1).f_code.co_name  # _getframe()则是自己的名字
