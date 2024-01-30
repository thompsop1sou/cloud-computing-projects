import requests
import json
import os

class ExerciseAPI:

    def __init__(self):
        # Variables for accessing API
        self.api_key = os.getenv('EXERCISE_API_KEY')
        self.base_url = 'https://api.api-ninjas.com/v1/exercises'
        # Variables for filling out drop down menus in workout view
        self.types = ['cardio', 'olympic_weightlifting', 'plyometrics',
             'powerlifting', 'strength', 'stretching', 'strongman']
        self.muscles = ['abdominals', 'abductors', 'adductors', 'biceps',
               'calves', 'chest', 'forearms', 'glutes',
               'hamstrings', 'lats', 'lower_back', 'middle_back',
               'neck', 'quadriceps', 'traps', 'triceps']
        self.difficulties = ['beginner', 'intermediate', 'expert']

    def call(self, api_params, max_offset=1, include_instr = False):
        """
        Function makes a call using api_params to Exercises API by API Ninjas

        :param api_params: dictionary
        :param max_offset: int (determines how many results to include)
        :param include_instr: bool (if True, include exercise instructions in results)
        :return: list of dictionaries
        """
        # Create the URL with the appropriate parameters
        api_url = self.base_url
        if api_url[-1] != '?':
            api_url = api_url + '?'
        for key, value in api_params.items():
            api_url = api_url + key + '=' + value + '&'
        api_url = api_url[:-1]
        # Loop and continue to get results from the API until too many errors or have reached max_offset
        results = []
        errors = 0
        offset = 0
        while offset < max_offset:
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
        # Return the results
        return results
