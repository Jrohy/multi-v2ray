import json
from flask import Flask

from loader import Loader

app = Flask(__name__)

loader = Loader('test.dat', 'test.json')

group_list = loader.profile.group_list

@app.route('/list', methods=['GET'])
def node_list():
    return json.dumps(group_list, default=lambda x: x.__dict__, ensure_ascii=False)

if __name__ == '__main__':
    app.run(debug=True)