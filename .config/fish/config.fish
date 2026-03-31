alias ls='eza -1 --color=always --icons=always --hyperlink --group-directories-first'
alias cat='bat'
alias rm='rm -i'
alias mkdir='mkdir -p'
alias cd='z'

if status is-interactive
    set -g fish_greeting
    fastfetch --logo-recache true
    stty -icanon -echo
    dd bs=1 count=1 >/dev/null 2>&1
    stty icanon echo
    zoxide init fish | source
    direnv hook fish | source

    function nvim
        kitty --title=["nvim"] -e nvim $argv > /dev/null 2>&1 & disown
    end
    
    function open
        command xdg-open $argv >/dev/null 2>&1 & disown
    end

    function auto_activate_venv --on-variable PWD
        if test -f .venv/bin/activate.fish
            if not set -q VIRTUAL_ENV
                source .venv/bin/activate.fish
            end
        else if set -q VIRTUAL_ENV
            deactivate
        end
    end
end

function fish_command_not_found
    if type -q yay
        echo "Command '$argv[1]' not found. Searching in packages..."
        pacman -F $argv[1]
    else
        echo "Command '$argv[1]' not found and 'yay' is not installed."
    end
end

if test -f /opt/miniconda3/etc/fish/conf.d/conda.fish
    source /opt/miniconda3/etc/fish/conf.d/conda.fish
end
