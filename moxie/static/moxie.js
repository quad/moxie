var STOPPED = 0;
var PLAYING = 1;
var PAUSED = 2;

var _player;
var _player_status;
var _player_track;
var _player_position;

var _original_title;

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

	// Immediately update.

	track_update(null);
}

function track_update(event) {
	_songs.each(function(index) {
		var message = $(this).find("span.position");

		if (_player_status && _player_track == index) {
			var counter;

			if (_player_position) {
				var time = Math.round(_player_position / 1000);

				counter = render_duration(time) + "&nbsp;/";
			}
			else {
				counter = "&hellip;&nbsp;/";
			}

			message.html(counter);

			$(this).addClass("active");

			if (_player_status == PLAYING) {
				$(this).addClass("playing");
				$(this).removeClass("paused");
			}
			else if (_player_status == PAUSED) {
				$(this).addClass("paused");
				$(this).removeClass("playing");
			}

			var title = $(this).find(".title");
			document.title = jQuery.trim(title.text()) + " | " + _original_title;
		}
		else {
			message.html("");

			$(this).removeClass("active");
			$(this).removeClass("playing");
			$(this).removeClass("paused");
		}
	});
}

function MusicPlayer_callback() {
	_player = $("#player")[0];
	_songs = $("li.song");

	_original_title = document.title;

	_songs.click(function(event) { track_click(event, false); });
	$("ul.songs").everyTime("1s", track_update);
}

function MusicPlayer_update(status, track, position) {
	_player_status = status;
	_player_track = track;
	_player_position = position;
}
