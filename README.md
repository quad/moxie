moxie makes mixtapes!
=====================

Remember [muxtape][mt]? Yeah, that was nice.

[moxie][mx] is like that but for _UNIX nerds_.

Ok, that's cool. I'm not a programmer though...
-----------------------------------------------

No one's perfect. :-) We got you covered.

 1. Use [setuptools][st]!

        $ easy_install moxie

    [Some people][packaging] prefer [pip][pip]. You might be one of those people.

        $ pip install moxie

    We swing both ways.

 2. Make a directory full of MP3s!

        $ ls
        01 Act 1_ Eternal Sunshine (the pledge).mp3
        02-abdominal-breathe_later.mp3
        Blizzard - Village Theme (Diablo I).mp3
        cells-sincity.mp3
        Chromeo-Fancy.mp3
        prefuse73-megachoppedsuite.mp3
        Rihanna feat. Jay-Z - Umbrella (Instrumental).mp3

    Oh jeez, whose are those?

 3. Test it out...

        $ moxie-test
        http://127.0.0.1:8080/

    Almost perfect! Except, that text at the top could be improved.

 4. Make a `README` file:

        $ cat > README
        One Red Mixtape
        Made by [this guy](http://oneredpaperclip.blogspot.com/)!

    A title. And a subtitle!
    
    Did I mention you can use [Markdown][md] with the subtitle? I probably should have.

 5. Use `local.css` if you don't like red. 

        $ cat > local.css
        div#header {
                color: white;
                background-color: black;
        }

    How post-ironic: a black and white mixtape entitled "One _Red_ Mixtape."

 6. `moxie-static` to wrap that sucker up.

        $ moxie-static --verbose --url http://mixtape.quadhome.com/
	Using current directory...
	Wrote ./index.html
	Wrote ./index.rss
	Wrote ./index.xspf
	Wrote ./.moxie.js.swp
	Wrote ./jquery-1.6.2.min.js
	Wrote ./moxie.js
	Wrote ./soundmanager2-nodebug-jsmin.js
	Wrote ./soundmanager2.swf
	Wrote ./style.css


 7. I donno. Put it on a web server someplace?

Hey, that was helpful. But I'm a hacker!
----------------------------------------

Oh ho! Well, just a couple recommendations:

 * [Ditz][d], a fine issue tracker.
 * [git][g] for `git://github.com/quad/moxie.git`
 * [lame][l] to make test data.
 * [nose][n] for all those unittests we forget to write.
 * [SCons][sc] is better than make.
 * [virtualenv][ve]. This is our Opinionated Requirement.

I'm hesitant to ask; but, you know to use `apt`/`emerge`/`yum` and friends. Right?

        $ git clone git://github.com/quad/moxie.git src

        $ virtualenv moxie

        $ . moxie/bin/activate 

        (moxie)$ cd src/
        (moxie)$ ./setup.py develop
        (moxie)$ scons
        (moxie)$ ./setup.py test

Terminal diarrhea throughout this.

        (moxie)$ moxie-test
        http://127.0.0.1:8080/

**IT WORKS!**

        (moxie)$ ditz status
        unassigned  0/ 1 bugfix,    0/ 2 features,  0/ 0 tasks 

Now get to work.

xoxo

-- la moxie comunidad hacker

[mt]: http://muxtape.com/ "Muxtape"
[mx]: http://pypi.python.org/pypi/moxie "Python Package Index : moxie"
[st]: http://peak.telecommunity.com/DevCenter/EasyInstall "EasyInstall"
[packaging]: http://www.b-list.org/weblog/2008/dec/14/packaging/ "James Bennett : On Packaging"
[pip]: http://pip.openplans.org/ "pip documentation"
[md]: http://daringfireball.net/projects/markdown/ "Daring Fireball: Markdown"
[d]: http://ditz.rubyforge.org/ "Ditz"
[g]: http://git.or.cz/ "Git - Fast Version Control System"
[l]: http://lame.sourceforge.net/ "LAME MP3 Encoder"
[n]: http://somethingaboutorange.com/mrl/projects/nose/ "nose: a discovery-based unittest extension"
[sc]: http://www.scons.org/ "SCons: A software construction tool"
[ve]: http://pypi.python.org/pypi/virtualenv "Python Package Index : virtualenv"
