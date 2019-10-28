import json
import os
import random
import time


def initialize_game_info(json_date):
    result = check_all_error_factor(json_date)
    if result:
        return result

    return "HI!"

    match_id = json_date['id']
    various_delete(match_id)
    write_game_info(json_date)
    append_to_authorization(json_date)
    result = "initialization was executed"

    return result


def check_all_error_factor(json_date):
    result = check_if_necessary_key_existing(json_date)
    if result:
        return result

    result = check_if_it_has_already_been_initialized(json_date['id'])
    if result:
        return result

    make_up_for_wanting_value(json_date)

    result = check_contradictory_value_for_initialization(json_date)
    if result:
        return result

    return ""


def check_if_necessary_key_existing(json_date):
    result = []
    if 'id' not in json_date:
        result.append("no id")
    if 'Authorization' not in json_date:
        result.append("no Authorization")
    else:
        authorizations = json_date['Authorization']
        if len(authorizations) != 2:
            result.append("Authorization must be two")
        else:
            for auth in authorizations:
                if 'token' not in auth:
                    result.append("no token")
                if 'teamID' not in auth:
                    result.append("no teamID")

    return result


def check_if_it_has_already_been_initialized(match_id):
    # turn == turnsであれば残していいかも
    return ""


def check_contradictory_value_for_initialization(json_date):
    result = []
    key_names = ['id', 'intervalMillis', 'turnMillis', 'turns', 'startedAtUnixTime', 'height', 'width']
    range_of_values = [(0, 10**9), (0, 10**4), (0, 10**5), (1, 60), (0, 10**4), (1, 20), (1, 20)]
    key_names_and_range_of_values = list(zip(key_names, range_of_values))

    for key_name_and_range_of_value in key_names_and_range_of_values:
        key_name = key_name_and_range_of_value[0]
        lower_limit = key_name_and_range_of_value[1][0]
        upper_limit = key_name_and_range_of_value[1][1]
        value = json_date[key_name]
        if not type(value) is int:
            result.append(key_name + "' must be int")
        elif not lower_limit <= value <= upper_limit:
            result.append(key_name + " must be from " + str(lower_limit) + " to " + str(upper_limit) + " inclusive")

    # あとpoints, tiledをheight,widthで判定

    return result


def make_up_for_wanting_value(json_date):
    hgoe = 0


def various_delete(match_id):
    path = "./matchID:" + str(match_id) + "___field_information.json"
    if os.path.isfile(path):
        os.remove(path)


def write_game_info(json_date):
    # id,
    # intervalMillis,
    # turnMillis,
    # turns,
    #
    # startedAtUnixTime,
    # turn,
    # height,
    # width,
    # points,
    # tiled,
    # teams
    # {teamName},
    # actions
    return 0


def append_to_authorization(json_date):
    return 0


