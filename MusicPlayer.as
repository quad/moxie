import flash.external.ExternalInterface;

class MusicPlayer {
	private var urls : Array;
	private var sound : Sound;
	private var track : Number;
	private var status : Number;
	private var pausedOffset : Number;

	public static var STOPPED : Number = 0;
	public static var PLAYING : Number = 1;
	public static var PAUSED : Number = 2;

	public function MusicPlayer(urls : Array) {
		this.urls = urls;
		this.sound = new Sound(_root);

		this.sound.onSoundComplete = Delegate.create(this, this.onSoundComplete);
	}

	public function connectExternal() : Void {
		ExternalInterface.addCallback("play", this, this.play);
		ExternalInterface.addCallback("stop", this, this.stop);
		ExternalInterface.addCallback("pause", this, this.pause);

		ExternalInterface.addCallback("getStatus", this, function() : Void { return this.status });
		ExternalInterface.addCallback("getTrack", this, function() : Void { return this.track });

		ExternalInterface.addCallback("getPosition", this, function() : Void { return this.sound.position });
	}

	public function play(number : Number) : Void {
		if (number == null && this.status == PAUSED) {
			this.sound.start(this.pausedOffset / 1000);
		}
		else {
			number = (number == null) ? 0 : number;

			// Reset the position on the sound object.
			this.sound.stop();
			this.sound.start(0);
			this.sound.stop();

			this.sound.loadSound(this.urls[number], true);

			this.track = number;
		}

		this.status = PLAYING;
	}

	public function stop() : Void {
		this.sound.stop();

		this.track = undefined;
		this.status = STOPPED;
	}

	public function pause() : Void {
		this.pausedOffset = this.sound.position;

		this.sound.stop();

		this.status = PAUSED;
	}

	private function onSoundComplete() : Void {
		// If there is another track, play it.
		var next_track : Number = this.track + 1;

		this.stop();

		if (next_track < this.urls.length)
			this.play(next_track);
	}

	public static function main() : Void {
		if (_root.playlist == undefined)
			return;

		var playlist : XSPF = new XSPF();

		playlist.onLoad = function () {
			var player : MusicPlayer = new MusicPlayer(this.tracks);
			player.connectExternal();

			ExternalInterface.call("MusicPlayer_callback");
		}

		playlist.load(_root.playlist);
	}

	public static function log(args : Object) : Void {
		ExternalInterface.call("console.log", args);
	}
}
