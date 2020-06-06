# Contributing to Raspberry Pi Documentation

The sources for all the Raspberry Pi documentation are stored online on a site called GitHub, located here:

https://github.com/raspberrypi/documentation

Although you won't be able to directly change documentation on the official repository, you can take a look at all the source files and see how everything is arranged. The sources files and folders follow the hierarchical documentation as found on the Raspberry Pi website.

Before making any changes, it is wise to find out whether your contribution is likely to be accepted by checking [here](https://www.raspberrypi.org/documentation/CONTRIBUTING.md).

In order to submit new or corrected documentation, you have to create a GitHub account (if you don't already have one) and **fork** the original repository to your account. You make changes as you see fit, save them in your repository, then make something called a **pull request** to the original Raspberry Pi repository. This pull request (**PR**) then appears in the Raspberry Pi repository where it can be assessed by the maintainers, copy edited, and, if appropriate, merged with the official repository.

The documentation which appears on the Raspberry Pi website is generated from the GitHub repository, and is updated approximately hourly.

You will need a GitHub account to perform any of the following operations. 

## Forking a repository

This is easy. Go to the Raspberry Pi repository, https://github.com/raspberrypi/documentation, and look at the top right of the page. There should be a button labelled **Fork**, which will fork a copy of the repository to your own GitHub account. 

## Make Changes

In your own copy of the repo, you can now alter or add files. The file format is GitHub Markdown, and for this reason new files should have the suffix `.md`. There is a description of GitHub Markdown [here](https://guides.github.com/features/mastering-markdown/).

To edit a file, first find the file in the filename tree, and click on it. This displays the page in fully rendered markup, and on the toolbar at the top of the document (not top of the page) is a small icon of a pencil. This is the edit button. Click on it and the file will appear in the Github editor. You can now edit away to your heart's content. You can click on **Preview changes** to see the fully rendered file with your edits.  

At the end of the page is a box called **Commit Changes**. You can either commit your changes directly to your own master branch or create a new branch for use as a pull request. Use the master option, as this means you are making changes to your master copy. Using the branch option will create a new branch in your own repository, but that's a little more complicated to deal with so it won't be described here. If you are making a lot of independent changes over time before pushing the changes to Raspberry Pi, you may wish to investigate the branch option. Update the commit title and enter a description of the change at this point. 

Selecting **Commit changes** will make the change to your master branch. You now need to take that change and make a pull request from it.

## Opening a Pull Request

This is pretty easy. Click on the **Pull Requests** tab on the toolbar. Afterwards, there should be a green button just below the toolbar that is labelled **New pull request**. Click it, and a page should appear that asks you to compare changes. This PR page is actually on the Raspberry Pi GitHub page, not the contributor's, because a PR requests the Raspberry Pi repository maintainers to 'pull' from the contributor's repository. The left-hand side should be the `raspberrypi/documentation` repository, and the branch should be the master one. The right-hand side is where the PR is coming from: your GitHub account, and your master branch. Further down the page you should see a list of the commits you want to have in the PR, and, below that, the actual changes. 

If you are happy for the PR to be created, click on **Create pull request**.

And that's it! The Raspberry Pi documentation PR list will now have your entry in it. It will be read, assessed for technical correctness, passed to copy editors for final checking, and finally merged to the main documentation tree.


This is a very quick guide to contributing via GitHub, but it will get you started and enable you to make a difference!

