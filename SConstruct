debug = ARGUMENTS.get('debug', 0)

mtasc_options = ['-strict', '-header 0:0:0', '-version 8', '-main', '-cp MusicPlayer/']

if debug:
  mtasc_options.append('-trace MusicPlayer.log')

mtasc = Builder(action = "mtasc %s $SOURCE -swf $TARGET" % (' '.join(mtasc_options)),
                suffix = '.swf',
                src_suffix = '.as')

env = Environment(BUILDERS = {'ActionScript': mtasc})

env.ActionScript(source = 'MusicPlayer/MusicPlayer', target = 'moxie/static/MusicPlayer')
