from helper import docker_exec_with_retry

db_container_name = 'postgres_DB'
db_docker_image = "fetchdocker/data-takehome-postgres:latest"

db_username = "postgres"
db_name = "postgres"
db_table_name = "user_logins"

db_docker_ports = {'8000/tcp': ('127.0.0.1', 8000)}
db_command_tag = "POSTGRES WRITE"
select_command_tag = "POSTGRES SELECT * FROM"


def generate_db_command(user_login_data):
    user_id = user_login_data.user_id
    device_type = user_login_data.device_type
    masked_ip = user_login_data.masked_ip
    masked_device_id = user_login_data.masked_device_id
    locale = user_login_data.locale
    app_version = user_login_data.app_version

    query = "psql -U {} -d {} -c \"INSERT INTO user_logins " \
            "(user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date) " \
            "VALUES ('{}', '{}', '{}', '{}', '{}', {}, now());\" -A -t"
    command = query.format(db_username, db_name, user_id, device_type, masked_ip, masked_device_id, locale, app_version)
    return command


def write_to_postgres(postgres_container, user_login_data):
    db_command = generate_db_command(user_login_data)
    postgres_response = docker_exec_with_retry(postgres_container, db_command, db_command_tag)
    print(postgres_response)
    print("Writing to postgres done")


def get_table_as_string(postgres_container):
    select_command = "psql -U postgres -d postgres -c \"SELECT * FROM user_logins\""
    postgres_response = docker_exec_with_retry(postgres_container, select_command, select_command_tag)
    print(postgres_response.output)
    print("Select command executed")
    return postgres_response.output
