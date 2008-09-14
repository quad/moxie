/* A XSPF parser.
 *
 * Exposes an ordered array of URLs.
 */

class XSPF {
	public var tracks : Array;
	public var onLoad : Function;

	private var xml : XML;

	public function load(url : String) : Void {
		this.xml = new XML();

		this.xml.ignoreWhite = true;
		this.xml.onLoad = Delegate.create(this, this.parse);

		this.xml.load(url);
	}

	private function parse(success : Boolean) : Void {
		if (!success)
			return;

		/* Load track URLs from trackList > track > location */

		this.tracks = new Array();

		var root : XMLNode = this.xml.firstChild;

		for (var node : XMLNode = root.firstChild;
		     node != null;
		     node = node.nextSibling) {
			if (node.nodeName != "trackList")
				continue;

			for (var track : XMLNode = node.firstChild;
			     track != null;
			     track = track.nextSibling) {
				if (track.nodeName != "track")
					continue;

				for (var track_meta : XMLNode = track.firstChild;
				     track_meta != null;
				     track_meta = track_meta.nextSibling) {
					if (track_meta.nodeName == "location") {
						this.tracks.push(track_meta.firstChild.nodeValue);
						break;
					}
				}
			}
		}

		if (this.tracks != undefined && this.onLoad != undefined)
			this.onLoad();
	}
}
