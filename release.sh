#!/bin/sh -x

git clean -df

if [ -d "release-moxie" ]; then
	rm -rf release-moxie
fi
virtualenv release-moxie
. release-moxie/bin/activate

scons

nosetests

./setup.py sdist bdist_egg
