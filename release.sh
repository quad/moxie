#!/bin/sh -e

git clean -df

if [ -d "release-moxie" ]; then
	rm -rf release-moxie
fi
virtualenv release-moxie
. release-moxie/bin/activate

./setup.py develop -q

scons -Q

./setup.py test -q
./setup.py sdist bdist_egg
