import json
import os
import random
import time


def initialize_game_info(json_date):
    result = check_all_error_factor(json_date)
    if result:
        return result

    match_id = json_date['id']
    json_date['startedAtUnixTime'] += int(time.time())
    make_up_for_dependent_info(json_date)
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

    result = check_value_of_authorization(json_date)
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
                    result.append("no Authorization's token")
                if 'teamID' not in auth:
                    result.append("no Authorization's teamID")

    return result


def check_if_it_has_already_been_initialized(match_id):
    # turn == turnsであれば残していいかも->ちゃんとファイルは消そうね
    return ""


def check_value_of_authorization(json_date):
    result = []
    for Authorization in json_date['Authorization']:
        token = Authorization['token']
        teamID = Authorization['teamID']
        if not type(token) is str:
            result.append("token must be str")
        if not type(teamID) is int:
            result.append("Authorization's teamID must be str")
        if not 0 < len(token) <= 10 ** 5:
            result.append("token length must be from 1 to 10^5 inclusive")
        if not 0 < teamID <= 10 ** 5:
            result.append("Authorization's teamID must be from 1 to 10^5 inclusive")

    if not result:
        token_list = []
        teamID_list = []
        for Authorization in json_date['Authorization']:
            token_list.append(Authorization['token'])
            teamID_list.append(Authorization['teamID'])

        if len(token_list) != len(set(token_list)):
            result.append("contains the same token")
        if len(teamID_list) != len(set(teamID_list)):
            result.append("contains the same Authorization's teamID")

    return result


def check_contradictory_value_for_initialization(json_date):
    result = []

    # ------ element ------ #
    # check for types and ranges

    key_names = ['id', 'intervalMillis', 'turnMillis', 'turns', 'startedAtUnixTime', 'height', 'width']
    range_of_values = [(0, 10**9), (0, 10**4), (0, 10**5), (1, 60), (0, 10**4), (1, 20), (1, 20)]
    key_names_and_range_of_values = list(zip(key_names, range_of_values))

    for key_name_and_range_of_value in key_names_and_range_of_values:
        key_name = key_name_and_range_of_value[0]
        lower_limit = key_name_and_range_of_value[1][0]
        upper_limit = key_name_and_range_of_value[1][1]
        value = json_date[key_name]
        if not type(value) is int:
            result.append(key_name + " must be int")
        elif not lower_limit <= value <= upper_limit:
            result.append(key_name + " must be from " + str(lower_limit) + " to " + str(upper_limit) + " inclusive")

    if result:
        result = list(set(result))
        return result

    # ------ list ------ #
    # check for types and ranges

    height = json_date['height']
    width = json_date['width']

    key_names = ['points']
    range_of_values = [(-10**9, 10**9)]
    key_names_and_range_of_values = list(zip(key_names, range_of_values))

    for key_name_and_range_of_value in key_names_and_range_of_values:
        key_name = key_name_and_range_of_value[0]
        lower_limit = key_name_and_range_of_value[1][0]
        upper_limit = key_name_and_range_of_value[1][1]
        value = json_date[key_name]
        tmp_result = []
        if len(value) != height:
            tmp_result.append(key_name + " height must be the as 'height'")
        else:
            for line in value:
                if len(line) != width:
                    tmp_result.append(key_name + " width must be the as 'width'")

        if tmp_result:
            tmp_result = set(tmp_result)
            for R in tmp_result:
                result.append(R)
        else:
            for line in value:
                for elem in line:
                    if not type(elem) is int:
                        tmp_result.append(key_name + " must be int")
                    if not lower_limit <= elem <= upper_limit:
                        tmp_result.append(key_name + " must be from " + str(lower_limit) + " to " + str(upper_limit) + " inclusive")
            if tmp_result:
                tmp_result = set(tmp_result)
                for R in tmp_result:
                    result.append(R)

    # ------ teams ------ #
    # check for types and ranges and duplicates

    teams = json_date['teams']

    if len(teams) != 2:
        result.append("team must be two")
    else:
        tmp_result = []
        for team in teams:
            teamID = team['teamID']
            teamName = team['teamName']
            if not type(teamID) is int:
                tmp_result.append("teamID must be int")
            if not type(teamName) is str:
                tmp_result.append("teamName must be str")
            if not 0 <= teamID <= 10**5:
                tmp_result.append("teamID must be from 0 to 10^5 inclusive")
            if not 0 < len(teamName) <= 100:
                tmp_result.append("teamName length must be from 1 to 100 inclusive")

            agents = team['agents']

            for agent in agents:
                key_names = ['agentID', 'y', 'x']
                range_of_values = [(1, 10**5), (1, height), (0, width)]
                key_names_and_range_of_values = list(zip(key_names, range_of_values))
                for key_name_and_range_of_value in key_names_and_range_of_values:
                    key_name = key_name_and_range_of_value[0]
                    lower_limit = key_name_and_range_of_value[1][0]
                    upper_limit = key_name_and_range_of_value[1][1]
                    value = agent[key_name]
                    if not type(value) is int:
                        result.append(key_name + " must be int")
                    elif not lower_limit <= value <= upper_limit:
                        result.append(
                            key_name + " must be from " + str(lower_limit) + " to " + str(upper_limit) + " inclusive")

        if tmp_result:
            tmp_result = set(tmp_result)
            for R in tmp_result:
                result.append(R)
        else:
            teamID_list = []
            teamName_list = []
            agentID_list = []
            agent_location_list = []
            for team in teams:
                teamID_list.append(team['teamID'])
                teamName_list.append(team['teamName'])
                agents = team['agents']
                for agent in agents:
                    agentID_list.append(agent['agentID'])
                    agent_location_list.append((agent['y'], agent['x']))

            if len(teamName_list) != len(set(teamName_list)):
                result.append("The two team Names are the same")
            if len(agentID_list) != len(set(agentID_list)):
                result.append("contains the same agentID")
            if len(agent_location_list) != len(set(agent_location_list)):
                result.append("contains the same agent location")

            if len(teamID_list) != len(set(teamID_list)):
                result.append("contains the same teamID")
            else:
                A_teamID_list = []
                Authorizations_info = json_date['Authorization']
                for A_info in Authorizations_info:
                    A_teamID_list.append(A_info['teamID'])
                if set(teamID_list) != set(A_teamID_list):
                    result.append("Authorization has a different teamID than teams")

    result = list(set(result))
    return result


def make_up_for_wanting_value(json_date):
    hgoe = 0


# def various_delete(match_id):
#     path = "./matchID:" + str(match_id) + "___field_information.json"
#     if os.path.isfile(path):
#         os.remove(path)


def make_up_for_dependent_info(json_date):
    # tilePoint, areaPointもやろうね
    height = json_date['height']
    width = json_date['width']
    tiled = [[0]*width]*height

    for team in json_date['teams']:
        teamID = team['teamID']
        for agent in team['agents']:
            y = agent['y'] - 1
            x = agent['x'] - 1
            tiled[y][x] = teamID
    json_date['tiled'] = tiled


def write_game_info(json_date):
    result_json = {}
    keys = ['id', 'intervalMillis', 'turnMillis', 'turns', 'startedAtUnixTime', 'height', 'width', 'points', 'tiled']
    for key in keys:
        result_json[key] = json_date[key]
    result_json['turn'] = 0

    result_teams = []

    for team in json_date['teams']:
        result_team = {}
        team_keys = ['teamID', 'teamName', 'tilePoint', 'areaPoint']
        for key in team_keys:
            result_team[key] = team[key]

        result_agents = []
        for agent in team['agents']:
            result_agent = {}
            result_agent['agentID'] = agent['agentID']
            result_agent['y'] = agent['y']
            result_agent['x'] = agent['x']
            result_agents.append(result_agent)
        result_team['agents'] = result_agents
        result_teams.append(result_team)
    result_json['teams'] = result_teams

    result_json = json.loads(json.dumps(result_json))

    result_json['actions'] = []

    path = "./json/" + str(json_date['id']) + "th_field_info.json"

    with open(path, mode='w') as f:
        json.dump(result_json, f, indent=2)


def append_to_authorization(json_date):

    return 0


