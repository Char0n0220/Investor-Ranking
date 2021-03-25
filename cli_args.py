import argparse


def get_cli_args():
    """Use argparse to define command line interface and return arguments."""
    parser = argparse.ArgumentParser(
        description='Investor Ranking containerized microservice')
    parser.add_argument(
        '-D',
        '--start-date',
        help='Set start of date range for historical Emaxx Data Retrieving: YYYY-MM-DD',
        action='store',
        default='2019-01-01',
        metavar='DATE',
        type=str
    )

    parser.add_argument(
        '-I',
        '--issuer',
        help='Specify which issuer to run Investor Ranking with',
        action='store',
        type=str,
        required=True
    )

    parser.add_argument(
        '-S',
        '--sector',
        help='Specify which sector the specified issuer belongs to',
        action='store',
        type=str,
        required=True
    )

    parser.add_argument(
        '-C',
        '--currency',
        help='Specify which currency to run Investor Ranking with',
        action='store',
        type=str,
        required=True
    )

    parser.add_argument(
        '-T',
        '--tenor',
        help='Specify a standard tenor to run Investor Ranking with',
        action='store',
        type=int,
        required=True
    )

    parser.add_argument(
        '-M',
        '--mode',
        help='Specify mode: "production", "development"',
        action='store',
        type=str,
        required=True
    )

    return parser.parse_args()