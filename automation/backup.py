import argparse
import boto3
import datetime
import os

def backup_rds(endpoint, output_dir):
    client = boto3.client('rds')
    snapshot_id = f"backup-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    client.create_db_snapshot(
        DBSnapshotIdentifier=snapshot_id,
        DBInstanceIdentifier=endpoint
    )
    print(f"Triggered snapshot: {snapshot_id}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rds-endpoint', required=True)
    parser.add_argument('--output', default='backups/')
    args = parser.parse_args()
    os.makedirs(args.output, exist_ok=True)
    backup_rds(args.rds_endpoint, args.output)