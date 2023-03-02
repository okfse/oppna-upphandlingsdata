import json


class Writer(object):
    @staticmethod
    def write_json(dict, filename):
        with open(filename, 'w') as fp:
            json_string = json.dumps(dict, ensure_ascii=False,
                                     indent=4).encode('utf-8')
            fp.write(json_string.decode())

    @staticmethod
    def write_file(content, filename):
        with open(filename, 'wb') as f:
            f.write(content)
