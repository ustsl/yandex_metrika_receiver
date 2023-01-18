import time
import requests

from abc import ABC


class YandexMetrikaSettings(ABC):

    def __init__(self):
        self._settings = {}
        self._params = {}
        self._headers = {}
        self._checkup = False
        self.data = []

    @property
    def settings(self):
        counter = self._settings.get('counter')
        token = self._settings.get('token')
        params = self._settings.get('params')
        if not counter:
            return 'Need dict key - counter'
        if not token:
            return 'Need dict key - token'
        if not params:
            return 'Need dict key - params'
        return self._set_params(counter=counter, params=params, token=token)

    @settings.setter
    def settings(self, settings):
        self._settings = settings

    def _set_params(self, counter=None, params=None, token=None):

        self._headers = {'Authorization': 'OAuth ' + token}
        dates = params.get('date')
        preset = params.get('preset')

        if not dates or len(dates) != 2:
            return 'Need dates list (start, end)'
        if not preset:
            return 'Need preset list (dimension, metrics)'
        else:
            self._checkup = True
            self._params = {
                'date1': dates[0],
                'date2': dates[1],
                'id': counter,
                'offset': 0,
                'limit': 0,
                'accuracy': 'full',
                'dimensions': preset[0],
                'metrics': preset[1],
                'filters': params.get('filters')}
            return self._params

    def __str__ (self):
        return str(self._settings)

class YandexMetrikaReceiver(YandexMetrikaSettings):

    _API_URL = 'https://api-metrika.yandex.ru/stat/v1/data'

    def _request_method(self, offset, n_rows):

        # Функция запроса
        self._params['offset'] = offset
        self._params['limit'] = n_rows
        r = requests.get(YandexMetrikaReceiver._API_URL,
                         params=self._params, headers=self._headers)
        self.json = r.json()
        print(r)

    def receive(self, n_rows=100, time_pause=1):

        offset = 1
        timer = 1
        cycle = True

        if self._checkup == False:
            return 'Settings Error'

        while cycle == True:

            # Получаем данные в цикле
            self._request_method(offset, n_rows)
            dataset = self.json

            if 'data' in dataset.keys():
                self.data += dataset['data']
            else:
                print(dataset)
                self.data = 'error'
                break

            if 'errors' in dataset.keys():
                print(dataset)
                self.data = 'error'
                break

            timer += 1

            if timer / 10 == int(timer / 10):
                print('Finished step - {}, next row - {}'
                      .format(timer, offset))

            time.sleep(time_pause)

            offset += n_rows

            if len(dataset['data']) == 0:
                cycle = False
                break

        return self.data
