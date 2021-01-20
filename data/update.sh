#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

sourceRepo=${1}
targetFolder=${2}

# If the repo with the "database" is not present, clone it from github, otherwise do a git pull
if [ -d ${targetFolder} ]; then
  echo "Repo is already cloned. Getting latest version..."
  cd ${targetFolder}
  git pull
else
  echo "Repo is not cloned."
  git clone ${sourceRepo} ${targetFolder}
fi
