#!/bin/bash
# This script assumes that the submodules have already been init-ed
# Update each submodule to the remote-branch specified in .gitmodules
git submodule update --remote
# Also update some nested submodules
SUBMODULE_DIR=../lib/pico-sdk
if [[ -d $SUBMODULE_DIR ]] && [[ -f $SUBMODULE_DIR/.gitmodules ]]; then
  SUB_SUBMODULES_DIR=$SUBMODULE_DIR/lib
  # This is necessary because otherwise things get very confused if a nested submodule gets deleted
  if [[ -d $SUB_SUBMODULES_DIR ]]; then
    rm -rf $SUB_SUBMODULES_DIR
    git -C $SUBMODULE_DIR checkout -- lib
  fi
  git -C $SUBMODULE_DIR submodule update --init
fi