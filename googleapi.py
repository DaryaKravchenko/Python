from googleplaces import GooglePlaces, types, lang

access_token = ''
typesRest = [types.TYPE_RESTAURANT, types.TYPE_CAFE, types.TYPE_BAR]
typesCinema = [types.TYPE_MOVIE_THEATER, types.TYPE_PARK, types.TYPE_MUSEUM]
typeShops = [types.TYPE_STORE]


def getplaces(location, state):
    google_places = GooglePlaces(access_token)

    if state == 1:
        typesNeed = typesRest
    elif state == 2:
        typesNeed = typesCinema
    else:
        typesNeed = typeShops

    query_result = google_places.nearby_search(lat_lng=location, radius=1000, types=typesNeed, language=lang.RUSSIAN)

    places = []

    for i in query_result.places:
        places.append({'name': i.name, 'location': i.geo_location})

    return places




