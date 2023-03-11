import click


@click.command("scrape-url")
@click.option("--url", type=click.STRING, help="", default='https://www.illion.com.au/contact-us/')
@click.option("--is-running-local/--is-not-running-local", default=False)
def main(url: str,
         is_running_local: bool,
         ):
    """
    Main program execution.

    :type url: object
    :param is_running_local: If program is running on local machine.
    :return:
    """


if __name__ == '__main__':
    main()
