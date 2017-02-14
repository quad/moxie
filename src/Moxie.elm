module Moxie exposing (..)

import Html exposing (a, div, h1, li, text, span, ul, program)
import Html.Attributes exposing (class, href, id)
import List exposing (indexedMap)


type Time
    = Time Float


type URL
    = URL String


type Status
    = Playing Time
    | Paused Time
    | Stopped


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
    , status : Status
    }


type Msg
    = None


main : Program Never Model Msg
main =
    program { init = init, view = view, update = update, subscriptions = subscriptions }


init : ( Model, Cmd Msg )
init =
    ( { header =
            { title = "model.header.title"
            , subtitle = "model.header.subtitle"
            , url = URL "#"
            }
      , tracks =
            [ { artist = "track 1"
              , title = "title 1"
              , duration = Time 123.4
              , url = URL "#1"
              , status = Playing <| Time 12.34
              }
            , { artist = "track 2"
              , title = "title 2"
              , duration = Time 61.0
              , url = URL "#2"
              , status = Paused <| Time 1.234
              }
            , { artist = "track 3"
              , title = "title 3"
              , duration = Time 0
              , url = URL "#3"
              , status = Stopped
              }
            ]
      }
    , Cmd.none
    )


view : Model -> Html.Html Msg
view { header, tracks } =
    div []
        [ header_view header
        , tracks
            |> indexedMap track_view
            |> tracks_view
        ]


header_view : Header -> Html.Html Msg
header_view { title, subtitle, url } =
    case url of
        URL url ->
            div [ id "header" ]
                [ h1 [] [ text title ]
                , a [ href url ] [ text subtitle ]
                ]


tracks_view : List (Html.Html msg) -> Html.Html msg
tracks_view tracks =
    ul [ class "songs" ] tracks


track_view : Int -> Track -> Html.Html Msg
track_view index { artist, title, url, duration, status } =
    let
        number =
            toString (index + 1)

        (URL url_) =
            url

        ( track_class, time ) =
            case status of
                Playing t ->
                    ( "song playing", t )

                Paused t ->
                    ( "song paused", t )

                Stopped ->
                    ( "song", Time 0.0 )

        track_id =
            "track_" ++ number

        track_name =
            artist ++ " - " ++ title

        track_time =
            minutes_and_seconds time

        track_duration =
            minutes_and_seconds duration
    in
        li
            [ class track_class
            , id track_id
            ]
            [ a [ class "title", href url_ ] [ text track_name ]
            , span [ class "time" ]
                [ span [ class "position" ] [ text track_time ]
                , span [ class "duration" ] [ text track_duration ]
                ]
            ]


minutes_and_seconds : Time -> String
minutes_and_seconds (Time time) =
    let
        t =
            floor time

        seconds =
            t
                % 60
                |> toString
                |> String.padLeft 2 '0'

        minutes =
            t
                // 60
                |> toString
    in
        if time >= 60 then
            minutes ++ ":" ++ seconds
        else
            ":" ++ seconds


update : Msg -> Model -> ( Model, Cmd msg )
update msg model =
    ( model, Cmd.none )


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none
