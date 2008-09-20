var STOPPED = 0;
var PLAYING = 1;
var PAUSED = 2;

var _player;
var _player_status;
var _player_track;
var _player_position;

var _songs;

function render_duration(time) {
	var seconds = time % 60;
	var minutes = Math.floor(time / 60) % 60;
	var hours   = Math.floor(time / (60 * 60));

	function leadingZero(s) {
		return (s > 9) ? s : ("0" + s);
	}

	var duration = ":" + leadingZero(seconds);

	if (hours)
		duration = hours + ":" + leadingZero(minutes) + duration;
	else if (minutes)
		duration = minutes + duration;

	return duration;
}

function track_click(event) {
	var track = parseInt($(event.currentTarget)[0].id, 10);

	// Pause if we're playing the track, otherwise play it!

	if (_player_status == PLAYING && _player_track == track)
		_player.pause();
	else
		if (_player_track == track)
			_player.play();
		else
			_player.play(track);
}

function track_update(event) {
	if (_player_status) {
		var time = Math.round(_player_position / 1000);
		var message = render_duration(time) + "&nbsp;/";

		$("li.song#" + _player_track).find("span.position").html(message);
	}

	_songs.each(function(index) {
		if (_player_status && _player_track == index)
			return;

		$(this).find("span.position").html("");
	});
}

function MusicPlayer_callback() {
	_player = $("#player")[0];

	_songs = $("li.song");
	_songs.click(function(event) { track_click(event, false); });

	$("ul.songs").everyTime("1s", track_update);
}

function MusicPlayer_update(status, track, position) {
	_player_status = status;
	_player_track = track;
	_player_position = position;
}
