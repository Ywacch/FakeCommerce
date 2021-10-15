import json
from backend.database import Database

db = Database()
html_path = "../frontend/index.html"


def url_handler(headers):
    top_header = headers[0]
    methods = top_header.split()
    if methods[0] == 'GET':
        return get_handler(methods[1])
    elif methods[0] == 'POST':
        post_data = headers[-1]
        return post_handler(methods[1], post_data)
    elif methods[0] == 'DELETE':
        return delete_handler(methods[1])


def get_handler(url_params):
    print("processing get req")
    url_params = url_params.split('/')
    response_data = {'response_content': '', 'response_status': None}
    if len(url_params) == 2:
        if url_params[1] == 'posts':  # get all posts
            items = db.get_all_items()
            response_data['response_content'] = json.dumps(items).encode('utf-8')
            response_data['response_status'] = '200 OK'
        else:  # go to home page
            index_html = open(html_path, 'rb')
            html = index_html.read()
            index_html.close()

            response_data['response_content'] = html
            response_data['response_status'] = '200 OK'

    elif len(url_params) == 3:  # get post according to id
        post_id = url_params[2]
        item = db.get_item(post_id)
        response_data['response_content'] = json.dumps(item).encode('utf-8')
        response_data['response_status'] = '200 OK'
    else:
        pass  # error
    return response_data


def post_handler(url_params, post_data):
    response_data = {'response_content': '', 'response_status': None}
    print("processing post req")
    url_params = url_params.split('/')
    if len(url_params) == 2:
        item = json.loads(post_data)
        if item['username'] and item['title'] and item['description']:
            db.add_item(item['username'], item['title'], item['description'])
            response_data['response_status'] = '200 OK'
        else:
            response_data['response_status'] = '400 Bad Request'
    else:
        pass  # error

    return response_data


def delete_handler(url_params):
    response_data = {'response_content': '', 'response_status': None}
    print("processing delete req")
    url_params = url_params.split('/')
    if len(url_params) == 3:  # delete post from store
        post_id = url_params[2]
        if db.get_item(post_id) is None:
            response_data['response_status'] = '400 Bad Request'
        else:
            db.delete_item(post_id)
            response_data['response_status'] = '200 OK'
    else:
        pass  # error
    return response_data