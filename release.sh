#!/bin/sh -x

git clean -df

if [ -d "release-moxie" ]; then
	rm -rf release-moxie
fi
virtualenv release-moxie
. release-moxie/bin/activate

scons

./setup test

./setup sdist bdist_egg
