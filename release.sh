#!/bin/sh -x

git clean -df
scons
./setup test
./setup sdist bdist_egg
