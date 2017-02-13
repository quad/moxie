import Html exposing (a, div, h1, li, text, span, ul, program)
import Html.Attributes exposing (class, href, id)
import List exposing (indexedMap)

type Duration = Duration Float
type URL = URL String
type PlayState = Playing Track Duration | Paused Track Duration | Stopped

type alias Model =
  { header : Header
  , tracks : List Track
  }

type alias Header =
  { title : String
  , subtitle : String
  , url : URL
  }

type alias Track =
  { artist : String
  , title : String
  , duration : Duration
  , url : URL
  , playing: PlayState
  }

type Msg = None

main : Program Never Model Msg
main = program { init = init, view = view, update = update, subscriptions = subscriptions }

init : (Model, Cmd Msg)
init =
  ( { header =
      { title = "model.header.title"
      , subtitle = "model.header.subtitle"
      , url = URL "#"
      }
    , tracks =
      [ { artist = "track 1",
          title = "title 1",
          duration = Duration 0.0,
          url = URL "#1",
          playing = Stopped
        },
        { artist = "track 2",
          title = "title 2",
          duration = Duration 61.0,
          url = URL "#2",
          playing = Stopped
        }
      ]
    }
  , Cmd.none
  )

view : Model -> Html.Html Msg
view {header, tracks} =
  div []
    [ header_view header
    , tracks_view
        <| indexedMap track_view
        <| tracks
    ]

header_view : Header -> Html.Html Msg
header_view {title, subtitle, url} =
  case url of
    URL url ->
      div [id "header"]
        [ h1 [] [text title]
        , a [href url] [text subtitle]
        ]

tracks_view : List (Html.Html msg) -> Html.Html msg
tracks_view tracks =
  ul [class "songs"] tracks

track_view : Int -> Track -> Html.Html Msg
track_view index {artist, title, url} =
  let
    number = toString (index + 1)
    track_id = "track_" ++ number
    name = artist ++ " - " ++ title
    (URL url_) = url
  in
    li
      [ class "song"
      , id track_id
      ]
      [ a [class "title", href url_] [text name]
      , span [class "time"]
        [ span [class "position"] [text "0:00"]
        , span [class "duration"] [text "0:00"]
        ]
      ]

update : Msg -> Model -> (Model, Cmd msg)
update msg model =
  (model, Cmd.none)

subscriptions : Model -> Sub Msg
subscriptions model = Sub.none
