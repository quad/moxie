module Moxie exposing (..)

import Html exposing (a, div, h1, li, text, span, ul, program)
import Html.Attributes exposing (class, href, id)
import List exposing (indexedMap)

type Time = Time Float
type URL = URL String
type Status = Playing Track Time | Paused Track Time | Stopped

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
  , duration : Time
  , url : URL
  , status: Status
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
          duration = Time 0.0,
          url = URL "#1",
          status = Stopped
        },
        { artist = "track 2",
          title = "title 2",
          duration = Time 61.0,
          url = URL "#2",
          status = Stopped
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
track_view index {artist, title, url, duration} =
  let
    number = toString (index + 1)
    track_id = "track_" ++ number
    name = artist ++ " - " ++ title
    (URL url_) = url
    duration_ = minutes_and_seconds duration
  in
    li
      [ class "song"
      , id track_id
      ]
      [ a [class "title", href url_] [text name]
      , span [class "time"]
        [ span [class "position"] [text "0:00"]
        , span [class "duration"] [text duration_]
        ]
      ]

minutes_and_seconds : Time -> String
minutes_and_seconds (Time time) =
  let
    seconds =
      floor time % 60
        |> toString
        |> String.padLeft 2 '0'
    minutes =
      floor time // 60
        |> toString
  in
    if time >= 60 then
      minutes ++ ":" ++ seconds
    else
      ":" ++ seconds

update : Msg -> Model -> (Model, Cmd msg)
update msg model =
  (model, Cmd.none)

subscriptions : Model -> Sub Msg
subscriptions model = Sub.none
