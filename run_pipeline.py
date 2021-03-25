from cli_args import get_cli_args
from connection import Connection
from stage1.stage1_load_data import load_stage1_tra, load_stage1_non_tra
from utilities.secrets import hostname, database, username, password, access_key, secret_access_key
from upload_function import upload_to_s3
import warnings
warnings.filterwarnings('ignore')


def main(args):
    issuer, sector, tenor, start_date, currency = args.issuer, args.sector, args.tenor, args.start_date, args.currency
    print("Investor Ranking is running in {} mode".format(args.mode))
    print("issuer:{}, sector:{}, tenor:{}, start_date:{}, currency:{}".format(issuer,sector,tenor,start_date,currency))

    #connection = Connection(env_dict['hostname'], env_dict['database'], env_dict['username'], env_dict['password'])
    connection = Connection(hostname, database, username, password)
    connection.connect()

    stage1_traditional_df, _, _ = load_stage1_tra(connection, start_date, issuer,
                                                  currency, sector, tenor)
    traditional_investor_id_list = stage1_traditional_df['investor_id'].unique().tolist()
    stage1_non_traditional_df, _, _ = load_stage1_non_tra(connection, start_date,
                                                          currency, sector, tenor, traditional_investor_id_list)

    upload = upload_to_s3(access_key, secret_access_key,
                          stage1_traditional_df,
                          issuer,
                          currency)
    if upload:
        print("Successfully Upload to S3!")
    else:
        print("Failed uploading to S3!")

    print(stage1_traditional_df)
    print(stage1_non_traditional_df)

    intersection = set(stage1_traditional_df['investor'].unique().tolist()).intersection(
        set(stage1_non_traditional_df['investor'].unique().tolist())
    )
    assert(len(intersection)==0)

    connection.close()


if __name__ == '__main__':
    """
    Sample Input Payload:
        docker-compose run investor-ranking -I "AT&T Inc" -S "Telecommunication Services" -C "USD" -T 10 -M "DEV"
    """
    args = get_cli_args()
    main(args)