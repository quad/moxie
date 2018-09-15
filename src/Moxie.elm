port module Moxie exposing (Time(..), minutes_and_seconds, pause, play, rewind)

import Browser exposing (document)
import Html exposing (a, audio, div, h1, li, span, text, ul)
import Html.Attributes exposing (class, href, id, preload, rel, src, target)
import Html.Events exposing (on, preventDefaultOn)
import Http
import Json.Decode as Json exposing (field)
import List exposing (indexedMap)


type Time
    = Time Float


decodeTime =
    Json.map Time Json.float


type URL
    = URL String


type Status
    = Loading
    | Playing Time
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
    | Progress Int Time
    | End Int


main =
    document { init = init, view = view, update = update, subscriptions = subscriptions }


init : () -> ( Model, Cmd Msg )
init _ =
    ( { header =
            { title = "model.header.title"
            , subtitle = "model.header.subtitle"
            , url = URL "#"
            }
      , tracks = []
      }
    , getIndexJson
    )


getIndexJson =
    Http.get "index.json" decodeIndexJson
        |> Http.send Index


decodeIndexJson =
    let
        decodeURL =
            Json.map URL Json.string

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
    Json.map2 (\a b -> ( a, b ))
        decodeHeader
        decodeTracks


view { header, tracks } =
    { title = header.title
    , body =
        [ case tracks of
            [] ->
                div [ class "initing" ] []

            _ :: _ ->
                div []
                    [ header_view header
                    , tracks
                        |> indexedMap track_view
                        |> tracks_view
                    ]
        ]
    }


header_view { title, subtitle, url } =
    case url of
        URL u ->
            div [ id "header" ]
                [ h1 [ id "title" ] [ text title ]
                , a
                    [ id "subtitle"
                    , href u
                    , rel "noopener"
                    , target "_blank"
                    ]
                    [ text subtitle ]
                ]


tracks_view tracks =
    ul [ id "songs" ] tracks


track_view index { artist, title, url, duration, status } =
    let
        number =
            String.fromInt (index + 1)

        (URL track_url) =
            url

        ( track_class, time, onClick_msg ) =
            case status of
                Loading ->
                    ( "song playing loading", Nothing, Pause index )

                Playing t ->
                    ( "song playing", Just t, Pause index )

                Paused t ->
                    ( "song paused", Just t, Resume index )

                Stopped ->
                    ( "song", Nothing, Play index )

        track_id =
            "track_" ++ number

        track_name =
            artist ++ " - " ++ title

        track_time =
            case time of
                Just t ->
                    minutes_and_seconds t

                Nothing ->
                    ""

        track_duration =
            minutes_and_seconds duration
    in
    li
        [ class track_class
        , id track_id
        , onClick onClick_msg
        ]
        [ a [ class "name", href track_url ] [ text track_name ]
        , span [ class "time" ]
            [ span [ class "position" ] [ text track_time ]
            , span [ class "duration" ] [ text track_duration ]
            ]
        , audio [ src track_url, preload "none", onTimeUpdate <| Progress index, onEnded <| End index ] []
        ]


onTimeUpdate message =
    decodeTime
        |> Json.at [ "target", "currentTime" ]
        |> Json.map message
        |> on "timeupdate"


onEnded message =
    message
        |> Json.succeed
        |> on "ended"


minutes_and_seconds (Time time) =
    let
        t =
            max 0 time
                |> floor

        seconds =
            modBy 60 t
                |> String.fromInt
                |> String.padLeft 2 '0'

        minutes =
            t
                // 60
                |> String.fromInt
    in
    if time >= 60 then
        minutes ++ ":" ++ seconds

    else
        ":" ++ seconds


onClick message =
    preventDefaultOn
        "click"
        (Json.succeed ( message, True ))


ffi tracks =
    tracks
        |> indexedMap
            (\i t ->
                case t.status of
                    Loading ->
                        [ rewind i, play i ]

                    Playing _ ->
                        [ play i ]

                    Paused _ ->
                        [ pause i ]

                    Stopped ->
                        [ pause i ]
            )
        |> List.concat
        |> Cmd.batch


update msg model =
    case msg of
        Index (Ok ( header, tracks )) ->
            ( { model | header = header, tracks = tracks }, Cmd.none )

        Index (Err _) ->
            ( model, Cmd.none )

        Play i ->
            let
                set =
                    \idx t ->
                        if idx == i then
                            { t | status = Loading }

                        else
                            { t | status = Stopped }

                m =
                    { model | tracks = indexedMap set model.tracks }
            in
            ( m, ffi m.tracks )

        Pause i ->
            let
                set =
                    \idx t ->
                        case ( idx == i, t.status ) of
                            ( True, Playing (Time time) ) ->
                                { t | status = Paused <| Time time }

                            ( _, _ ) ->
                                { t | status = Stopped }

                m =
                    { model | tracks = indexedMap set model.tracks }
            in
            ( m, ffi m.tracks )

        Resume i ->
            let
                set =
                    \idx t ->
                        case ( idx == i, t.status ) of
                            ( True, Paused (Time time) ) ->
                                { t | status = Playing <| Time time }

                            ( _, _ ) ->
                                { t | status = Stopped }

                m =
                    { model | tracks = indexedMap set model.tracks }
            in
            ( m, ffi m.tracks )

        Progress i t ->
            let
                set =
                    \idx tr ->
                        case ( idx == i, tr.status ) of
                            ( True, Loading ) ->
                                { tr | status = Playing t }

                            ( True, Playing _ ) ->
                                { tr | status = Playing t }

                            ( True, Paused _ ) ->
                                { tr | status = Paused t }

                            ( _, _ ) ->
                                tr

                m =
                    { model | tracks = indexedMap set model.tracks }
            in
            ( m, Cmd.none )

        End i ->
            let
                set =
                    \idx t ->
                        case ( idx == (i + 1), t.status ) of
                            ( True, Stopped ) ->
                                { t | status = Loading }

                            ( _, _ ) ->
                                { t | status = Stopped }

                m =
                    { model | tracks = indexedMap set model.tracks }
            in
            ( m, ffi m.tracks )


port rewind : Int -> Cmd msg


port play : Int -> Cmd msg


port pause : Int -> Cmd msg


subscriptions model =
    Sub.none
