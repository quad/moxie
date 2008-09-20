class Track {
	public var onSoundComplete : Function;
	public var pausedOffset : Number;
	public var sound : Sound = undefined;
	public var url : String;

	public function Track(url : String) {
		this.url = url;
	}

	private function _onSoundComplete() : Void {
		this.onSoundComplete();
	}

	public function play() : Void {
		if (this.sound == undefined) {
			this.sound = new Sound();
			this.sound.onSoundComplete = Delegate.create(this, this._onSoundComplete);

			this.sound.loadSound(this.url, true);
		}

		if (this.pausedOffset)
			this.sound.start(this.pausedOffset / 1000);
		else
			this.sound.start();

		this.pausedOffset = undefined;
	}

	public function stop() : Void {
		this.pausedOffset = undefined;

		if (this.sound)
			this.sound.stop();
	}

	public function pause() : Void {
		this.pausedOffset = this.sound.position;

		if (this.sound)
			this.sound.stop();
	}

	public function isPaused() : Boolean {
		return this.pausedOffset != undefined;
	}
}
