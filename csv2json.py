import csv
import json
from util import fix_category

def get_row_as_key_value(p):
    return {
        'uid'       : p[0],
        'product_id': p[1],
        'category'  : p[2],
        'title'     : p[3],
        'size'      : p[4],
        'price'     : p[5],
        'calorie'   : p[6],
        'desc'      : p[7],
        'url'       : p[8],
        'image'     : p[9],
    }

def main(store_name):
    csv_path = './' + store_name + '/menu.csv'
    export_json_path = './' + store_name + '/menu.json'
    counter = 0
    result = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        prev = {'product_id': '0'}
        for row in reader:
            counter += 1
            if counter == 1:
                continue
            row = get_row_as_key_value(row)
            product_id = row['product_id']
            if prev['product_id'] == row['product_id']:
                result[-1]['size'].append({
                    'name': row['size'],
                    'price': row['price'],
                    'calorie': row['calorie'],
                })
            else:
                result.append({
                    'product_id': int(product_id),
                    'category': row['category'],
                    'common_category': fix_category(store_name, row['category']),
                    'title': row['title'],
                    'desc': row['desc'],
                    'url': row['url'],
                    'image': row['image'],
                    'size': [
                        {
                            'name': row['size'],
                            'price': row['price'],
                            'calorie': row['calorie'],
                        }
                    ]
                })
                
            prev = row
        pass
    with open(export_json_path, 'w') as f:
        f.write(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main('matsuya')
    main('sukiya')
    main('yoshinoya')