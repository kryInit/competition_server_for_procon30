import common
import os
import json


def make_pre_game_info(rqh):
    result = common.check_authorization(rqh)
    if result:
        return result

    a_path = "./json/Authorization.json"
    token = rqh['Authorization']

    with open(a_path, 'r') as f:
        auth_info = json.load(f)

    result = []
    idss = auth_info[token]
    for ids in idss:
        tmp_result = {}
        keys = ['id', 'intervalMillis', 'turnMillis', 'turns']
        match_id = ids['matchID']
        team_id = ids['teamID']
        f_path = "./json/" + str(match_id) + "th_field_info.json"
        with open(f_path, 'r') as f:
            field_info = json.load(f)
        for key in keys:
            tmp_result[key] = field_info[key]
        tmp_result['teamID'] = team_id

        for team in field_info['teams']:
            if team['teamID'] != team_id:
                tmp_result['matchTo'] = team['teamName']
        result.append(tmp_result)

    result = json.dumps(result)

    return result
