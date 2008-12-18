moxie makes mixtapes!
=====================

Remember [muxtape]? Yeah, that was nice.

[moxie] is like that but for _UNIX nerds_.

Ok, that's cool. I'm not a programmer though...
-----------------------------------------------

No one's perfect. :-) We got you covered.

 1. Use [setuptools]!

        $ easy_install moxie

    [Some people][packaging] prefer [pip]. You might be one of those people.

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

    Oh jeez, whose list is that?

 3. Try it out!

        $ moxie-test
        http://127.0.0.1:8080/

    Almost perfect! Except, that text at the top could be improved.

 4. Make a `README` file!

        $ cat > README
        One Red Mixtape
        Made by [this guy](http://oneredpaperclip.blogspot.com/)!

    A title! And a subtitle! Two lines!
    
    Did I mention you can use [Markdown][md] with the subtitle? I probably
    should have.

 5. Use `local.css` if you don't like red. 

        $ cat > local.css
        div#header {
                color: white;
                background-color: black;
        }

    How post-ironic: a black and white mixtape entitled _One Red Mixtape_.

 6. `moxie-static` to wrap that sucker up.

        $ moxie-static --verbose
        Wrote index.html
        Wrote xspf
        Wrote MusicPlayer.swf
        Wrote style.css
        Wrote jquery-1.2.6.min.js
        Wrote moxie.js
        Wrote expressInstall.swf
        Wrote swfobject.js

 7. I donno. Put it on a web server someplace!

Hey, that was helpful. But I'm a hacker!
----------------------------------------

[muxtape]: http://muxtape.com/ "Muxtape"
[moxie]: http://pypi.python.org/pypi/Moxie "Python Package Index : Moxie"
[setuptools]: http://peak.telecommunity.com/DevCenter/EasyInstall "EasyInstal"
[packaging]: http://www.b-list.org/weblog/2008/dec/14/packaging/ "James Bennett : On Packaging"
[md]: http://daringfireball.net/projects/markdown/ "Daring Fireball: Markdown"
