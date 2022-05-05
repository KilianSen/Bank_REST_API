from flask import Flask, jsonify, request
from BankSys import Bank


app = Flask('RESTBank')
bank = Bank('RESTBank')


@app.route('/')
def index():
    with open('index.html', 'r') as o:
        t = o.read()
    return t


@app.route('/map')
def mapf():
    rls: {str, [str]} = {}
    for r in list(reversed([rule for rule in app.url_map.iter_rules()]))[1::]:
        for m in r.methods:
            if m not in rls:
                rls[m] = []
            rls[m].append(str(r))
    print(rls)
    return jsonify(rls)


@app.route('/accounts')
def accounts():
    return jsonify(list(bank.accounts))


@app.route('/account', methods=['GET'])
def acc_get():
    return jsonify(bank.account(request.args['uuid']).toDict())


@app.route('/account', methods=['POST'])
def acc_create():
    return jsonify(bank.account_create(request.args['name']))


@app.route('/transactions')
def transactions():
    return jsonify(list(bank.transactions))


@app.route('/transaction', methods=['GET'])
def trans_get():
    return jsonify(bank.transaction(request.args['uuid']).toDict())


@app.route('/transactions', methods=['POST'])
def trans_create():
    return jsonify(bank.transaction_create(request.args['origin'],
                                           request.args['destination'],
                                           float(request.args['value'])))


app.run()
pass
