import json
from requests import Session
from services.writer import Writer

BASE_URL = ' https://www.upphandlingsmyndigheten.se'
PATH = '/api/sv/statisticsservice/bridgeapi/statistics'
URL = BASE_URL + PATH

def download():
    s = Session()
    areas = s.get(URL).json()['areas']

    areas_extract = []

    for area in areas:
        print(f"Area: {area['value']}")
        params = __create_params(area)

        response = s.get(URL, params=params)
        products = response.json()['products']

        products_extract = []

        for product in products:
            print(f"  Product: {product['value']}")
            params = __create_params(area, product)

            response = s.get(URL, params=params)
            units = response.json()['units']

            units_extract = []

            for unit in units:
                print(f"    Unit: {unit['value']}")
                params = __create_params(area, product, unit)

                response = s.get(URL, params=params)
                distributed_units = response.json()['distributedUnits']

                distributed_units_extract = []

                for distributed_unit in distributed_units:
                    print(f"      Distributed unit: {distributed_unit['value']}")
                    params = __create_params(area, product, unit, distributed_unit)

                    response = s.get(URL, params=params)
                    # print(response.url)
                    measurements = response.json()['measurements']
                    __clean_parameters(measurements)
                    cleaned_parameters = response.json()['parameters']
                    __clean_parameters(cleaned_parameters)

                    distributed_units_extract.append({
                        'distributedUnit': distributed_unit['value'],
                        'measurements': measurements,
                        'parameters': cleaned_parameters
                    })

                units_extract.append({
                    'unit': unit['value'],
                    'distributedUnits': distributed_units_extract
                })

            products_extract.append({
                'product': product['value'],
                'units': units_extract,
            })

        areas_extract.append({
            'area': area['value'],
            'products': products_extract,
        })

    return areas_extract

def save(filepath='all_parameters.json'):
    Writer.write_json(download(), filepath)

def get_from_file(filepath='all_parameters.json'):
        try:
            file = open(filepath)
        except FileNotFoundError:
            return []

        return json.load(file)

def get(filepath):
    parameters = get_from_file(filepath)

    if not parameters:
        save(filepath)
        parameters = get_from_file(filepath)

    return parameters

def get_request_for(distributed_unit, year=2021, measurement='SUM', dimensions=[], filepath='all_parameters.json'):
    all_parameters = get(filepath)

    request = {
        'year': year,
        'resultFormat': 'table',
        'chartStacked': 'false',
        'chartType': 'column',
        'timefragment': 'Tidsperiod.År',
        'fetch': 20
        }

    for area in all_parameters:
        request['area'] = area['area']
        for product in area['products']:
            request['product'] = product['product']
            for unit in product['units']:
                request['unit'] = unit['unit']
                for distributed in unit['distributedUnits']:
                    request['distributedUnit'] = distributed['distributedUnit']

                    if distributed['distributedUnit'] == distributed_unit:
                        request['measurement'] = measurement

                        request['param'] = []
                        for parameter in distributed['parameters']:
                            for dimension in parameter['dimensions']:
                                if not dimensions or dimension['heading'] in dimensions:
                                    for property in dimension['properties']:
                                        request['param'].append(property['value'])
                                        request['orderBy'] = request['param'][0]
                        print((f"Found parameters for distributed unit: {distributed_unit}:\n"
                        f"- Area: {request['area']}\n"
                        f"  - Product: {request['product']}\n"
                        f"    - Unit: {request['unit']}"))
                        return request

def __create_params(area=None, product=None, unit=None, distributed_unit=None, measurement=None, variable=None):
    params = {}

    if area:
        params['area'] = area['value']
    if product:
        params['product'] = product['value']
    if unit:
        params['unit'] = unit['value']
    if distributed_unit:
        params['distributedUnit'] = distributed_unit['value']
    if measurement:
        params['measurement'] = measurement['value']
    if variable:
        params['variable'] = variable['value']

    return params

def __clean_parameters(parameters):
    for parameter in parameters:
        parameter.pop('id', None)
        parameter.pop('disabled', None)

        if 'dimensions' in parameter:
            subparameters = parameter['dimensions']
        elif 'properties' in parameter:
            subparameters = parameter['properties']
        else:
            subparameters = None

        if subparameters:
            __clean_parameters(subparameters)

            parameter.pop('description', None)
        else:
            parameter.pop('text', None)

