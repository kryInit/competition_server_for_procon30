import os
import json
import glob


def kill_game(match_id):
    # Authorization関係もちゃんと処理する
    path = "./json/" + str(match_id) + "th_field_info.json"
    os.remove(path)


def check_authorization(rqh):
    it = json.loads(json.dumps({'status': 'InvalidToken'}))
    if 'Authorization' not in rqh:
        return it

    a_path = "./json/Authorization.json"
    token = rqh['Authorization']

    if not os.path.isfile(a_path):
        return it

    with open(a_path, 'r') as f:
        auth_info = json.load(f)
    if token not in auth_info:
        return it

    return {}


def remove_all_json_file():
    for p in glob.glob("./json/*.json"):
        if os.path.isfile(p):
            os.remove(p)
