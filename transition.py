import common
import copy
import json
import time
import os


def transition():
    target_match_ids = create_set_of_target_match_ids()

    for match_id in target_match_ids:
        team_ids = create_team_ids(match_id)
        actions = create_actions(match_id, team_ids)
        add_apply(actions)
        update_field_info(match_id, actions)
        delete_file(match_id, team_ids)


def create_set_of_target_match_ids():
    a_path = "./json/Authorization.json"
    all_match_ids = set()
    target_match_ids = set()

    if not os.path.isfile(a_path):
        return set()

    with open(a_path, 'r') as f:
        auth_info = json.load(f)

    for matches in auth_info.values():
        for match in matches:
            all_match_ids.add(match['matchID'])

    for match_id in all_match_ids:
        f_path = "./json/" + str(match_id) + "th_field_info.json"

        with open(f_path, 'r') as f:
            field_info = json.load(f)
        saut = field_info['startedAtUnixTime']
        ims = field_info['intervalMillis']
        tms = field_info['turnMillis']
        turns = field_info['turns']
        turn = field_info['turn']
        if (time.time()-saut)/((tms+ims)/1000) <= turns and time.time()-saut > (tms+ims)/1000*turn+tms/1000:
            target_match_ids.add(match_id)

        if ((time.time()-saut) - (tms+ims/1000*turns)) >= 3600:
            common.kill_game(match_id)
            # ついでに終わってから結構時間が経ったもの(1時間後にした)は消しておく

    return target_match_ids


def create_team_ids(match_id):

    f_path = "./json/" + str(match_id) + "th_field_info.json"
    with open(f_path, 'r') as f:
        field_info = json.load(f)

    teams = field_info['teams']

    result = (teams[0]['teamID'], teams[1]['teamID'])

    return result


# [ {agentID, type, x, y, dx, dy, turn} ]が返される
def create_actions(match_id, team_ids):
    result = []
    tmp_dict = {}

    for i in range(2):
        tpath = "./json/" + str(match_id) + "-" + str(team_ids[i]) + "_tmp_actions_executed.json"
        if not os.path.isfile(tpath):
            continue

        with open(tpath, 'r') as f:
            tmp_actions = json.load(f)
        tmp_dict.update(tmp_actions)

    f_path = "./json/" + str(match_id) + "th_field_info.json"
    with open(f_path, 'r') as f:
        field_info = json.load(f)

    for team in field_info['teams']:
        for agent in team['agents']:
            agent_id = str(agent['agentID'])
            if agent_id in tmp_dict:
                tmp_dict[agent_id]['y'] = agent['y']
                tmp_dict[agent_id]['x'] = agent['x']

    for agent_id, other in tmp_dict.items():
        other['agentID'] = agent_id
        result.append(other)

    return result


def add_apply(actions):
    for action in actions:
        action['apply'] = 0
        if action['type'] == "stay":
            action['apply'] = 1

    finish = True
    while finish:
        finish = False
        targets = {}

        for action in actions:
            x = action['x']
            y = action['y']
            dx = action['dx']
            dy = action['dy']
            if action['apply']:
                if action['type'] == "move":
                    targets.setdefault((y+dy, x+dx), 0)
                    targets[(y+dy, x+dx)] += 1
                else:
                    targets.setdefault((y, x), 0)
                    targets[(y, x)] += 1
            else:
                targets.setdefault((y, x), 0)
                targets.setdefault((y+dy, x+dx), 0)
                targets[(y, x)] += 1
                targets[(y+dy, x+dx)] += 1

        for action in actions:
            if action['apply']:
                continue
            x = action['x']
            y = action['y']
            dx = action['dx']
            dy = action['dy']
            if targets[(y+dy, x+dx)] == 1:
                action['apply'] = 1
                finish = True

    for action in actions:
        del action['y'], action['x']


def update_field_info(match_id, actions):
    # tile, areapointを更新
    #
    f_path = "./json/" + str(match_id) + "th_field_info.json"
    with open(f_path, 'r') as f:
        field_info = json.load(f)

    id_actions = {}
    for action in actions:
        agent_id = action['agentID']
        type = action['type']
        dx = action['dx']
        dy = action['dy']
        apply = action['apply']
        id_actions[agent_id] = {"type": type, "dx": dx, "dy": dy, "apply": apply}

    for i in range(2):
        team = field_info['teams'][i]
        for j in range(len(team['agents'])):
            agent = team['agents'][j]
            agent_id = str(agent['agentID'])
            y = agent['y']
            x = agent['x']
            if agent_id in id_actions:
                if id_actions[agent_id]['apply']:
                    dx = id_actions[agent_id]['dx']
                    dy = id_actions[agent_id]['dy']
                    type = id_actions[agent_id]['type']
                    if type == "move":
                        y += dy
                        x += dx
                        field_info['tiled'][y-1][x-1] = team['teamID']
                    if type == "remove":
                        field_info['tiled'][y+dy-1][x+dx-1] = 0
            team['agents'][j]['y'] = y
            team['agents'][j]['x'] = x
        field_info['teams'][i] = team

    for action in actions:
        action['turn'] = field_info['turn']

    field_info['turn'] += 1

    for action in actions:
        field_info['actions'].append(action)

    with open(f_path, mode='w') as f:
        json.dump(field_info, f, indent=2)


def delete_file(match_id, team_ids):
    for team_id in team_ids:
        path = "./json/" + str(match_id) + "-" + str(team_id) + "_tmp_actions_executed.json"
        if os.path.isfile(path):
            os.remove(path)
