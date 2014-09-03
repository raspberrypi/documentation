# Sonic Pi

Sonic Pi is an open source programming environment designed to explore and teach programming concepts through the process of creating sounds and making music.

The code you write in Sonic Pi is based on Ruby, which is really nice and clean. This means you can write a lot without worrying too much about syntax, braces and brackets - though they are important for more complex programs.

## Getting started

You'll find Sonic Pi on Raspbian in the applications menu under **Education**. Open it up and you'll see a window like this:

![Sonic Pi interface](images/sonic-pi.png)

This is the Sonic Pi application interface. It has three sections to the window. The largest one is for writing your code and we call it the Programming Panel. The top right hand window is the Output Panel and it displays information about your program as it runs. Underneath is the third window: the Error Panel which displays information if there is a problem with your code.

## Making sounds

In **Workspace 1**, type:

```ruby
play 60
```

Now click the Play icon and the note should play. MIDI Note value 60 is a C.

Try changing `play 60` to `pley 60` to see what an error looks like.

Now type the code:

```ruby
play 60
play 67
play 69
```

and hit the Play button again.

The notes are being played immediately so they are effectively played at the same time. To add a pause between notes, use `sleep`:

```ruby
play 60
sleep 1
play 67
sleep 2
play 69
```

## A Tune: Frère Jacques

The song *Frère Jacques* begins with:

`C D E C` or `60 62 64 60` 	in MIDI notes.

### Music Notes to MIDI Note Values

| C       | D      | E     | F     | G     | A     | B     |
| :-----: |:------:|:-----:|:-----:|:-----:|:-----:|:-----:|
| 60      | 62     | 64    | 65    | 67    | 69    | 71    |

Here is the tune:

```ruby
play 60
sleep 0.5
play 62
sleep 0.5
play 64
sleep 0.5
play 60
sleep 0.5
```

## Looping

In order to repeat a set of instructions, you can use a loop. In Ruby this is simple:

```ruby
2.times do
  play 60
  sleep 0.5
  play 62
  sleep 0.5
  play 64
  sleep 0.5
  play 60
  sleep 0.5
end
```

## Functions

You can define a set of instructions in a function, and then call the function multiple times instead of copy and pasting lines of code:

```ruby
def frere
  play 60
  sleep 0.5
  play 62
  sleep 0.5
  play 64
  sleep 0.5
  play 60
  sleep 0.5
end
```
Then call the function by typing `frere`. For example in a loop:

```ruby
4.times do
  frere
end
```

## Synths

Synths are different effects the `play` function uses to make sounds. The default synth is called `"pretty_bell"` but alternatives are available:

```ruby
"pretty_bell"
"dull_bell"
"beep"
"saw_beep"
"fm"
```

Try a different synth:

```ruby
with_synth "fm"
2.times do
  play 60
  sleep 0.5
  play 62
  sleep 0.5
end
```

## Threads

You can play two tunes at the same time using threads. Like loops, they are blocks encasing lines with the `end` keyword:

```ruby
in_thread do
  with_synth "saw_beep"
  2.times do
    play 60
    sleep 0.5
    play 67
    sleep 0.5
  end
end
```

## Workspaces

You have multiple workspaces available in the Sonic Pi application window. This means you can try out code blocks in other workspaces without deleting your other code. You are encouraged to use the other workspaces to try things out, experiment and sandbox!

## Sonic Pi files

If you choose to save a file, you can return to it later or share it with others. Sonic Pi files are simple text files so you can view and edit them on other computers and play them on other Raspberry Pis.
