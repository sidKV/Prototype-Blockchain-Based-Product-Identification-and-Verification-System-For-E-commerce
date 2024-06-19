from flask import Flask, request, jsonify, render_template
import hashlib
import json
import datetime
import uuid

app = Flask(__name__)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash='0', product_info={})

    def create_block(self, previous_hash, product_info):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'product_info': product_info,
            'previous_hash': previous_hash,
            'unique_id': str(uuid.uuid4())
        }
        block['hash'] = self.hash(block)
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_block = block
            block_index += 1

        return True

    def add_block(self, product_info):
        previous_block = self.get_previous_block()
        previous_hash = previous_block['hash']
        return self.create_block(previous_hash, product_info)
    
    #def search_block(self, unique_id=None, serial_number=None):
      #  if unique_id:
        #    return [block for block in self.chain if block['unique_id'] == unique_id]
        #elif serial_number:
        #    return [block for block in self.chain if block['product_info']['serial_number'] == serial_number]
        #else:
         #   return None
        

    def search_block(self, unique_id=None, serial_number=None):
        if unique_id:
            return [block for block in self.chain if block.get('unique_id') == unique_id]
        elif serial_number:
            return [block for block in self.chain if block.get('product_info', {}).get('serial_number') == serial_number]
        else:
            return None

blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_block', methods=['POST'])
def add_block():
    serial_number = request.form['serial_number']
    brand = request.form['brand']
    type_ = request.form['type']
    cost = request.form['cost']
    is_sold = request.form['is_sold']
    manufacturer = request.form['manufacturer']
    date = request.form['date']

    product_info = {
        'serial_number': serial_number,
        'brand': brand,
        'type': type_,
        'cost': cost,
        'is_sold': is_sold,
        'manufacturer': manufacturer,
        'date': date
    }

    block = blockchain.add_block(product_info)
    response = {'message': 'Block added successfully', 'block': block}
    return jsonify(response), 201

@app.route('/search_block', methods=['GET'])
def search_block():
    unique_id = request.args.get('unique_id')
    serial_number = request.args.get('serial_number')

    if unique_id:
        results = blockchain.search_block(unique_id=unique_id)
    elif serial_number:
        results = blockchain.search_block(serial_number=serial_number)
    else:
        return jsonify({'error': 'Invalid search parameters'}), 400

    if results:
        return jsonify(results), 200
    else:
        return jsonify({'message': 'Block not found'}), 404

@app.route('/display_blockchain', methods=['GET'])
def display_blockchain():
    return jsonify(blockchain.chain), 200

if __name__ == '__main__':
    app.run(debug=True)
