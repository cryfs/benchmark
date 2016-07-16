#!/bin/bash
# This is a simple script measuring performance for handling one large file (reading from it, writing to it, deleting it).
# It is independent from other performance scripts in this repository.

set -ev

CRYFS=cryfs
export CRYFS_FRONTEND=noninteractive
DD_PARAMS="bs=10M count=400"
ROOTDIR=/mnt
BASEDIR=${ROOTDIR}/basedir
MOUNTDIR=/tmp/mountdir
FILE=${MOUNTDIR}/file

function _unmount {
  sync
  fusermount -u ${MOUNTDIR}
  sync
  umount ${ROOTDIR}
  sleep 5
}

function _mount {
  mount ${ROOTDIR}
  echo y | ${CRYFS} ${BASEDIR} ${MOUNTDIR}
  sleep 5
}

function _remount {
  _unmount
  _mount
}

function _clear {
  fusermount -u ${MOUNTDIR} || echo not mounted
  umount ${ROOTDIR} || echo not mounted
  mount ${ROOTDIR}
  rm -rf ${BASEDIR}
  mkdir ${BASEDIR}
  umount ${ROOTDIR}
  rm -rf ${MOUNTDIR}
  mkdir ${MOUNTDIR}
  sync
  sleep 5
}

function _createTest {
  echo ----------------
  echo -----Create-----
  echo ----------------
  time dd if=/dev/zero of=${FILE} ${DD_PARAMS}
}

function _readTest {
  echo ----------------
  echo ------Read------
  echo ----------------
  time dd if=${FILE} of=/dev/null ${DD_PARAMS}
}

function _overwriteTest {
  echo ----------------
  echo ---Overwrite----
  echo ----------------
  time dd conv=notrunc if=/dev/zero of=${FILE} ${DD_PARAMS}
}

function _shrinkTest {
  echo ----------------
  echo -----Shrink-----
  echo ----------------
  time dd if=/dev/zero of=${FILE} bs=1M count=1
}

function _deleteTest {
  echo ----------------
  echo -----Delete-----
  echo ----------------
  time rm ${FILE}
}

_clear

_mount

_createTest
_remount

_readTest
_remount

_overwriteTest
_remount

_shrinkTest
_remount

_unmount
_clear
_mount

_createTest
_remount

_readTest
_remount

_overwriteTest
_remount

_deleteTest
_remount

_unmount
