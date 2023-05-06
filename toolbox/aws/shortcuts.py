from .utils import start_instance, stop_instance
import configparser
from typing import List
import subprocess
import time

def start_instance_from_config(config_path: str) -> None:
    """Starts the EC2 instance."""
    # config
    config = configparser.ConfigParser()
    config.read(config_path)

    # Start the EC2 instance
    instance_id = config['AWS']['INSTANCE_ID']
    region_name = config['AWS']['REGION']
    start_instance(instance_id, region_name, config)

    # Wait for the instance to start
    print("\nTo login, wait a few seconds and run the following command:")
    print("ssh -i " + config['AWS']['SSH_KEY_PATH'] + " ubuntu@" + config['AWS']['PUBLIC_IP'])


def stop_instance_from_config(config_path: str) -> None:
    """Stops the EC2 instance."""
    # config
    config = configparser.ConfigParser()
    config.read(config_path)

    # Start the EC2 instance
    instance_id = config['AWS']['INSTANCE_ID']
    region_name = config['AWS']['REGION']
    stop_instance(instance_id, region_name, config)


def start_instance_and_run_from_config(config_path, commands: List[str], wait_seconds: int = 20) -> None:
    # config
    config = configparser.ConfigParser()
    config.read(config_path)

    # Start the EC2 instance
    instance_id = config['AWS']['INSTANCE_ID']
    region_name = config['AWS']['REGION']
    start_instance(instance_id, region_name, config)

    # Wait for the instance to start
    print(f"Waiting {wait_seconds} seconds for the instance to start...")
    time.sleep(wait_seconds)

    # Connect to the EC2 instance and pull the latest code from GitHub
    cmd_aws = "; ".join(commands)
    cmd_str = "ssh -i " + config['AWS']['SSH_KEY_PATH'] + " ec2-user@" + config['AWS']['PUBLIC_IP'] + " '" + cmd_aws + "'"
    print("Running command: " + cmd_str)
    subprocess.run(cmd_str, shell=True)

    print("\nTo login, run the following command:")
    print("ssh -i " + config['AWS']['SSH_KEY_PATH'] + " ec2-user@" + config['AWS']['PUBLIC_IP'])