"""

3 Steps to Commit your changes
Suppose you have created a new branch on GitHub with the name feature-branch.

enter image description here

FETCH
    git pull <remote_name> <branch_name> #use this
    git pull --all         Pull all remote branches
    git branch -a          List all branches now
Checkout and switch to the feature-branch directory. You can simply copy the branch name from the output of branch -a command above

git checkout -b feature-branch

VALIDATE

Next use the git branch command to see the current branch. It will show feature-branch with * In front of it

git branch   check current branch
git status   check the state of your codebase       
COMMIT

git add .   add all untracked files
git commit -m "Rafactore code or use your message"
Take update and the push changes on the origin server

 git pull origin feature-branch
 git push origin feature-branch
OR you can rebase with the master before commit

git fetch
git rebase origin/master
git push origin feature-branch

"""
