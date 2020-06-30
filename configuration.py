import yaml


def read_configuration():
    # Load configuration
    file = open('config/config.yml', "r")
    config = yaml.load(file, Loader=yaml.FullLoader)

    base_url = config['stock_API_baseUrl']
    function = config['stock_API_function']
    function_name = config['stock_API_function_name']
    stock_symbol = config['stock_symbol']
    alpha_vantage_api_key = config['alpha_vantage_API_key']
    sendgrid_api_key = config['sendgrid_API_key']
    email_from = config['email_from']
    email_to = config['email_to']
    threshold = config['threshold']

    file.close()

    return base_url, function, function_name, alpha_vantage_api_key, sendgrid_api_key, stock_symbol, email_from, \
        email_to, threshold
