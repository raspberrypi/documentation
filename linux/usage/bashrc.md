# .bashrc and .bash_aliases

In your home folder you will find a hidden file called `.bashrc` which contains some user configuration options. You can edit this file to suit your needs. Changes made in this file will be actioned the next time a terminal is opened, since that is when the `.bashrc` file is read.

If you want your changes to take place in your current terminal, you can use either `source ~/.bashrc` or `exec bash`. These actually do slightly different things: the former simply re-executes the `.bashrc` file, which may result in undesirable changes to things like the path, the latter replaces the current shell with a new bash shell, which resets the shell back to the state at login, throwing away any shell variables you may have set. Choose whichever is most appropriate.

Some useful adaptions are provided for you; some of these are commented out with a `#` by default. To enable them, remove the `#` and they will be active next time you boot your Pi or start a new terminal.

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

Ubuntu users may be familiar with these as they are provided by default on that distribution. Uncomment these lines to have access to these aliases in future.

`.bashrc` also contains a reference to a `.bash_aliases` file, which does not exist by default. You can add it to provide a handy way of keeping all your aliases in a separate file.

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

You can add other things directly to this file, or to another and include that file like the `.bash_aliases` example above.
