import common
import initialization as init
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

    s = request.get_json()
    result_massage = init.initialize_game_info(s)

    print("result massage = " + str(result_massage))

    print("\nfinished initialization!\n")

    dict_for_json_result = {'result': result_massage}

    json_result = json.loads(json.dumps(dict_for_json_result))

    return json.dumps(json_result, indent=2)


@app.route('/matches')
def return_list_of_matches():
    hogehoge = 0
    return hogehoge


@app.route('/matches/<matchID>')
def return_match_info(matchID):
    return matchID


@app.route('/matches/<matchID>/action', methods=["POST"])
def update_actions(matchID):
    return matchID


@app.route('/ping')
def ping():
    hoge = request.headers

    return str(hoge)


def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    # tmp = field_information()
    # schedule.every(1).seconds.do(tmp.hogehoge)
    # Thread(target=run_schedule).start()

    app.run(host='localhost', port=8000)

