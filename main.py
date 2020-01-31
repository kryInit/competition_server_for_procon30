import common
import matches
import matches_matchID
import update_actions as update
import initialization as init
import transition as trans
import json
import os
import time
import schedule
from flask import *
from threading import Thread

app = Flask(__name__)  # インスタンス生成


@app.route('/initialization', methods=["POST"])
def initialization():
    print("\nnow initializing...\n")

    json_data = request.get_json()
    result_message = init.initialize_game_info(json_data)

    print("result message = " + str(result_message))

    print("\nfinished initialization!\n")

    dict_for_json_result = {'result': result_message}

    result_json = json.loads(json.dumps(dict_for_json_result))

    return str(json.dumps(result_json)) + "\n"


@app.route('/matches')
def pre_game_info():
    print("\nnow making pre-game info...\n")

    result_message = matches.make_pre_game_info(request.headers)

    print("result message = " + str(result_message))

    print("\nfinished making pre-game info!\n")

    return str(result_message) + "\n"


@app.route('/matches/<match_id>')
def game_state_info(match_id):
    print("\nnow making game state info\n")

    result_json = matches_matchID.make_game_state_info(int(match_id), request.headers)

    print("result massage = " + str(result_json))

    print("\nfinished making game state info!\n")

    return str(json.dumps(result_json)) + "\n"


@app.route('/matches/<match_id>/action', methods=["POST"])
def update_actions(match_id):
    print("\nnow updating actions...\n")

    json_data = request.get_json()
    result_json = update.update_action(json_data, match_id, request.headers)

    print("result massage = " + str(result_json))

    print("\nfinished updating actions!\n")

    return str(json.dumps(result_json)) + "\n"


@app.route('/matches/<match_id>/delete')
def delete_game(match_id):
    print("\nnow deleting " + str(match_id) + "th game ...\n")

    is_ok = True
    cnt = 0
    a_path = "./json/Authorization.json"
    tokens = request.headers['Authorization'].split(',')
    if not os.path.isfile(a_path):
        result_json = {'result': "Authorization does not exist"}
        print("result_massage = " + str(result_json))
        print("\nfinished deleting " + str(match_id) + "th game!\n")
        return str(json.dumps(result_json)) + "\n"

    with open(a_path, 'r') as f:
        auth = json.load(f)

    for token, _matches in auth.items():
        for match in _matches:
            if str(match['matchID']) == str(match_id):
                cnt += 1
                if token not in tokens:
                    is_ok = False

    if cnt < 2:
        result_json = {'result': str(match_id) + "th game does not exist"}
    elif is_ok:
        common.kill_game(match_id)
        result_json = {'result': str(match_id) + "th game was deleted"}
    else:
        result_json = {'result': str(match_id) + "th game can't be deleted"}

    print("result_massage = " + str(result_json))

    print("\nfinished deleting " + str(match_id) + "th game!\n")

    return str(json.dumps(result_json)) + "\n"


@app.route('/ping')
def ping():
    if 'Authorization' not in request.headers:
        return json.loads(json.dumps({'status': 'InvalidToken'}))

    a_path = "./json/Authorization.json"
    token = request.headers['Authorization']

    if not os.path.isfile(a_path):
        return json.loads(json.dumps({'status': 'InvalidToken'}))

    with open(a_path, 'r') as f:
        auth_info = json.load(f)
    if token not in auth_info:
        return json.loads(json.dumps({'status': 'InvalidToken'}))

    return str((json.dumps({'status': 'OK'}))) + "\n"


run_flag = True


def run_schedule():
    while run_flag:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    schedule.every(1).seconds.do(trans.transition)
    Thread(target=run_schedule).start()

    common.remove_all_json_file()

    app.run(host='localhost', port=8000)

    common.remove_all_json_file()
    run_flag = False

