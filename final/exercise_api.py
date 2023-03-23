import requests
import json
import os

class ExerciseAPI:

    def __init__(self):
        self.api_key = os.getenv('EXERCISE_API_KEY')
        self.base_url = 'https://api.api-ninjas.com/v1/exercises'
        self.kinds = ['cardio', 'olympic_weightlifting', 'plyometrics',
             'powerlifting', 'strength', 'stretching', 'strongman']
        self.muscles = ['abdominals', 'abductors', 'adductors', 'biceps',
               'calves', 'chest', 'forearms', 'glutes',
               'hamstrings', 'lats', 'lower_back', 'middle_back',
               'neck', 'quadriceps', 'traps', 'triceps']
        self.difficulties = ['beginner', 'intermediate', 'expert']

    def call(self, api_params, include_instr = False):
        api_url = self.base_url
        if api_url[-1] != '?':
            api_url = api_url + '?'
        for key, value in api_params.items():
            api_url = api_url + key + '=' + value + '&'
        api_url = api_url[:-1]
        results = []
        errors = 0
        offset = 0
        while offset < 10:
            response = requests.get('{}&offset={}'.format(api_url, offset*10), headers={'X-Api-Key': self.api_key})
            if response.status_code == requests.codes.ok:
                errors = 0
                offset = offset + 1
                curr_results = json.loads(str(response.text))
                if len(curr_results) == 0:
                    break
                else:
                    if not include_instr:
                        for exercise in curr_results:
                            del exercise['instructions']
                    results.extend(curr_results)
            else:
                errors = errors + 1
                if errors < 10:
                    print("Error:", response.status_code, response.text)
                else:
                    break
        return results
