import click

import scrapertype_scrapername.source.parameters_manager as parameters_manager
from scrapertype_scrapername.env_vars import AWS_S3_KEY_ENV, AWS_S3_SECRET_ENV, AWS_S3_REGION_ENV, \
    PROXY_SERVICE_USER_ENV, PROXY_SERVICE_PASS_ENV, \
    PARAMS_FILE, CUSTOMER_AWS_KEY, CUSTOMER_AWS_SECRET, CUSTOMER_AWS_REGION, MONGO_HOST, MONGO_USER, \
    MONGO_PASSWORD, SQL_HOST, SQL_USER, SQL_PASSWORD, PROJECT_PATH
from scrapertype_scrapername.output_manager.write_output_pipeline import save_output_data
from scrapertype_scrapername.source.scrapername import ScraperName


@click.command("execute-scraper")
@click.option("--scraper-name", type=click.STRING, help="", default='default_scraper')
@click.option("--execution-type", type=click.STRING, help="", default='normal')
@click.option("--doctype-to-export", type=click.STRING, help="Accepts csv and parquet", default='csv')
@click.option("--local-path-to-export", type=click.STRING, help="", default=None)
@click.option("--received-input", type=click.STRING, help="", default=None)
@click.option("--max-chunk-lines", type=click.INT, help="", default=5000)
@click.option("--max-worker-instances", type=click.INT, help="", default=1)
@click.option("--current-worker-number", type=click.INT, help="", default=0)
@click.option('--aws-s3-key', type=click.STRING, envvar=AWS_S3_KEY_ENV, help="", default=None)
@click.option('--aws-s3-secret', type=click.STRING, envvar=AWS_S3_SECRET_ENV, help="", default=None)
@click.option('--aws-s3-region', type=click.STRING, envvar=AWS_S3_REGION_ENV, help="", default=None)
@click.option('--customer-s3-key', type=click.STRING, envvar=CUSTOMER_AWS_KEY, help="", default=None)
@click.option('--customer-s3-secret', type=click.STRING, envvar=CUSTOMER_AWS_SECRET, help="", default=None)
@click.option('--customer-s3-region', type=click.STRING, envvar=CUSTOMER_AWS_REGION, help="", default=None)
@click.option('--customer-s3-bucket', type=click.STRING, help="", default=None)
@click.option('--customer-s3-prefix', type=click.STRING, help="", default=None)
@click.option('--option-save-to-customer-bucket', type=click.BOOL, help="", default=False)
@click.option('--mongo-host', type=click.STRING, envvar=MONGO_HOST, help="", default=None)
@click.option('--mongo-user', type=click.STRING, envvar=MONGO_USER, help="", default=None)
@click.option('--mongo-password', type=click.STRING, envvar=MONGO_PASSWORD, help="", default=None)
@click.option('--sql-host', type=click.STRING, envvar=SQL_HOST, help="", default=None)
@click.option('--sql-user', type=click.STRING, envvar=SQL_USER, help="", default=None)
@click.option('--sql-password', type=click.STRING, envvar=SQL_PASSWORD, help="", default=None)
@click.option("--proxy-service-user", envvar=PROXY_SERVICE_USER_ENV, type=click.STRING, help="", default=None)
@click.option("--proxy-service-pass", envvar=PROXY_SERVICE_PASS_ENV, type=click.STRING, help="", default=None)
@click.option("--is-running-local/--is-not-running-local", default=False)
def main(scraper_name: str,
         execution_type: str,
         doctype_to_export: str,
         local_path_to_export: str,
         received_input: str,
         max_chunk_lines: int,
         max_worker_instances: int,
         current_worker_number: int,
         aws_s3_key: str,
         aws_s3_secret: str,
         aws_s3_region: str,
         customer_s3_key: str,
         customer_s3_secret: str,
         customer_s3_region: str,
         customer_s3_bucket: str,
         customer_s3_prefix: str,
         option_save_to_customer_bucket: bool,
         mongo_host: str,
         mongo_user: str,
         mongo_password: str,
         sql_host: str,
         sql_user: str,
         sql_password: str,
         proxy_service_user: str,
         proxy_service_pass: str,
         is_running_local: bool,
         ):
    """
    Main program execution.

    :param scraper_name: Name of scrapper.
    :param execution_type: Type of execution of program.
    :param doctype_to_export: If you want to export data to .csv or .parquet.
    :param local_path_to_export: Select some path to export data.
    :param received_input: Some received input.
    :param max_chunk_lines: Maximum chunk of data.
    :param max_worker_instances: Identify how many instances that will run on some pipeline.
    :param current_worker_number: Identify the current worker number(instance number of pipeline).
    :param aws_s3_key: Aws Key.
    :param aws_s3_secret: Aws Secret.
    :param aws_s3_region: Aws Region.
    :param customer_s3_key: Customer AWS s3 Key.
    :param customer_s3_secret: Customer Aws Secret.
    :param customer_s3_region: Customer Aws Region.
    :param customer_s3_bucket: Customer aws s3 bucket.
    :param customer_s3_prefix: Customer AWS s3 prefix.
    :param option_save_to_customer_bucket: If is allowed to save on customer aws s3 storage.
    :param mongo_host: Mongodb Host.
    :param mongo_user: Mongodb User.
    :param mongo_password: Mongodb Password.
    :param sql_host: SQL Host.
    :param sql_user: SQL User.
    :param sql_password: SQL Password.
    :param proxy_service_user: Some proxy service user.
    :param proxy_service_pass: Some proxy service password.
    :param is_running_local: If program is running on local machine.
    :return:
    """
    param_parquet = PARAMS_FILE
    project_path = PROJECT_PATH

    run_program = True
    stats_to_return = {''}

    if not max_chunk_lines:
        max_lines_to_save = 10000

    if execution_type == 'normal':
        run_test = False
    elif execution_type == 'testing':
        run_test = True
    else:
        run_test = False

    # Get all parameters to run on ./assets/.parquet file
    all_params = parameters_manager.create_or_get_all_params_list(parquet_dir=param_parquet)

    # Manage witch parameter runs
    parameters_to_run = parameters_manager.parameters_organizer(parameter_list=all_params,
                                                                max_workers=max_worker_instances,
                                                                worker_number=current_worker_number,
                                                                is_testing=run_test)

    print('Selected parameters: ', len(parameters_to_run))

    if run_program:
        # Passes all input information to main class
        scraper_class = ScraperName(parameters_to_run=parameters_to_run,
                                    scraper_name=scraper_name,
                                    execution_type=execution_type,
                                    is_testing=run_test,
                                    project_path=project_path,
                                    doctype_to_export=doctype_to_export,
                                    local_path_to_export=local_path_to_export,
                                    received_input=received_input,
                                    max_chunk_lines=max_chunk_lines,
                                    max_worker_instances=max_worker_instances,
                                    current_worker_number=current_worker_number,
                                    aws_s3_key=aws_s3_key,
                                    aws_s3_secret=aws_s3_secret,
                                    aws_s3_region=aws_s3_region,
                                    customer_s3_key=customer_s3_key,
                                    customer_s3_secret=customer_s3_secret,
                                    customer_s3_region=customer_s3_region,
                                    customer_s3_bucket=customer_s3_bucket,
                                    customer_s3_prefix=customer_s3_prefix,
                                    option_save_to_customer_bucket=option_save_to_customer_bucket,
                                    mongo_host=mongo_host,
                                    mongo_user=mongo_user,
                                    mongo_password=mongo_password,
                                    sql_host=sql_host,
                                    sql_mongo_user=sql_user,
                                    sql_mongo_password=sql_password,
                                    proxy_service_user=proxy_service_user,
                                    proxy_service_pass=proxy_service_pass
                                    )
        # Select execution types
        if execution_type == 'normal':
            stats_to_return = scraper_class.run_scrapername()
        elif execution_type == 'create_params':
            scraper_class.create_parameters()

    else:
        pass

    # Show run stats
    print(stats_to_return)
    # Save some output file
    save_output_data(str(stats_to_return), is_running_local)


if __name__ == '__main__':
    main()
