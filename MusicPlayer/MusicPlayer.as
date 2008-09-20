import flash.external.ExternalInterface;

class MusicPlayer {
	private static var player : MusicPlayer;

	public static var STOPPED : Number = 0;
	public static var PLAYING : Number = 1;
	public static var PAUSED : Number = 2;

	private var urls : Array = [];
	private var tracks : Object = {};

	private var playing_index : Number = 0;
	private var playing_track : Object = undefined;

	public function MusicPlayer(urls : Array) {
		this.urls = urls;

		var OSC_callback : Function = Delegate.create(this, this.onSoundComplete);

		for (var url : String in this.urls)
		{
			url = this.urls[url];

			this.tracks[url] = new Track(url);
			this.tracks[url].onSoundComplete = OSC_callback;
		}
	}

	private function onSoundComplete() {
                // If there is another track, play it.
                var next_index : Number = this.playing_index + 1;

		if (next_index < this.urls.length)
			this.play(next_index);
	}

	public function connectExternal() : Void {
		ExternalInterface.addCallback("play", this, this.play);
		ExternalInterface.addCallback("pause", this, this.pause);

		ExternalInterface.call("MusicPlayer_callback");

		setInterval(Delegate.create(this, this._update), 1000);
	}

	private function _update() : Void {
		var status : Number;

		if (this.playing_track) {
			if (this.playing_track.isPaused()) {
				status = PAUSED;
			}
			else {
				status = PLAYING;
			}
		}
		else {
			status = STOPPED;
		}

		ExternalInterface.call("MusicPlayer_update",
				       status,
				       this.playing_index,
				       this.playing_track.sound.position);
	}

	public function play(index : Number) : Void {
		if (index == null && this.playing_track.isPaused()) {
			this.playing_track.play();
		}
		else {
			this.playing_track.stop();

			index = (index == null) ? 0 : index;

			this.playing_index = index;
			this.playing_track = this.tracks[this.urls[index]];

			this.playing_track.play();
		}
	}

	public function pause() : Void {
		if (this.playing_track)
			this.playing_track.pause();
	}

	public static function main() : Void {
		if (_root.playlist == undefined)
			return;

		var playlist : XSPF = new XSPF();

		playlist.onLoad = function() : Void  {
			MusicPlayer.player = new MusicPlayer(this.tracks);
			MusicPlayer.player.connectExternal();
		}

		playlist.load(_root.playlist);
	}

	public static function log(args : Object) : Void {
		ExternalInterface.call("console.log", args);
	}
}
