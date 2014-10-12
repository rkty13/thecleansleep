#!/bin/bash
git pull heroku master
echo The following changes above have been pulled, y to push
read PULL
git add --all
echo Please enter a comment:
read COMMENT
git commit -m $COMMENT
git push heroku master