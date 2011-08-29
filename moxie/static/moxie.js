soundManager.onready(function () {
	"use strict";

	var original_title = document.title;

	function render_duration(time) {
		function leadingZero(s) {
			return (s > 9) ? s : ("0" + s);
		}

		var seconds  = time % 60,
		    minutes  = Math.floor(time / 60) % 60,
		    hours    = Math.floor(time / (60 * 60)),
		    duration = ":" + leadingZero(seconds);

		if (hours) {
			duration = hours + ":" + leadingZero(minutes) + duration;
		} else if (minutes) {
			duration = minutes + duration;
		}

		return duration;
	}

	$("li.song").each(function () {
		var e       = $(this),
		    next_e  = e.next(),
		    message = function (html) { e.find(".position").html(html); },
		    timer   = function (html) { message(html + "&nbsp;/&nbsp;"); };

		e.data("sound", soundManager.createSound({
			id: e.attr("id"),
			url: e.find("a").attr("href"),
			whileloading: function () {
				e.addClass("active");

				if (!this.position) {
					timer("&hellip;");
				}
			},
			whileplaying: function () {
				e.addClass("active");

				if (this.position) {
					var time = Math.round(this.position / 1000);
					timer(render_duration(time));

					e.addClass("playing");
					e.removeClass("paused");

					document.title = $.trim(e.find(".title").text()) + " | " + original_title;
				}
			},
			onpause: function () {
				e.addClass("paused");
				e.removeClass("playing");
			},
			onbeforefinish: function () {
				var next_sound = next_e.data("sound");

				if (next_sound) {
					setTimeout(function () { next_sound.load(); }, 0);
				}
			},
			onstop: function () {
				message("");

				e.removeClass("active");
				e.removeClass("paused");
				e.removeClass("playing");

				document.title = original_title;
			},
			onfinish: function () {
				this.options.onstop();

				var next_sound = next_e.data("sound");

				if (next_sound) {
					setTimeout(function () { next_sound.play(); }, 0);
				}
			}
		}));
	});

	$("li.song").click(function () {
		var track = $(this).data("sound");

		if (track.playState) {
			track.togglePause();
		} else {
			soundManager.stopAll();
			track.play();
		}

		return false;
	});
});
