import os

from colorama import Fore, init
from fabric2 import task
from fabric2.util import get_local_user
from invoke import env

env.version = '0.7.3'
env.colorize_errors = True
env.proxy = '127.0.0.1:1087'
# env.pypi_mirror = ' -i https://mirrors.aliyun.com/pypi/simple/'  # 如果是 http 地址，加 --trusted-host mirrors.aliyun.com
env.pypi_mirror = ' -i https://pypi.douban.com/simple/'


#########
# Hello #
#########
@task(default=True, aliases=['别名测试', '别名二'])
def hello(c, path='参数值'):
    """Hello"""
    init(autoreset=True)
    print('*' * 60)
    print('*  ' + Fore.CYAN + '  Fabric 使用指南  '.center(58, '=') + '  *')
    print('*' + ' ' * 58 + '*')
    print('*' + Fore.GREEN + '  查看所有命令: fab -l'.ljust(64) + '*')
    print('*' + Fore.GREEN + '      查看命令: fab -d 命令'.ljust(64) + '*')
    print('*' + Fore.YELLOW + '  带参数命令请输入: fab2 命令 --参数 {}'.format(path) + '*')
    print('*' + Fore.MAGENTA + '    带参数命令: fab 命令:参数'.ljust(67) + '*')
    print('*' + Fore.BLUE + '  info' + Fore.RED + ' error ' + Fore.YELLOW + 'warning' + ' ' * 38 + '*')
    print('*' + Fore.GREEN + '  Hello ~  ' + get_local_user() + '*')
    print('*' + ' ' * 58 + '*')
    print('*' * 60)


@task(hosts=['local'])
def install(c, pypi_mirror=env.pypi_mirror):
    """初始化工具包"""
    init(autoreset=True)
    role = input('请输入角色 [all, android, ios, macos, node, python, django, wiki, jekyll]: ')
    confirm = input('是否使用 brew cask 安装 常用软件 (速度较慢) ? [y/N]: ')
    is_cask = confirm.lower() in ['ok', 'y', 'yes']
    confirm = input('是否使用本地代理 {}? [y/N]: '.format(env.proxy))
    is_proxy = confirm.lower() in ['ok', 'y', 'yes']
    print(Fore.GREEN + '安装 Fabric ( 修正 six, 以免以后执行 fab update 报错 ), isort, requests')  # https://github.com/pypa/pip/issues/3165
    # c.local('sudo -H pip2 install -U Fabric==1.14{} --ignore-installed six'.format(pypi_mirror))
    c.local('sudo -H pip install fabric isort requests{}'.format(pypi_mirror))
    if not os.path.exists('/usr/local/bin/brew'):
        print(Fore.GREEN + '安装 Homebrew')
        c.local('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
    print(Fore.GREEN + '安装 bash-completion, Tree')
    c.local('brew install bash-completion tree')
    print(Fore.GREEN + '安装 Ruby, 配置 RubyGems')
    c.local('brew install ruby')  # 系统原版某些gem安装不上
    c.local('brew link --overwrite ruby')
    c.local('gem sources --add https://gems.ruby-china.com/ --remove https://rubygems.org/')
    c.local('sudo gem update --system')
    print(Fore.GREEN + '{} GitHub Desktop, Google Chrome, Visual Studio Code'.format('安装' if is_cask else '跳过'))
    if is_cask:
        c.local('brew cask install github google-chrome visual-studio-code')
    print(Fore.GREEN + '{} BearyChat, Charles, Dash, Postman'.format('安装' if is_cask else '跳过'))
    if is_cask:
        c.local('brew cask install bearychat charles dash postman')
    if role.lower() in ['wiki']:
        print(Fore.GREEN + '安装 gollum')  # https://github.com/gollum/gollum/wiki/Installation
        c.local('brew install icu4c')
        c.local('sudo gem install charlock_holmes -- --with-icu-dir=/usr/local/opt/icu4c')
        c.local('sudo gem install gollum')
    if role.lower() in ['jekyll']:
        print(Fore.GREEN + '安装 Jekyll - 附带安装 Bundler')
        c.local('sudo gem install bundler jekyll')  # https://jekyllrb.com
    if role.lower() in ['all', 'android', 'django']:
        print(Fore.GREEN + '安装 Java')
        c.local('brew cask install java')
    if role.lower() in ['all', 'mobile', 'ios', 'macos']:
        print(Fore.GREEN + '安装 CocoaPods')
        c.local('sudo gem install cocoapods')
        print(Fore.GREEN + '安装 Carthage, SwiftFormat, SwiftLint')
        c.local('brew install carthage swiftformat swiftlint')
    if role.lower() in ['all', 'mobile', 'android']:
        print(Fore.GREEN + '安装 Android Studio')
        c.local('brew cask install android-studio')
    if role.lower() in ['all', 'mobile', 'android', 'ios', 'macos']:
        print(Fore.GREEN + '安装 fastlane')
        c.local('sudo gem install fastlane -NV')  # gem方式 官方文档有参数 -NV, brew方式被墙且无法更新
    if role.lower() in ['all', 'node']:
        print(Fore.GREEN + '安装 Node.js')
        c.local('brew install node')
        print(Fore.GREEN + '全局安装 BrowserSync, gulp')
        c.local('npm install -g browser-sync gulp-cli gulp')
    if role.lower() in ['all', 'python', 'django']:
        print(Fore.GREEN + '安装 Python')
        c.local('brew install python')
        print(Fore.GREEN + '安装 Pylint, Flake8, YAPF, twine, virtualenvwrapper')  # 上传到pypi需要twine
        c.local('sudo -H pip install pylint flake8 yapf twine virtualenvwrapper{}'.format(pypi_mirror))
    if role.lower() in ['all', 'django']:
        print(Fore.GREEN + '安装 MySQL, Redis, gettext')
        c.local('brew install mysql redis gettext')
        print(Fore.GREEN + '安装 Transifex Command-Line Tool')
        c.local('sudo -H pip install transifex-client{}'.format(pypi_mirror))
        print(Fore.GREEN + '{} Docker, MySQL Workbench'.format('安装' if is_cask else '跳过'))
        if is_cask:
            c.local('brew cask install docker mysqlworkbench')
    c.local('brew cleanup')
    c.local('sudo gem clean')
    print(Fore.GREEN + '配置 .bash_profile')
    curl('-o .bash_profile https://raw.githubusercontent.com/nyssance/Free/master/bash_profile', is_proxy)


@task(hosts=['local'])
def update(c, is_proxy=True, pypi_mirror=env.pypi_mirror):
    """更新工具包"""
    init(autoreset=True)
    print(Fore.CYAN + '更新自己 当前版本 {} 更新在下次执行时生效'.format(env.version))
    curl('-O https://raw.githubusercontent.com/nyssance/Free/master/fabfile.py', is_proxy)
    print(Fore.CYAN + '更新 bash_profile')
    curl('-o .bash_profile https://raw.githubusercontent.com/nyssance/Free/master/bash_profile', is_proxy)
    print(Fore.CYAN + '更新 Homebrew')
    c.local('brew upgrade')
    c.local('brew cleanup')
    print(Fore.CYAN + '检查 Homebrew 状态')
    c.local('brew services list')
    c.local('brew doctor')
    if os.path.exists('/usr/local/bin/node'):
        print(Fore.CYAN + '更新 npm')
        c.local('npm update -g')
    if os.path.exists('/usr/local/bin/python3'):
        print(Fore.CYAN + '更新 pip, Pylint, Flake8, YAPF, twine, virtualenvwrapper')
        c.local('sudo -H pip install -U --upgrade-strategy=eager pip pylint flake8 yapf twine virtualenvwrapper{}'.format(pypi_mirror))
        print(Fore.CYAN + '更新 Transifex Command-Line Tool')
        c.local('sudo -H pip install -U --upgrade-strategy=eager transifex-client{}'.format(pypi_mirror))
    print(Fore.CYAN + '更新 Fabric, isort, requests')
    # c.local('sudo -H pip2 install -U pip{}'.format(pypi_mirror))  # 更新pip2会引起python3 pip失效
    c.local('sudo -H pip install -U --upgrade-strategy=eager Fabric==1.14 isort requests{}'.format(pypi_mirror))
    print(Fore.CYAN + '更新 RubyGems')
    c.local('gem sources')
    c.local('sudo gem update --system')
    c.local('sudo gem update')
    c.local('sudo gem clean')
    c.local('brew cask outdated')
    print(Fore.CYAN + '更新完毕\n如果更新了python, 需要重新创建虚拟环境\n如果更新了ruby, 可能需要 brew link --overwrite ruby')


@task(hosts=['local'])
def clean(c):
    """清理"""
    local('brew prune')
    # -aIx 是删除所有, -n /usr/local/bin 是防止 OS X 上无权限
    # SO: https://stackoverflow.com/questions/8095209/uninstall-all-installed-gems-in-osx#8095234
    # SO: https://stackoverflow.com/questions/2893889/how-do-i-fix-the-you-dont-have-write-permissions-into-the-usr-bin-directory#34989655
    c.local('sudo gem uninstall -aIx -n /usr/local/bin')


def curl(c, command='', is_proxy=True):
    c.local('curl -fsSL{} {}'.format(' -x {}'.format(env.proxy) if is_proxy and env.proxy else '', command))
