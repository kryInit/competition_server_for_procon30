import common
import json
import os
import random
import time


def initialize_game_info(json_data):
    result = check_all_error_factor(json_data)
    if result:
        return result

    json_data['startedAtUnixTime'] += int(time.time())
    make_up_for_dependent_info(json_data)
    write_game_info(json_data)
    append_to_authorization(json_data)
    result = "initialization was executed"

    return result


def check_all_error_factor(json_data):
    result = check_if_necessary_key_existing(json_data)
    if result:
        return result

    result = check_if_it_has_already_been_initialized(json_data['id'])
    if result:
        return result

    result = check_value_of_authorization(json_data)
    if result:
        return result

    make_up_for_wanting_value(json_data)

    result = check_contradictory_value_for_initialization(json_data)
    if result:
        return result

    return ""


def check_if_necessary_key_existing(json_data):
    result = []
    if 'id' not in json_data:
        result.append("no id")
    if 'Authorization' not in json_data:
        result.append("no Authorization")
    else:
        authorizations = json_data['Authorization']
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
    result = ""
    path = "./json/" + str(match_id) + "th_field_info.json"
    if os.path.isfile(path):
        with open(path, 'r') as f:
            json_data = json.load(f)
        if json_data['turns'] == ['turn']:
            common.kill_game(match_id)
        else:
            result = "A match with matchID:" + str(match_id) + " already exists"

    return result


def check_value_of_authorization(json_data):
    result = []
    for Authorization in json_data['Authorization']:
        token = Authorization['token']
        team_id = Authorization['teamID']
        if not type(token) is str:
            result.append("token must be str")
        if not type(team_id) is int:
            result.append("Authorization's teamID must be str")
        if not 0 < len(token) <= 10 ** 5:
            result.append("token length must be from 1 to 10^5 inclusive")
        if not 0 < team_id <= 10 ** 5:
            result.append("Authorization's teamID must be from 1 to 10^5 inclusive")

    if not result:
        token_list = []
        team_id_list = []
        for Authorization in json_data['Authorization']:
            token_list.append(Authorization['token'])
            team_id_list.append(Authorization['teamID'])

        if len(token_list) != len(set(token_list)):
            result.append("contains the same token")
        if len(team_id_list) != len(set(team_id_list)):
            result.append("contains the same Authorization's teamID")

    return result


def check_contradictory_value_for_initialization(json_data):
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
        value = json_data[key_name]
        if not type(value) is int:
            result.append(key_name + " must be int")
        elif not lower_limit <= value <= upper_limit:
            result.append(key_name + " must be from " + str(lower_limit) + " to " + str(upper_limit) + " inclusive")

    if result:
        result = list(set(result))
        return result

    # ------ list ------ #
    # check for types and ranges

    height = json_data['height']
    width = json_data['width']

    key_names = ['points']
    range_of_values = [(-10**9, 10**9)]
    key_names_and_range_of_values = list(zip(key_names, range_of_values))

    for key_name_and_range_of_value in key_names_and_range_of_values:
        key_name = key_name_and_range_of_value[0]
        lower_limit = key_name_and_range_of_value[1][0]
        upper_limit = key_name_and_range_of_value[1][1]
        value = json_data[key_name]
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

    teams = json_data['teams']

    if len(teams) != 2:
        result.append("team must be two")
    else:
        tmp_result = []
        for team in teams:
            team_id = team['teamID']
            team_name = team['teamName']
            if not type(team_id) is int:
                tmp_result.append("teamID must be int")
            if not type(team_name) is str:
                tmp_result.append("teamName must be str")
            if not 0 <= team_id <= 10**5:
                tmp_result.append("teamID must be from 0 to 10^5 inclusive")
            if not 0 < len(team_name) <= 100:
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
            team_id_list = []
            team_name_list = []
            agent_id_list = []
            agent_location_list = []
            for team in teams:
                team_id_list.append(team['teamID'])
                team_name_list.append(team['teamName'])
                agents = team['agents']
                for agent in agents:
                    agent_id_list.append(agent['agentID'])
                    agent_location_list.append((agent['y'], agent['x']))

            if len(team_name_list) != len(set(team_name_list)):
                result.append("The two team Names are the same")
            if len(agent_id_list) != len(set(agent_id_list)):
                result.append("contains the same agentID")
            if len(agent_location_list) != len(set(agent_location_list)):
                result.append("contains the same agent location")

            if len(team_id_list) != len(set(team_id_list)):
                result.append("contains the same teamID")
            else:
                a_team_id_list = []
                authorizations_info = json_data['Authorization']
                for a_info in authorizations_info:
                    a_team_id_list.append(a_info['teamID'])
                if set(team_id_list) != set(a_team_id_list):
                    result.append("Authorization has a different teamID than teams")

    result = list(set(result))
    return result


def make_up_for_wanting_value(json_data):
    pass


def make_up_for_dependent_info(json_data):
    # tilePoint, areaPointもやろうね
    height = json_data['height']
    width = json_data['width']
    tiled = [[0] * width for i in range(height)]

    for team in json_data['teams']:
        team_id = team['teamID']
        for agent in team['agents']:
            y = agent['y'] - 1
            x = agent['x'] - 1
            tiled[y][x] = team_id
    json_data['tiled'] = tiled


def write_game_info(json_data):
    result_json = {}
    keys = ['id', 'intervalMillis', 'turnMillis', 'turns', 'startedAtUnixTime', 'height', 'width', 'points', 'tiled']
    for key in keys:
        result_json[key] = json_data[key]
    result_json['turn'] = 0

    result_teams = []

    for team in json_data['teams']:
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

    path = "./json/" + str(json_data['id']) + "th_field_info.json"

    with open(path, mode='w') as f:
        json.dump(result_json, f, indent=2)


def append_to_authorization(json_data):
    path = "./json/Authorization.json"
    auth_info = {}
    if os.path.isfile(path):
        with open(path, 'r') as f:
            auth_info = json.load(f)
        os.remove(path)

    match_id = json_data['id']

    for items in json_data['Authorization']:
        token = items['token']
        team_id = items['teamID']

        ids = {'matchID': match_id, 'teamID': team_id}

        if token in auth_info:
            auth_info[token].append(ids)
        else:
            auth_info[token] = [ids]

    auth_info = json.loads(json.dumps(auth_info))

    with open(path, mode='w') as f:
        json.dump(auth_info, f, indent=2)




