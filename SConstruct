debug = ARGUMENTS.get('debug', 0)

mtasc_options = ['-strict', '-header 0:0:0', '-version 8', '-main']

if debug:
  mtasc_options.append('-trace MusicPlayer.log')

mtasc = Builder(action = "mtasc %s $SOURCE -swf $TARGET" % (' '.join(mtasc_options)),
                suffix = '.swf',
                src_suffix = '.as')

env = Environment(BUILDERS = {'ActionScript': mtasc})

env.ActionScript(source = 'MusicPlayer', target = 'static/MusicPlayer')
