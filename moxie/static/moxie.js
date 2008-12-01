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

	if (hours) {
		duration = hours + ":" + leadingZero(minutes) + duration;
	}
	else if (minutes) {
		duration = minutes + duration;
	}

	return duration;
}

function track_update() {
	_songs.each(function (index) {
		var message = $(this).find("span.position");

		if (_player_status && _player_track == index) {
			var counter;

			// Update the position counter.

			if (_player_position) {
				var time = Math.round(_player_position / 1000);

				counter = render_duration(time);
			}
			else {
				counter = "&hellip;";
			}

			counter = counter + "&nbsp;/&nbsp;";

			message.html(counter);

			// Update the CSS styles.

			$(this).addClass("active");

			if (_player_status == PLAYING) {
				$(this).addClass("playing");
				$(this).removeClass("paused");

				// Update the title with the track name.
				var title_dom = $(this).find(".title");
				document.title = $.trim(title_dom.text()) + " | " + _original_title;
			}
			else if (_player_status == PAUSED) {
				$(this).addClass("paused");
				$(this).removeClass("playing");
			}
		}
		else {
			// Clear any stale position counters.
			message.html("");

			// Clear any stale CSS styles.
			$(this).removeClass("active");
			$(this).removeClass("playing");
			$(this).removeClass("paused");
		}
	});

	if (_player_status == STOPPED) {
		// Reset the title.
		document.title = _original_title;
	}
}

function track_click() {
	// This is a work-around for IE not supporting .currentTarget.
	// http://www.quirksmode.org/js/events_order.html
	var track = parseInt($(this).attr("id"), 10);

	// Pause if we're playing the track, otherwise play it!
	if (_player_status == PLAYING && _player_track == track) {
		_player.MusicPlayer_pause();
	}
	else {
		if (_player_track == track) {
			_player.MusicPlayer_play();
		}
		else {
			_player.MusicPlayer_play(track);
		}
	}

	// Immediately update.
	track_update();
}

function MusicPlayer_callback() {
	// Cache repeated references.
	_player = swfobject.getObjectById("player");    // Use swfobject for browser compatibility.
	_songs = $("li.song");
	_original_title = document.title;

	// Bind DOM events.
	_songs.click(track_click);
}

function MusicPlayer_update(status, track, position) {
	_player_status = status;
	_player_track = track;
	_player_position = position;

	track_update();
}
