import json
import os
import random
import time


def initialize_game_info(json_date):
    result = check_if_necessary_key_existing(json_date)
    if result:
        return result

    result = check_invalid_value_for_initialization(json_date)
    if result:
        return result

    return 0

    match_id = json_date['match_id']
    various_delete(match_id)
    write_game_info(json_date)
    append_to_authorization(json_date)
    result = "initialization was executed"

    return result


def check_if_necessary_key_existing(json_date):

    return ""


def check_invalid_value_for_initialization(json_date):
    return ""


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


