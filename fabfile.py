# -*- coding: utf-8 -*-

import os

from fabric.colors import blue, cyan, green, magenta, red, yellow
from fabric.decorators import task
from fabric.operations import local
from fabric.state import env
from fabric.utils import puts

env.version = '0.28'
env.colorize_errors = True
env.proxy = '127.0.0.1:1087'
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
    puts('*' + green('      查看命令: fab -d 命令'.ljust(64)) + '*')
    puts('*' + magenta('    带参数命令: fab 命令:参数'.ljust(67)) + '*')
    puts('*' + blue('  info') + red(' error ') + yellow('warning') + ' ' * 38 + '*')
    puts('*' + ' ' * 58 + '*')
    puts('*' * 60)


@task
def install(role=None, pypi_option=env.pypi_option):
    """初始化工具包, 例如 fab install:ios"""
    if not role:
        role = raw_input('请输入角色(all, android, ios, macos, django, wiki): ')
    puts(cyan('安装requests, 修正six, 以免以后执行 fab update 报错'))  # https://github.com/pypa/pip/issues/3165
    local('sudo -H pip install requests{}'.format(pypi_option))
    local('sudo -H pip install -U Fabric{} --ignore-installed six'.format(pypi_option))
    if not os.path.exists('/usr/local/bin/brew'):
        puts(cyan('安装 Homebrew'))
        local('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
    puts(cyan('安装 bash-completion, Tree'))
    local('brew install bash-completion tree')
    puts(cyan('安装Ruby, 配置 RubyGems'))
    local('brew install ruby')  # 系统原版某些gem安装不上
    local('brew link --overwrite ruby')
    local('gem sources --add https://gems.ruby-china.org/ --remove https://rubygems.org/')
    local('sudo gem update --system')
    puts(cyan('安装 GitHub Desktop, Google Chrome, Visual Studio Code'))
    local('brew cask install github google-chrome, visual-studio-code')
    puts(cyan('安装 BearyChat, Charles, Dash, Postman'))
    local('brew cask install bearychat charles dash postman')
    if role.lower() in ['wiki']:
        puts(cyan('安装 gollum'))  # https://github.com/gollum/gollum/wiki/Installation
        local('brew install icu4c')
        local('sudo gem install charlock_holmes -- --with-icu-dir=/usr/local/opt/icu4c')
        local('sudo gem install gollum')
    if role.lower() in ['jekyll']:
        puts(cyan('安装 Jekyll, Bundler'))
        local('sudo gem install jekyll bundler')  # https://jekyllrb.com
    if role.lower() in ['all', 'android', 'django']:
        puts(cyan('安装 Java'))
        local('brew cask install java')
    if role.lower() in ['all', 'mobile', 'ios', 'macos']:
        puts(cyan('安装 CocoaPods'))
        local('sudo gem install cocoapods')
        puts(cyan('安装 Carthage, SwiftFormat, SwiftLint'))
        local('brew install carthage swiftformat swiftlint')
    if role.lower() in ['all', 'mobile', 'android']:
        puts(cyan('安装 Android Studio'))
        local('brew cask install android-studio')
    if role.lower() in ['all', 'mobile', 'android', 'ios', 'macos']:
        puts(cyan('安装 fastlane'))
        local('sudo gem install fastlane -NV')  # gem方式 官方文档有参数 -NV, brew方式被墙且无法更新
    if role.lower() in ['all', 'django']:
        puts(cyan('安装 Python 3, MySQL, Memcached, libMemcached, Redis, gettext'))
        local('brew install python3 mysql memcached libmemcached redis gettext')
        puts(cyan('安装 Pylint, Flake8, YAPF, Transifex Command-Line Tool, twine, virtualenvwrapper'))  # 上传到pypi需要twine
        local('sudo -H pip3 install pylint flake8 yapf transifex-client twine virtualenvwrapper{}'.format(pypi_option))
        puts(cyan('安装 MySQL Workbench'))
        local('brew cask install mysqlworkbench')
    local('brew cleanup')
    local('brew cask cleanup')
    local('sudo gem clean')
    puts(cyan('配置 .bash_profile'))
    curl('-o .bash_profile https://raw.githubusercontent.com/nyssance/Free/master/bash_profile')


@task
def update(pypi_option=env.pypi_option):
    """更新工具包"""
    puts(cyan('更新自己 当前版本 {} 更新在下次执行时生效'.format(env.version)))
    curl('-O https://raw.githubusercontent.com/nyssance/Free/master/fabfile.py')
    puts(cyan('更新 bash_profile'))
    curl('-o .bash_profile https://raw.githubusercontent.com/nyssance/Free/master/bash_profile')
    puts(cyan('更新 Homebrew'))
    local('brew upgrade')
    local('brew cleanup')
    if os.path.exists('/usr/local/bin/pip3'):
        puts(cyan('更新 pip, Pylint, Transifex Command-Line Tool, virtualenvwrapper, twine'))
        local('sudo -H pip3 install -U pip pylint transifex-client twine virtualenvwrapper{}'.format(pypi_option))
    puts(cyan('更新 Fabric, requests'))
    local('sudo -H pip2 install -U pip{}'.format(pypi_option))
    local('sudo -H pip install -U Fabric requests{}'.format(pypi_option))
    puts(cyan('更新 RubyGems'))
    local('sudo gem update --system')
    local('sudo gem update')
    local('sudo gem clean')
    local('brew cask outdated')
    puts(cyan('更新完毕\n如果更新了python3, 需要重新创建虚拟环境\n如果更新了ruby, 可能需要 brew link --overwrite ruby'))


@task
def update_pip(pip='pip3', pypi_option=env.pypi_option):
    local(
        '{0} freeze --local | cut -d = -f 1 | grep -v "^\(bonjour\|pyOpenSSL\|pyobjc-framework-Message\|pyobjc-framework-ServerNotification\|xattr\)" | sudo xargs {0} install -U{1}'.
        format(pip, pypi_option))


def curl(command=''):
    local('curl -fsSL{} {}'.format(' -x {}'.format(env.proxy) if env.proxy else '', command))
