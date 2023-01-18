dimensions = ['ym:s:startOfMonth', 'ym:s:firstVisitDate']
metrics = ['ym:s:visits', 'ym:s:pageDepth', 'ym:s:avgVisitDurationSeconds']
date = ['2023-01-01', '2023-01-02']
preset = [dimensions, metrics]
params = {'date': date, 'preset': preset, 'filters': None}
token = '**_***********************************************************'
counter = '********'

ymr = YandexMetrikaReceiver()
ymr.settings = {'counter': counter, 'token': token, 'params': params}
ymr.receive()