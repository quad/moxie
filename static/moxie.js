var STOPPED = 0;
var PLAYING = 1;
var PAUSED = 2;

function track_click(event, shouldStop)
{
	var player = $("#player")[0];
	var track = parseInt($(event.currentTarget)[0].id, 10);

	// Pause/stop if we're playing the track, otherwise play it!

	if (player.getStatus() == PLAYING && player.getTrack() == track)
	{
		if (shouldStop)
			player.stop();
		else
			player.pause();
	}
	else
	{
		if (player.getTrack() == track)
			player.play();
		else
			player.play(track);
	}
}

function track_update(event)
{
	var player = $("#player")[0];
	var track = $(this)[0].id;

	var message;

	if (player.getStatus() && player.getTrack() == track)
	{
		message = Math.round(player.getPosition() / 1000) + "&nbsp; /";
	}
	else
	{
		message = "&#9835;";
	}

	$(this).find(".time").html(message);
}

function MusicPlayer_callback()
{
	$("li.song").click(function(event) { track_click(event, false); });
	$("li.song").dblclick(function(event) { track_click(event, true); });
	$("li.song").everyTime("1s", track_update);
}
