from main import FlightObject, bellman_ford, parse_flights


def test_bellman_ford_logic():
    # Standard case: 0 -> 1 ($100), 1 -> 2 ($100), 0 -> 2 ($500)
    # k=1 stop: 0->1->2 is $200
    flights = [(0, 1, 100), (1, 2, 100), (0, 2, 500)]
    assert bellman_ford(3, flights, 0, 2, 1) == 200
    # k=0 stops: must take 0->2 ($500)
    assert bellman_ford(3, flights, 0, 2, 0) == 500


def test_parse_flights_formats():
    # Test dictionary format (the one that was causing the ValueError)
    # In the actual app, these are now Pydantic objects after InputData validation
    dict_flights = [FlightObject(src=0, dst=1, price=100.0)]
    assert parse_flights(dict_flights) == [(0, 1, 100.0)]

    # Test list format
    list_flights = [[0, 1, 100]]
    assert parse_flights(list_flights) == [(0, 1, 100)]
