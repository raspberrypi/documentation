# Contributing to Raspberry Pi Documentation

All the Raspberry Pi documentation is stored online, on a site called Github, using Github Markdown. It can be found at the following location.

https://github.com/raspberrypi/documentation

Although you won't be able to change documentation on the official repository you can take a look at all the source files and see how it is all arranged. But first, find out whether your contribution is likely to be accepted, by checking [here](https://www.raspberrypi.org/documentation/CONTRIBUTING.md)

The process of sending in new or corrected documentation requires you to create a github account, if you don't already have one, and `fork` the original repository. You then make changes as you see fit, save them in your repository, then make something called a pull request to the original Raspberry Pi repository. This `PR` appears in the Raspberry Pi repository where it can be assessed by the maintainers, copy edited, and merged with the official repository.

The actual documentation as it appears on the Raspberry Pi website is generated from the Github repository, and is updated approximately hourly.

You will need a github account to do any of the following operations. 

## Forking a repository

This is easy. Go to the Raspberry Pi repository, https://github.com/raspberrypi/documentation, and look at the top right of the page. There should be a button labelled `Fork`, which will fork a copy of the repository to your own Github account. 

## Make Changes

In your own copy of the repo you can now alter or add files. The file format is Github Markdown, and for this reason new files should have the suffix `.md`. There is a description of Github Markdown [here](https://guides.github.com/features/mastering-markdown/).

To edit a file, first find the file in the filename tree, and click on it. This displays the page in fully rendered markup, and on the toolbar at the top of the document (not top of the page) is a small icon of a pencil. This is the edit button. Click on it and the file will appear in the Github editor. You can now edit away to your hearts content. You can click on ```Preview changes``` to see the fully rendered file with your edits.  

At the end of the page is a box called Commit Changes. You can either commit your changes directly to your own master branch or create a new branch for use as a pull request. We are actually going to use the master option, this means you are making changes to your master copy. Using the branch option will create a new branch, but that's a little more complicated to deal with so won't be described here. However, if you are making a lot of independant changes over time before pushing the changes to Raspberry Pi, you may wish to investigate this option. You might want to update the commit title and enter a description at this point. 

Selecting `Commit changes` will make the change to your master branch. You now need to take that change and make a Pull request from it.

## Opening a Pull Request

This is pretty easy. Click on the `<> Code` tab on the toolbar. This takes you back to the files page. A button should be just above the  file tree that is labelled `New pull request`. Click on this. A page now appears that describes where the PR is to go (note that this PR page is actually on the Raspberry Pi github page, not the contributors, as you are pulling to the Raspberry Pi repository from the contributors repository). The left hand side should be the raspberrypi/documentation repository, and the branch should be master. The right hand side is where the PR is coming from, your github account, and your master branch. Further down the page are a list of the commits you are wanting to have the in PR, and below that the actual changes. 

if you are happy for the PR to be created, click on `Create pull request`.

And that is it!


Of course, this is a very quick guide to contributing via Github, but it should get you going well enough to make a difference!







