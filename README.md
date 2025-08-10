# Kubernetes MCP Server (FastMCP)

This project provides a Kubernetes MCP (Model Context Protocol) server built using [FastMCP](https://github.com/jlowin/fastmcp) and the official Kubernetes Python client. It exposes a wide range of Kubernetes management and inspection tools as MCP tools, making it easy to interact with your Kubernetes or OpenShift cluster programmatically or via GitHub Copilot.


use https://gitingest.com/jlowin/fastmcp
download the above and feed it as a context to your copilot chat

prompt to build a mcp server: build a kubernet mcp server with top 30 kubernetes tools using the jlowin-fastmcp-8a5edab282632443.txt file. Make the functions dynamic so that it works for all cases even when the user does not provide a namespace or resource name.

## Features

The MCP server exposes the following Kubernetes operations as MCP tools:

- **Pod Management**: List, describe, and get logs for pods
- **Deployment Management**: List, scale, and inspect deployments
- **Service Management**: List and get details of services
- **Namespace Management**: List, create, and delete namespaces
- **Node Management**: List and describe nodes
- **ConfigMap & Secret Management**: List and get ConfigMaps and Secrets
- **Persistent Volumes & Claims**: List PVs and PVCs, get PVC details
- **Job & CronJob Management**: List and get jobs and cronjobs
- **Ingress Management**: List and get ingresses
- **DaemonSet, StatefulSet, ReplicaSet Management**: List and get details for each
- **Event Management**: List and get cluster events

All tools support filtering by namespace where applicable.

## Prerequisites

- Python 3.x
- [fastmcp](https://pypi.org/project/fastmcp/)
- [kubernetes](https://pypi.org/project/kubernetes/) Python client
- [kubectl](https://kubernetes.io/docs/tasks/tools/) (for cluster access)
- Access to a Kubernetes or OpenShift cluster (kubeconfig or in-cluster config)

## Installation

1. Install Python dependencies:

    ```sh
    pip install fastmcp kubernetes
    ```

2. Ensure `python` and `fastmcp` are in your system PATH.
3. Install and configure `kubectl` and connect to your cluster.
4. (Optional) Update your `mcp.json` to add the MCP server endpoint:

    ```json
    "kubernetes-local": {
      "name": "Kubernetes MCP Server",
      "url": "http://localhost:8000/mcp/"
    }
    ```

## Usage

1. Start the MCP server:

    ```sh
    python kube_mcp_server.py
    ```

2. The server will run on `http://0.0.0.0:8000/mcp/` by default.
3. You can now interact with your Kubernetes cluster using MCP tools (e.g., via GitHub Copilot or any MCP client).

## Example MCP Tools

- `list_pods(namespace=None)`
- `get_pod_logs(pod_name=None, namespace=None)`
- `describe_pod(pod_name=None, namespace=None)`
- `list_deployments(namespace=None)`
- `scale_deployment(deployment_name, replicas, namespace)`
- `list_services(namespace=None)`
- `get_service(service_name=None, namespace=None)`
- `list_namespaces()`
- `create_namespace(namespace)`
- `delete_namespace(namespace)`
- `list_nodes()`
- `describe_node(node_name=None)`
- `list_configmaps(namespace=None)`
- `get_configmap(configmap_name=None, namespace=None)`
- `list_secrets(namespace=None)`
- `get_secret(secret_name=None, namespace=None)`
- `list_persistent_volumes()`
- `list_persistent_volume_claims(namespace=None)`
- `get_pvc(pvc_name=None, namespace=None)`
- `list_jobs(namespace=None)`
- `get_job(job_name=None, namespace=None)`
- `list_cronjobs(namespace=None)`
- `get_cronjob(cronjob_name=None, namespace=None)`
- `list_ingresses(namespace=None)`
- `get_ingress(ingress_name=None, namespace=None)`
- `list_daemonsets(namespace=None)`
- `get_daemonset(daemonset_name=None, namespace=None)`
- `list_statefulsets(namespace=None)`
- `get_statefulset(statefulset_name=None, namespace=None)`
- `list_events(namespace=None)`
- `get_event(event_name=None, namespace=None)`
- `list_replicasets(namespace=None)`
- `get_replicaset(replicaset_name=None, namespace=None)`

## Notes


Example prompt: 
1. get me the pods running on the vp1099 namespace.
2. scale down all pods in the vp1099 namespace to 1 replica.


- The server will attempt to use your local kubeconfig, or fall back to in-cluster config if running inside a cluster.
- Make sure your `kubectl` context is set to the desired cluster/namespace.
- You can extend the server by adding more MCP tools using the `@mcp.tool` decorator.
- **Gitingest support:** You can use gitingest to ingest and interact with GitHub repositories directly through MCP, enabling advanced code search and automation workflows alongside your Kubernetes operations.

## License

MIT License
