# -*- coding: utf-8 -*-

import os
import sys

from fabric.colors import blue, cyan, green, magenta, red, yellow
from fabric.decorators import task
from fabric.operations import local
from fabric.state import env
from fabric.utils import puts


env.version = '0.9.0'


# ============
# =  Hello   =
# ============
@task(default=True, alias='别名测试')
def hello():
    puts('*' * 60)
    puts('*  ' + cyan('  Fabric 使用指南  '.center(58, '=')) + '  *')
    puts('*' + ' ' * 58 + '*')
    puts('*' + green('  查看所有命令: fab -l'.ljust(64)) + '*')
    puts('*' + green('  查看命令: fab -d 命令'.ljust(64)) + '*')
    puts('*' + yellow('  带参数命令请输入: fab 命令:参数'.ljust(70)) + '*')
    puts('*' + ' ' * 58 + '*')
    puts('*' * 60)


@task
def setup(role='', proxy=True):
    """初始化工具包"""
    if not os.path.exists('/usr/local/bin/brew'):
        puts(green('安装 Homebrew'))
        local('ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
    puts(green('配置 代理'))
    local('brew install proxychains-ng')
    local('sed -i "" "s/socks4[[:space:]][[:space:]]127.0.0.1[[:space:]]9050/socks5  127.0.0.1 1086/g" /usr/local/Cellar/proxychains-ng/4.11/etc/proxychains.conf')
    local_proxy('brew install bash-completion ruby tree', proxy)
    puts(green('配置 RubyGems'))
    local('gem sources --add https://gems.ruby-china.org/ --remove https://rubygems.org/')
    local('gem sources -l')
    if role.lower() in ['all', 'wiki']:
        local_proxy('brew install icu4c', proxy)
        local('sudo gem install gollum')
        local('sudo gem clean')
    if role.lower() in ['all', 'ios', 'osx']:
        puts(green('安装 Alcatraz'))
        local('curl -fsSL https://raw.githubusercontent.com/supermarin/Alcatraz/deploy/Scripts/install.sh | sh')
        puts(green('安装 CocoaPods, shenzhen'))
        local('sudo gem install cocoapods shenzhen')
        local('sudo gem clean')
        puts(green('安装 SwiftLint'))
        local_proxy('brew install swiftlint', proxy)
    if role.lower() in ['all', 'dj', 'django', 'py', 'python']:
        local_proxy('brew install go python3 mysql memcached libmemcached redis gettext', proxy)
        puts(green('安装 virtualenvwrapper'))
        local('sudo pip3 install virtualenvwrapper -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com')
    puts(green('配置 .bash_profile'))
    local('curl -fsSL https://raw.githubusercontent.com/nypisces/Free/master/bash_profile > ~/.bash_profile')
    local('brew cleanup')


@task
def update(proxy=True):
    """更新工具包"""
    puts(green('更新自己 当前版本 {} 更新在下次执行时生效'.format(env.version)))
    local('curl -fsSL https://raw.githubusercontent.com/nypisces/Free/master/fabfile.py > ~/fabfile.py')
    local('sed -i "" "s/socks4[[:space:]][[:space:]]127.0.0.1[[:space:]]9050/socks5  127.0.0.1 1086/g" /usr/local/Cellar/proxychains-ng/4.11/etc/proxychains.conf')
    puts(green('更新 bash_profile'))
    local('curl -fsSL https://raw.githubusercontent.com/nypisces/Free/master/bash_profile > ~/.bash_profile')
    puts(green('更新 Homebrew'))
    local_proxy('brew update', proxy)
    local_proxy('brew upgrade', proxy)
    local('brew cleanup')
    puts(green('更新 RubyGems'))
    local('sudo gem update')
    local('sudo gem clean')


@task
def update_pip(pip='pip3', source=' -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com'):
    local('{0} freeze --local | cut -d = -f 1 | grep -v "^\(bonjour\|pyOpenSSL\|pyobjc-framework-Message\|pyobjc-framework-ServerNotification\|xattr\)" | sudo xargs {0} install -U{1}'.format(pip, source))


def local_proxy(command, proxy):
    local('{}{}'.format('proxychains4 ' if proxy else '', command))


def get_function_name():
    return sys._getframe(1).f_code.co_name  # _getframe()则是自己的名字
