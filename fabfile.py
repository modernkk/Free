# coding=utf-8

import os

from fabric.colors import blue, cyan, green, magenta, red, yellow
from fabric.decorators import task
from fabric.operations import local
from fabric.state import env
from fabric.utils import puts

env.version = '0.7.1'
env.colorize_errors = True
env.proxy = '127.0.0.1:1087'
# env.pypi_mirror = ' -i https://mirrors.aliyun.com/pypi/simple/'  # 如果是 http 地址，加 --trusted-host mirrors.aliyun.com
env.pypi_mirror = ' -i https://pypi.douban.com/simple/'

#########
# Hello #
#########
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
def install(role=None, pypi_mirror=env.pypi_mirror):
    """初始化工具包, 例如 fab install:ios"""
    role = raw_input('请输入角色 [all, android, ios, macos, node, python, django, wiki, jekyll]: ')
    confirm = raw_input('是否使用 brew cask 安装 常用软件 (速度较慢) ? [y/N]: ')
    is_cask = confirm.lower() in ['ok', 'y', 'yes']
    confirm = raw_input('是否使用本地代理 {}? [y/N]: '.format(env.proxy))
    is_proxy = confirm.lower() in ['ok', 'y', 'yes']
    puts(green('安装 Fabric ( 修正 six, 以免以后执行 fab update 报错 ), isort, requests'))  # https://github.com/pypa/pip/issues/3165
    local('sudo -H pip2 install -U Fabric==1.14{} --ignore-installed six'.format(pypi_mirror))
    local('sudo -H pip2 install isort requests{}'.format(pypi_mirror))
    if not os.path.exists('/usr/local/bin/brew'):
        puts(green('安装 Homebrew'))
        local('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
    puts(green('安装 bash-completion, Tree'))
    local('brew install bash-completion tree')
    puts(green('安装 Ruby, 配置 RubyGems'))
    local('brew install ruby')  # 系统原版某些gem安装不上
    local('brew link --overwrite ruby')
    local('gem sources --add https://gems.ruby-china.com/ --remove https://rubygems.org/')
    local('sudo gem update --system')
    puts(green('{} GitHub Desktop, Google Chrome, Visual Studio Code'.format('安装' if is_cask else '跳过')))
    if is_cask:
        local('brew cask install github google-chrome visual-studio-code')
    puts(green('{} BearyChat, Charles, Dash, Postman'.format('安装' if is_cask else '跳过')))
    if is_cask:
        local('brew cask install bearychat charles dash postman')
    if role.lower() in ['wiki']:
        puts(green('安装 gollum'))  # https://github.com/gollum/gollum/wiki/Installation
        local('brew install icu4c')
        local('sudo gem install charlock_holmes -- --with-icu-dir=/usr/local/opt/icu4c')
        local('sudo gem install gollum')
    if role.lower() in ['jekyll']:
        puts(green('安装 Jekyll - 附带安装 Bundler'))
        local('sudo gem install bundler jekyll')  # https://jekyllrb.com
    if role.lower() in ['all', 'android', 'django']:
        puts(green('安装 Java'))
        local('brew cask install java')
    if role.lower() in ['all', 'mobile', 'ios', 'macos']:
        puts(green('安装 CocoaPods'))
        local('sudo gem install cocoapods')
        puts(green('安装 Carthage, SwiftFormat, SwiftLint'))
        local('brew install carthage swiftformat swiftlint')
    if role.lower() in ['all', 'mobile', 'android']:
        puts(green('安装 Android Studio'))
        local('brew cask install android-studio')
    if role.lower() in ['all', 'mobile', 'android', 'ios', 'macos']:
        puts(green('安装 fastlane'))
        local('sudo gem install fastlane -NV')  # gem方式 官方文档有参数 -NV, brew方式被墙且无法更新
    if role.lower() in ['all', 'node']:
        puts(green('安装 Node.js'))
        local('brew install node')
        puts(green('全局安装 BrowserSync, gulp'))
        local('npm install -g browser-sync gulp-cli gulp')
    if role.lower() in ['all', 'python', 'django']:
        puts(green('安装 Python'))
        local('brew install python')
        puts(green('安装 Pylint, Flake8, YAPF, twine, virtualenvwrapper'))  # 上传到pypi需要twine
        local('sudo -H pip3 install pylint flake8 yapf twine virtualenvwrapper{}'.format(pypi_mirror))
    if role.lower() in ['all', 'django']:
        puts(green('安装 MySQL, Redis, gettext'))
        local('brew install mysql redis gettext')
        puts(green('安装 Transifex Command-Line Tool'))
        local('sudo -H pip3 install transifex-client{}'.format(pypi_mirror))
        puts(green('{} Docker, MySQL Workbench'.format('安装' if is_cask else '跳过')))
        if is_cask:
            local('brew cask install docker mysqlworkbench')
    local('brew cleanup')
    local('sudo gem clean')
    puts(green('配置 .bash_profile'))
    curl('-o .bash_profile https://raw.githubusercontent.com/nyssance/Free/master/bash_profile', is_proxy)


@task
def update(is_proxy=True, pypi_mirror=env.pypi_mirror):
    """更新工具包"""
    puts(cyan('更新自己 当前版本 {} 更新在下次执行时生效'.format(env.version)))
    curl('-O https://raw.githubusercontent.com/nyssance/Free/master/fabfile.py', is_proxy)
    puts(cyan('更新 bash_profile'))
    curl('-o .bash_profile https://raw.githubusercontent.com/nyssance/Free/master/bash_profile', is_proxy)
    puts(cyan('更新 Homebrew'))
    local('brew upgrade')
    local('brew cleanup')
    puts(cyan('检查 Homebrew 状态'))
    local('brew services list')
    local('brew doctor')
    if os.path.exists('/usr/local/bin/node'):
        puts(cyan('更新 npm'))
        local('npm update -g')
    if os.path.exists('/usr/local/bin/pip3'):
        puts(cyan('更新 pip, Pylint, Flake8, YAPF, twine, virtualenvwrapper'))
        local('sudo -H pip3 install -U --upgrade-strategy=eager pip pylint flake8 yapf twine virtualenvwrapper{}'.format(pypi_mirror))
        puts(cyan('更新 Transifex Command-Line Tool'))
        local('sudo -H pip3 install -U --upgrade-strategy=eager transifex-client{}'.format(pypi_mirror))
    puts(cyan('更新 Fabric, isort, requests'))
    # local('sudo -H pip2 install -U pip{}'.format(pypi_mirror))  # 更新pip2会引起pip3失效
    local('sudo -H pip2 install -U --upgrade-strategy=eager Fabric==1.14 isort requests{}'.format(pypi_mirror))
    puts(cyan('更新 RubyGems'))
    local('gem sources')
    local('sudo gem update --system')
    local('sudo gem update')
    local('sudo gem clean')
    local('brew cask outdated')
    puts(cyan('更新完毕\n如果更新了python, 需要重新创建虚拟环境\n如果更新了ruby, 可能需要 brew link --overwrite ruby'))


def curl(command='', is_proxy=True):
    local('curl -fsSL{} {}'.format(' -x {}'.format(env.proxy) if is_proxy and env.proxy else '', command))
