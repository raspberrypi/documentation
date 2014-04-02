# .bashrc and .bash_aliases

In your home folder, you will find a hidden file called `.bashrc` which contains some user configuration. You can edit this file to suit your needs.

Some useful adaptions are provided for you; some of these are commented out by default.

For example, some `ls` aliases:

```
alias ls='ls --color=auto'
#alias dir='dir --color=auto'
#alias vdir='vdir --color=auto'

alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
```
Aliases like these are provided to help users of other systems like Microsoft Windows (`dir` is the `ls` of DOS/Windows). Others are to add colour to the output of commands like `ls` and `grep` by default.

More variations of `ls` are also provided:

```
# some more ls aliases
#alias ll='ls -l'
#alias la='ls -A'
#alias l='ls -CF'
```

Ubuntu users may be familar with these as they are provided by default on that distribution. Uncomment these lines to have access to these aliases in future.

The lines starting with a `#` are commented out. To enable them, remove the `#` and they will be active next time you boot your Pi.

There is also reference to a `.bash_aliases` file which does not exist by default:

```
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi
```

The `if` statement here checks the file exists before including it.

Then you just create the file `.bash_aliases` and add more aliases like so:

```
alias gs='git status'
```

You can add other things directly to this file or to another, and include the file like the `.bash_aliases` example above.
