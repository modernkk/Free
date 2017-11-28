# -*- coding: utf-8 -*-

import os
import sys

from fabric.colors import blue, cyan, green, magenta, red, yellow
from fabric.decorators import task
from fabric.operations import local
from fabric.state import env
from fabric.utils import puts


env.version = '0.13'
env.pypi_option = ' -i https://mirrors.aliyun.com/pypi/simple/'  # 如果是 http 地址，加 --trusted-host mirrors.aliyun.com


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
def install(role=None, proxy=True, pypi_option=env.pypi_option):
    """初始化工具包, 例如 fab install:ios"""
    if not role:
        role = raw_input('请输入角色(all, android, ios, macos, python, wiki): ')
    if not os.path.exists('/usr/local/bin/brew'):
        puts(green('安装 Homebrew'))
        local('ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
    puts(green('配置 代理'))
    local('brew install proxychains-ng')
    local('sed -i "" "s/socks4[[:space:]][[:space:]]127.0.0.1[[:space:]]9050/socks5  127.0.0.1 1086/g" /usr/local/etc/proxychains.conf')
    local('brew install bash-completion ruby tree')
    local('brew link --overwrite ruby')
    puts(green('配置 RubyGems'))
    local('gem sources --add https://gems.ruby-china.org/ --remove https://rubygems.org/')
    local('gem sources -l')
    puts(green('安装 BearyChat, GitHub Desktop, Google Chrome, ShadowsocksX-NG'))
    local('brew cask install bearychat github google-chrome shadowsocksx-ng')
    puts(green('安装 Atom, Charles, Dash'))
    local('brew cask install atom charles dash')
    if role.lower() in ['all', 'wiki']:
        puts(green('安装 gollum'))  # https://github.com/gollum/gollum/wiki/Installation
        local('brew install icu4c')
        local('sudo gem install charlock_holmes -- --with-icu-dir=/usr/local/opt/icu4c')
        local('sudo gem install gollum')
    if role.lower() in ['all', 'mobile', 'ios', 'macos']:
        puts(green('安装 CocoaPods'))
        local('sudo gem install cocoapods')
        puts(green('安装 Carthage, SwiftFormat, SwiftLint'))
        local('brew install carthage swiftformat swiftlint')
    if role.lower() in ['all', 'mobile', 'android']:
        puts(green('安装 Java, Android Studio'))
        local('brew cask install java android-studio')
    if role.lower() in ['all', 'mobile', 'android', 'ios', 'macos']:
        puts(green('安装 fastlane'))
        local('sudo gem install fastlane -NV')  # gem方式 官方文档有参数 -NV, brew方式被墙且无法更新
    if role.lower() in ['all', 'dj', 'django', 'py', 'python']:
        local('brew install python3 mysql memcached libmemcached redis gettext')
        puts(green('安装 Pylint, Transifex Command-Line Tool, twine, virtualenvwrapper'))  # 上传到pypi需要twine
        local('sudo -H pip3 install pylint transifex-client twine virtualenvwrapper{}'.format(pypi_option))
        puts(green('安装 Java, Eclipse IDE for Java EE, MySQL Workbench'))
        local('brew cask install java eclipse-jee mysqlworkbench')
    local('brew cleanup')
    local('brew cask cleanup')
    local('sudo gem clean')
    puts(green('配置 .bash_profile'))
    curl('https://raw.githubusercontent.com/nypisces/Free/master/bash_profile > ~/.bash_profile')


@task
def update(proxy=True, pypi_option=env.pypi_option):
    """更新工具包"""
    puts(green('更新自己 当前版本 {} 更新在下次执行时生效'.format(env.version)))
    curl('https://raw.githubusercontent.com/nypisces/Free/master/fabfile.py > ~/fabfile.py')
    puts(green('更新 bash_profile'))
    curl('https://raw.githubusercontent.com/nypisces/Free/master/bash_profile > ~/.bash_profile')
    puts(green('更新 Homebrew'))
    local('brew upgrade')
    local('brew cleanup')
    puts(green('更新 pip, Pylint, Transifex Command-Line Tool, virtualenvwrapper, twine, Fabric'))  # https://github.com/Homebrew/legacy-homebrew/issues/25752
    try:
        local('sudo -H pip3 install -U pip pylint transifex-client twine virtualenvwrapper{}'.format(pypi_option))
    except Exception:
        pass
    local('sudo -H pip2 install -U pip{}'.format(pypi_option))
    local('sudo -H pip install -U Fabric{}'.format(pypi_option))  # https://github.com/pypa/pip/issues/3165
    puts(green('更新 RubyGems'))
    local('sudo gem update')
    local('sudo gem clean')
    puts(green('更新完毕\n如果更新了python3, 需要重新创建虚拟环境\n如果更新了ruby, 可能需要 brew link --overwrite ruby'))


@task
def update_pip(pip='pip3', pypi_option=env.pypi_option):
    local('{0} freeze --local | cut -d = -f 1 | grep -v "^\(bonjour\|pyOpenSSL\|pyobjc-framework-Message\|pyobjc-framework-ServerNotification\|xattr\)" | sudo xargs {0} install -U{1}'.format(pip, pypi_option))


def curl(command=''):
    local('curl -fsSL -x 127.0.0.1:1087 {}'.format(command))


def local_proxy(command, proxy):
    local('{}{}'.format('proxychains4 ' if proxy else '', command))


def get_function_name():
    return sys._getframe(1).f_code.co_name  # _getframe()则是自己的名字
