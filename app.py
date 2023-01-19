import json

from flask import Flask
from sqs_read import get_sqs_data, sqs_container_name, sqs_docker_image, sqs_docker_ports
from postgres_write import db_container_name, db_docker_image, db_docker_ports, write_to_postgres, get_table_as_string
from helper import delete_container, run_detached_container
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import HtmlFormatter


def setup():
    delete_container(sqs_container_name)
    sqs_container = run_detached_container(sqs_docker_image, sqs_container_name, sqs_docker_ports)
    delete_container(db_container_name)
    postgres_container = run_detached_container(db_docker_image, db_container_name, db_docker_ports)
    app.config['sqs_container'] = sqs_container
    app.config['postgres_container'] = postgres_container


app = Flask(__name__)
setup()


@app.route('/')
def run_api_seq():
    sqs_container = app.config['sqs_container']
    postgres_container = app.config['postgres_container']
    user_login_data = get_sqs_data(sqs_container)
    write_to_postgres(postgres_container, user_login_data)
    table_string = get_table_as_string(postgres_container).decode()
    table_html = highlight(table_string, SqlLexer(), HtmlFormatter())
    return table_html


if __name__ == '__main__':
    app.run()
