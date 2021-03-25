from utilities import get_env as util_env

# S3 Constants:
s3_bucket = 'investor-ranking'

hostname = util_env.getenv('DB_HOSTNAME')
database = util_env.getenv('DB_DATABASE')
username = util_env.getenv('DB_USERNAME')
password = util_env.getenv('DB_PASSWORD')


access_key = util_env.getenv('AWS_ACCESS_KEY_ID')
secret_access_key = util_env.getenv('AWS_SECRET_ACCESS_KEY')


def resolve_env_variables():
    # For Database Connection:
    hostname = util_env.getenv('DB_HOSTNAME')
    database = util_env.getenv('DB_DATABASE')
    username = util_env.getenv('DB_USERNAME')
    password = util_env.getenv('DB_PASSWORD')

    # For AWS Credentials:
    access_key = util_env.getenv('AWS_ACCESS_KEY_ID')
    secret_access_key = util_env.getenv('AWS_SECRET_ACCESS_KEY')

    env_dict = {
        'hostname': hostname,
        'database': database,
        'username': username,
        'password': password,
        'access_key': access_key,
        'secret_access_key': secret_access_key
    }

    return env_dict