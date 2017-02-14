module Moxie exposing (..)

import Html exposing (a, audio, div, h1, li, text, span, ul, program)
import Html.Attributes exposing (class, href, id, src)
import Html.Events exposing (onWithOptions, defaultOptions)
import Http
import Json.Decode as Json
import Json.Decode exposing (field)
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
    = Index (Result Http.Error ( Header, List Track ))
    | Play Int
    | Pause Int
    | Resume Int


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
    , getIndexJson
    )


getIndexJson : Cmd Msg
getIndexJson =
    Http.get "index.json" decodeIndexJson
        |> Http.send Index


decodeIndexJson : Json.Decoder ( Header, List Track )
decodeIndexJson =
    let
        decodeURL =
            Json.map URL Json.string

        decodeTime =
            Json.map Time Json.float

        decodeHeader =
            Json.map3 Header
                (field "title" Json.string)
                (field "subtitle" Json.string)
                (field "url" decodeURL)

        decodeTracks =
            field "tracks" (Json.list decodeTrack)

        decodeTrack =
            Json.map5 Track
                (field "artist" Json.string)
                (field "title" Json.string)
                (field "duration" decodeTime)
                (field "url" decodeURL)
                (Json.succeed Stopped)
    in
        Json.map2 (,)
            decodeHeader
            decodeTracks


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

        (URL track_url) =
            url

        ( track_class, time, onClick_msg ) =
            case status of
                Playing t ->
                    ( "song playing", t, Pause index )

                Paused t ->
                    ( "song paused", t, Resume index )

                Stopped ->
                    ( "song", Time 0, Play index )

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
            , onClickPreventDefault onClick_msg
            ]
            [ a [ class "title", href track_url ] [ text track_name ]
            , span [ class "time" ]
                [ span [ class "position" ] [ text track_time ]
                , span [ class "duration" ] [ text track_duration ]
                ]
            , audio [ src track_url ] []
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


onClickPreventDefault : a -> Html.Attribute a
onClickPreventDefault message =
    onWithOptions
        "click"
        { defaultOptions | preventDefault = True }
        (Json.succeed message)


update : Msg -> Model -> ( Model, Cmd msg )
update msg model =
    case msg of
        Index (Ok ( header, tracks )) ->
            ( { model | header = header, tracks = tracks }, Cmd.none )

        Index (Err _) ->
            ( model, Cmd.none )

        Play i ->
            ( { model
                | tracks =
                    model.tracks
                        |> indexedMap
                            (\idx track ->
                                case ( idx == i, track.status ) of
                                    ( True, Stopped ) ->
                                        { track | status = Playing <| Time 0 }

                                    ( _, _ ) ->
                                        { track | status = Stopped }
                            )
              }
            , Cmd.none
            )

        Pause i ->
            ( { model
                | tracks =
                    model.tracks
                        |> indexedMap
                            (\idx track ->
                                case ( idx == i, track.status ) of
                                    ( True, Playing (Time time) ) ->
                                        { track | status = Paused <| Time time }

                                    ( _, _ ) ->
                                        { track | status = Stopped }
                            )
              }
            , Cmd.none
            )

        Resume i ->
            ( { model
                | tracks =
                    model.tracks
                        |> indexedMap
                            (\idx track ->
                                case ( idx == i, track.status ) of
                                    ( True, Paused (Time time) ) ->
                                        { track | status = Playing <| Time time }

                                    ( _, _ ) ->
                                        { track | status = Stopped }
                            )
              }
            , Cmd.none
            )


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none
