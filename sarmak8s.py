# SARMA Kubernetes manager
# This tool is to CREATE, DELETE, WATCH and LOG kuberenetes objects.
# Author: Michael Cruz Sanchez (Search Engineer @lucidworks)
# Copyright: GPLv3+


import argparse
from kubernetes import client, config, watch

# Create the Pods
def create_pod(api_instance, namespace, pod_manifest):
    api_response = api_instance.create_namespaced_pod(namespace, pod_manifest)
    print(f"Pod '{pod_manifest['metadata']['name']}' created in namespace '{namespace}'")
    print(f"Status: {str(api_response.status)}")

# Delete the Pods
def delete_pod(api_instance, namespace, pod_name):
    api_response = api_instance.delete_namespaced_pod(pod_name, namespace)
    print(f"Pod '{pod_name}' deleted from namespace '{namespace}'")
    print(f"Status: {str(api_response.status)}")

# Logging
def get_pod_logs(api_instance, namespace, pod_name):
    api_response = api_instance.read_namespaced_pod_log(pod_name, namespace)
    print(f"Logs for pod '{pod_name}' in namespace '{namespace}':")
    print(api_response)

# Watch the process
def watch_pods(core_api):
    print("Watching pods...")
    w = watch.Watch()
    for event in w.stream(core_api.list_pod_for_all_namespaces):
        pod = event['object']
        namespace = pod.metadata.namespace
        name = pod.metadata.name
        phase = pod.status.phase
        print(f"Pod: {name}, Namespace: {namespace}, Phase: {phase}")

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Sarma Kubernetes Manager by Michael Cruz Sanchez')

    # Add subparsers for different commands
    subparsers = parser.add_subparsers(title='Commands', dest='command')
    
    # Subparser for creating a pod
    create_parser = subparsers.add_parser('create', help='Create a pod')
    create_parser.add_argument('-m', '--manifest', type=str, help='Path to the pod manifest file')
    
    # Subparser for deleting a pod
    delete_parser = subparsers.add_parser('delete', help='Delete a pod')
    delete_parser.add_argument('-n', '--namespace', type=str, help='Namespace of the pod')
    delete_parser.add_argument('-pn', '--pod_name', type=str, help='Name of the pod')
    
    # Subparser for getting pod logs
    logs_parser = subparsers.add_parser('logs', help='Get pod logs')
    logs_parser.add_argument('-n', '--namespace', type=str, help='Namespace of the pod')
    logs_parser.add_argument('-pn', '--pod_name', type=str, help='Name of the pod')
    
    # Subparser for watching pods
    subparsers.add_parser('watch', help='Watch pods')
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # Load the Kubernetes 1uration from default location
    config.load_kube_config(config_file='$HOME/.kube/config')

    # Create an instance of the Kubernetes API client
    api_client = client.ApiClient()

    # Create an instance of the CoreV1Api client
    core_api = client.CoreV1Api(api_client)

    if args.command == 'create':
        # Read the pod manifest file
        with open(args.manifest, 'r') as manifest_file:
            pod_manifest = manifest_file.read()

        # Create the pod
        create_pod(core_api, 'default', pod_manifest)

    elif args.command == 'delete':
        # Delete the pod
        delete_pod(core_api, args.namespace, args.pod_name)

    elif args.command == 'logs':
        # Get pod logs
        get_pod_logs(core_api, args.namespace, args.pod_name)

    elif args.command == 'watch':
        # Watch pods
        watch_pods(core_api)

if __name__ == '__main__':
    main()

