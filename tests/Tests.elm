module Tests exposing (..)

import Char exposing (isDigit)
import Expect
import Fuzz exposing (float, floatRange)
import Random exposing (maxInt)
import Test exposing (..)

import Moxie exposing (Time, minutes_and_seconds)


all : Test
all =
  describe "Moxie Test Suite"
    [ describe "minutes_and_seconds"
      [ test "0 is :00" <|
        \() ->
          Moxie.Time 0
            |> minutes_and_seconds
            |> Expect.equal ":00"
      , test "60 is 1:00" <|
        \() ->
          Moxie.Time 60
            |> minutes_and_seconds
            |> Expect.equal "1:00"
      , fuzz float "The seconds part are digits" <|
        \f ->
          Moxie.Time f
            |> minutes_and_seconds
            |> String.right 2
            |> String.all isDigit
            |> Expect.true "One of the seconds' characters wasn't a digit"
      , fuzz float "The third character is always a ':'" <|
        \f ->
          Moxie.Time f
            |> minutes_and_seconds
            |> String.slice -3 -2
            |> Expect.equal ":"
      , fuzz (floatRange 0 59) ":00 - :59 are three characters long" <|
        \f ->
          Moxie.Time f
            |> minutes_and_seconds
            |> String.length
            |> Expect.equal 3
      , fuzz (floatRange 60 (toFloat Random.maxInt)) "1:00, the minute part is digits" <|
        \f ->
          Moxie.Time f
            |> minutes_and_seconds
            |> String.dropRight 3
            |> String.all isDigit
            |> Expect.true "One of the minutes' characters wasn't a digit"
      ]
    ]
