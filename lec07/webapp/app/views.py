import json

import flask
from flask import render_template, request, jsonify
from app import application
from bandit import StateRepository, BerTSAgent, Arm, Response
from dataclasses import asdict



import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)



@application.route('/')
@application.route('/contextual')
def contextual():
    return render_template('contextual_bandit.html')

@application.route('/api/user_response', methods=['POST'])
def user_response():

    if request.is_json:
        data = request.get_json()
        user_responses = []

        for ur in data['responses']:
            arm = Arm(ur['arm']['color'], ur['arm']['theme'])
            response = Response(arm, ur['reward'])
            user_responses.append(response)

        repo = StateRepository(user_responses)
        agent = BerTSAgent()
        arm = agent.get_arm(repo.counts, repo.cum_rewards)

        ret = {}
        ret['arm'] = asdict(arm)
        ret['past_responses'] = data['responses']
        return jsonify(ret)


    return jsonify({'data': None})
