# colors for dark terminal themes
export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagaced

# Bash Completion for Fabric
function _fab_complete() {
    local cur
    if [[ -f "fabfile.py" || -d "fabfile" ]]; then
        cur="${COMP_WORDS[COMP_CWORD]}"
        COMPREPLY=( $(compgen -W "$(fab -F short -l)" -- ${cur}) )
        return 0
    else
        return 1
    fi
}

if [ -f /usr/local/etc/profile.d/bash_completion.sh ]; then
    . /usr/local/etc/profile.d/bash_completion.sh
    complete -o nospace -F _fab_complete fab
fi

# Homebrew
export PATH="/usr/local/sbin:$PATH"

# Ruby
export PATH="/usr/local/opt/ruby/bin:$PATH"
export PATH="/usr/local/lib/ruby/gems/2.5.0/bin:$PATH"

# virtualenvwrapper
export WORKON_HOME=~/Envs
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
