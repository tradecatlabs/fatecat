#!flask/bin/python
from flask import Flask, jsonify, make_response, abort, request
from wuxingData import wuxingDic
import main
import characters
import metaphysic
import readDic

app = Flask(__name__)


@app.route('/api/characters/gender/<gender>', methods=['GET'])
def get_ordinary_characters(gender):
    if gender == 'male':
        return jsonify(characters.male)
    elif gender == 'female':
        return jsonify(characters.female)
    else:
        abort(404)


@app.route('/api/characters/wuxing/<wuxing>', methods=['GET'])
def get_wuxing_characters(wuxing):
    if wuxing not in wuxingDic.keys():
        abort(404)
    return jsonify(wuxingDic.get(wuxing))


@app.route('/api/metaphysic', methods=['POST'])
def get_metaphysic_info():
    if not request.json or not 'year' in request.json or not 'month' in request.json or not 'day' in request.json or not 'hour' in request.json:
        abort(400)
    birthInfo = {
        'year': int(request.json['year']),
        'month': int(request.json['month']),
        'day': int(request.json['day']),
        'hour': int(request.json['hour'])
    }
    shenchenbazi = metaphysic.getShenChenBaZi(
        birthInfo['year'], birthInfo['month'], birthInfo['day'],
        birthInfo['hour'])
    wuxing = metaphysic.getWuXing(shenchenbazi)
    metaphysicInfo = {'shenchenbazi': shenchenbazi, 'wuxing': wuxing}
    return jsonify(metaphysicInfo)


@app.route('/api/imagery', methods=['POST'])
def get_imagery_info():
    if not request.json:
        abort(400)
    searchText = request.json["text"]
    relatedCharactersDic = readDic.main(searchText)
    return jsonify(relatedCharactersDic)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.debug = True
    app.run()