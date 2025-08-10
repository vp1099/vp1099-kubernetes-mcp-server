
from fastmcp import FastMCP
from kubernetes import client, config
from kubernetes.client.rest import ApiException

mcp = FastMCP("Kubernetes MCP Server")

# Top 30 Kubernetes tools as MCP tools
@mcp.tool
def list_pods(namespace: str = None) -> str:
    """List all pods in a namespace, or all namespaces if none specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        if namespace:
            pods = v1.list_namespaced_pod(namespace)
        else:
            pods = v1.list_pod_for_all_namespaces()
        pod_list = []
        for pod in pods.items:
            pod_list.append(f"{pod.metadata.namespace}/{pod.metadata.name}")
        return "\n".join(pod_list) if pod_list else "No pods found."
    except Exception as e:
        return f"Error fetching pods: {e}"

@mcp.tool
def get_pod_logs(pod_name: str = None, namespace: str = None) -> str:
    """Get logs for a specific pod. If pod or namespace not specified, return logs for all pods in all namespaces."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        logs = []
        if pod_name and namespace:
            logs.append(f"{namespace}/{pod_name}:\n" + v1.read_namespaced_pod_log(pod_name, namespace))
        else:
            pods = v1.list_pod_for_all_namespaces()
            for pod in pods.items:
                try:
                    log = v1.read_namespaced_pod_log(pod.metadata.name, pod.metadata.namespace, tail_lines=10)
                    logs.append(f"{pod.metadata.namespace}/{pod.metadata.name}:\n{log}")
                except Exception as e:
                    logs.append(f"{pod.metadata.namespace}/{pod.metadata.name}: Error fetching logs: {e}")
        return "\n\n".join(logs) if logs else "No pod logs found."
    except Exception as e:
        return f"Error fetching pod logs: {e}"

@mcp.tool
def describe_pod(pod_name: str = None, namespace: str = None) -> str:
    """Describe a specific pod, or all pods if none specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        descriptions = []
        if pod_name and namespace:
            pod = v1.read_namespaced_pod(pod_name, namespace)
            descriptions.append(f"{namespace}/{pod_name}:\n{pod}")
        else:
            pods = v1.list_pod_for_all_namespaces()
            for pod in pods.items:
                descriptions.append(f"{pod.metadata.namespace}/{pod.metadata.name}:\n{pod}")
        return "\n\n".join(descriptions) if descriptions else "No pod descriptions found."
    except Exception as e:
        return f"Error describing pod(s): {e}"

@mcp.tool
def list_deployments(namespace: str = None) -> str:
    """List all deployments in a namespace, or all namespaces if none specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        apps_v1 = client.AppsV1Api()
        if namespace:
            deployments = apps_v1.list_namespaced_deployment(namespace)
        else:
            deployments = apps_v1.list_deployment_for_all_namespaces()
        dep_list = [f"{d.metadata.namespace}/{d.metadata.name}" for d in deployments.items]
        return "\n".join(dep_list) if dep_list else "No deployments found."
    except Exception as e:
        return f"Error fetching deployments: {e}"

@mcp.tool
def scale_deployment(deployment_name: str = None, replicas: int = None, namespace: str = None) -> str:
    """Scale a deployment to a specified number of replicas. If not specified, returns all deployments and their replica counts."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        apps_v1 = client.AppsV1Api()
        if deployment_name and replicas is not None and namespace:
            body = {'spec': {'replicas': replicas}}
            apps_v1.patch_namespaced_deployment_scale(deployment_name, namespace, body)
            return f"Scaled deployment {namespace}/{deployment_name} to {replicas} replicas."
        else:
            deployments = apps_v1.list_deployment_for_all_namespaces()
            return "\n".join([f"{d.metadata.namespace}/{d.metadata.name}: {d.spec.replicas} replicas" for d in deployments.items])
    except Exception as e:
        return f"Error scaling deployment(s): {e}"

@mcp.tool
def list_services(namespace: str = None) -> str:
    """List all services in a namespace, or all namespaces if none specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        if namespace:
            services = v1.list_namespaced_service(namespace)
        else:
            services = v1.list_service_for_all_namespaces()
        svc_list = [f"{s.metadata.namespace}/{s.metadata.name}" for s in services.items]
        return "\n".join(svc_list) if svc_list else "No services found."
    except Exception as e:
        return f"Error fetching services: {e}"

@mcp.tool
def get_service(service_name: str = None, namespace: str = None) -> str:
    """Get details of a specific service, or all services if not specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        if service_name and namespace:
            svc = v1.read_namespaced_service(service_name, namespace)
            return str(svc)
        else:
            services = v1.list_service_for_all_namespaces()
            return "\n\n".join([f"{s.metadata.namespace}/{s.metadata.name}: {s.spec}" for s in services.items])
    except Exception as e:
        return f"Error fetching service(s): {e}"

@mcp.tool
def list_namespaces() -> str:
    """List all namespaces."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        ns = v1.list_namespace()
        return "\n".join([n.metadata.name for n in ns.items])
    except Exception as e:
        return f"Error fetching namespaces: {e}"

@mcp.tool
def create_namespace(namespace: str = None) -> str:
    """Create a new namespace. If none specified, returns all namespaces."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        if namespace:
            body = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace))
            v1.create_namespace(body)
            return f"Created namespace: {namespace}"
        else:
            ns = v1.list_namespace()
            return "\n".join([n.metadata.name for n in ns.items])
    except Exception as e:
        return f"Error creating/listing namespaces: {e}"

@mcp.tool
def delete_namespace(namespace: str = None) -> str:
    """Delete a namespace. If none specified, returns all namespaces."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        if namespace:
            v1.delete_namespace(namespace)
            return f"Deleted namespace: {namespace}"
        else:
            ns = v1.list_namespace()
            return "\n".join([n.metadata.name for n in ns.items])
    except Exception as e:
        return f"Error deleting/listing namespaces: {e}"

@mcp.tool
def list_nodes() -> str:
    """List all nodes in the cluster."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        nodes = v1.list_node()
        return "\n".join([n.metadata.name for n in nodes.items])
    except Exception as e:
        return f"Error fetching nodes: {e}"

@mcp.tool
def describe_node(node_name: str = None) -> str:
    """Describe a specific node, or all nodes if not specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        if node_name:
            node = v1.read_node(node_name)
            return str(node)
        else:
            nodes = v1.list_node()
            return "\n\n".join([str(n) for n in nodes.items])
    except Exception as e:
        return f"Error describing node(s): {e}"

@mcp.tool
def list_configmaps(namespace: str = None) -> str:
    """List all configmaps in a namespace, or all namespaces if none specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        if namespace:
            cms = v1.list_namespaced_config_map(namespace)
        else:
            cms = v1.list_config_map_for_all_namespaces()
        cm_list = [f"{cm.metadata.namespace}/{cm.metadata.name}" for cm in cms.items]
        return "\n".join(cm_list) if cm_list else "No configmaps found."
    except Exception as e:
        return f"Error fetching configmaps: {e}"

@mcp.tool
def get_configmap(configmap_name: str = None, namespace: str = None) -> str:
    """Get a specific configmap, or all configmaps if not specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        if configmap_name and namespace:
            cm = v1.read_namespaced_config_map(configmap_name, namespace)
            return f"ConfigMap '{configmap_name}' in namespace '{namespace}':\n" + str(cm.data)
        else:
            cms = v1.list_config_map_for_all_namespaces()
            return "\n\n".join([f"{cm.metadata.namespace}/{cm.metadata.name}: {cm.data}" for cm in cms.items])
    except Exception as e:
        return f"Error fetching configmap(s): {e}"

@mcp.tool
def list_secrets(namespace: str = None) -> str:
    """List all secrets in a namespace, or all namespaces if none specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        if namespace:
            secrets = v1.list_namespaced_secret(namespace)
        else:
            secrets = v1.list_secret_for_all_namespaces()
        secret_list = [f"{s.metadata.namespace}/{s.metadata.name}" for s in secrets.items]
        return "\n".join(secret_list) if secret_list else "No secrets found."
    except Exception as e:
        return f"Error fetching secrets: {e}"

@mcp.tool
def get_secret(secret_name: str = None, namespace: str = None) -> str:
    """Get a specific secret, or all secrets if not specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        if secret_name and namespace:
            secret = v1.read_namespaced_secret(secret_name, namespace)
            return str(secret)
        else:
            secrets = v1.list_secret_for_all_namespaces()
            return "\n\n".join([f"{s.metadata.namespace}/{s.metadata.name}: {s.data}" for s in secrets.items])
    except Exception as e:
        return f"Error fetching secret(s): {e}"

@mcp.tool
def list_persistent_volumes() -> str:
    """List all persistent volumes."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        pvs = v1.list_persistent_volume()
        return "\n".join([pv.metadata.name for pv in pvs.items])
    except Exception as e:
        return f"Error fetching persistent volumes: {e}"

@mcp.tool
def list_persistent_volume_claims(namespace: str = None) -> str:
    """List all persistent volume claims in a namespace, or all namespaces if none specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        if namespace:
            pvcs = v1.list_namespaced_persistent_volume_claim(namespace)
        else:
            pvcs = v1.list_persistent_volume_claim_for_all_namespaces()
        pvc_list = [f"{pvc.metadata.namespace}/{pvc.metadata.name}" for pvc in pvcs.items]
        return "\n".join(pvc_list) if pvc_list else "No PVCs found."
    except Exception as e:
        return f"Error fetching PVCs: {e}"

@mcp.tool
def get_pvc(pvc_name: str = None, namespace: str = None) -> str:
    """Get a specific persistent volume claim, or all PVCs if not specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        if pvc_name and namespace:
            pvc = v1.read_namespaced_persistent_volume_claim(pvc_name, namespace)
            return str(pvc)
        else:
            pvcs = v1.list_persistent_volume_claim_for_all_namespaces()
            return "\n\n".join([f"{pvc.metadata.namespace}/{pvc.metadata.name}: {pvc.status.phase}" for pvc in pvcs.items])
    except Exception as e:
        return f"Error fetching PVC(s): {e}"

@mcp.tool
def list_jobs(namespace: str = None) -> str:
    """List all jobs in a namespace, or all namespaces if none specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        batch_v1 = client.BatchV1Api()
        if namespace:
            jobs = batch_v1.list_namespaced_job(namespace)
        else:
            jobs = batch_v1.list_job_for_all_namespaces()
        job_list = [f"{j.metadata.namespace}/{j.metadata.name}" for j in jobs.items]
        return "\n".join(job_list) if job_list else "No jobs found."
    except Exception as e:
        return f"Error fetching jobs: {e}"

@mcp.tool
def get_job(job_name: str = None, namespace: str = None) -> str:
    """Get a specific job, or all jobs if not specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        batch_v1 = client.BatchV1Api()
        if job_name and namespace:
            job = batch_v1.read_namespaced_job(job_name, namespace)
            return str(job)
        else:
            jobs = batch_v1.list_job_for_all_namespaces()
            return "\n\n".join([f"{j.metadata.namespace}/{j.metadata.name}: {j.status}" for j in jobs.items])
    except Exception as e:
        return f"Error fetching job(s): {e}"

@mcp.tool
def list_cronjobs(namespace: str = None) -> str:
    """List all cronjobs in a namespace, or all namespaces if none specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        batch_v1 = client.BatchV1beta1Api() if hasattr(client, 'BatchV1beta1Api') else client.BatchV1Api()
        if namespace:
            cronjobs = batch_v1.list_namespaced_cron_job(namespace)
        else:
            cronjobs = batch_v1.list_cron_job_for_all_namespaces()
        cj_list = [f"{cj.metadata.namespace}/{cj.metadata.name}" for cj in cronjobs.items]
        return "\n".join(cj_list) if cj_list else "No cronjobs found."
    except Exception as e:
        return f"Error fetching cronjobs: {e}"

@mcp.tool
def get_cronjob(cronjob_name: str = None, namespace: str = None) -> str:
    """Get a specific cronjob, or all cronjobs if not specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        batch_v1 = client.BatchV1beta1Api() if hasattr(client, 'BatchV1beta1Api') else client.BatchV1Api()
        if cronjob_name and namespace:
            cj = batch_v1.read_namespaced_cron_job(cronjob_name, namespace)
            return str(cj)
        else:
            cronjobs = batch_v1.list_cron_job_for_all_namespaces()
            return "\n\n".join([f"{cj.metadata.namespace}/{cj.metadata.name}: {cj.status}" for cj in cronjobs.items])
    except Exception as e:
        return f"Error fetching cronjob(s): {e}"

@mcp.tool
def list_ingresses(namespace: str = None) -> str:
    """List all ingresses in a namespace, or all namespaces if none specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        networking_v1 = client.NetworkingV1Api()
        if namespace:
            ingresses = networking_v1.list_namespaced_ingress(namespace)
        else:
            ingresses = networking_v1.list_ingress_for_all_namespaces()
        ing_list = [f"{i.metadata.namespace}/{i.metadata.name}" for i in ingresses.items]
        return "\n".join(ing_list) if ing_list else "No ingresses found."
    except Exception as e:
        return f"Error fetching ingresses: {e}"

@mcp.tool
def get_ingress(ingress_name: str = None, namespace: str = None) -> str:
    """Get a specific ingress, or all ingresses if not specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        networking_v1 = client.NetworkingV1Api()
        if ingress_name and namespace:
            ingress = networking_v1.read_namespaced_ingress(ingress_name, namespace)
            return str(ingress)
        else:
            ingresses = networking_v1.list_ingress_for_all_namespaces()
            return "\n\n".join([f"{i.metadata.namespace}/{i.metadata.name}: {i.status}" for i in ingresses.items])
    except Exception as e:
        return f"Error fetching ingress(es): {e}"

@mcp.tool
def list_daemonsets(namespace: str = None) -> str:
    """List all daemonsets in a namespace, or all namespaces if none specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        apps_v1 = client.AppsV1Api()
        if namespace:
            ds = apps_v1.list_namespaced_daemon_set(namespace)
        else:
            ds = apps_v1.list_daemon_set_for_all_namespaces()
        ds_list = [f"{d.metadata.namespace}/{d.metadata.name}" for d in ds.items]
        return "\n".join(ds_list) if ds_list else "No daemonsets found."
    except Exception as e:
        return f"Error fetching daemonsets: {e}"

@mcp.tool
def get_daemonset(daemonset_name: str = None, namespace: str = None) -> str:
    """Get a specific daemonset, or all daemonsets if not specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        apps_v1 = client.AppsV1Api()
        if daemonset_name and namespace:
            ds = apps_v1.read_namespaced_daemon_set(daemonset_name, namespace)
            return str(ds)
        else:
            ds = apps_v1.list_daemon_set_for_all_namespaces()
            return "\n\n".join([f"{d.metadata.namespace}/{d.metadata.name}: {d.status}" for d in ds.items])
    except Exception as e:
        return f"Error fetching daemonset(s): {e}"

@mcp.tool
def list_statefulsets(namespace: str = None) -> str:
    """List all statefulsets in a namespace, or all namespaces if none specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        apps_v1 = client.AppsV1Api()
        if namespace:
            ss = apps_v1.list_namespaced_stateful_set(namespace)
        else:
            ss = apps_v1.list_stateful_set_for_all_namespaces()
        ss_list = [f"{s.metadata.namespace}/{s.metadata.name}" for s in ss.items]
        return "\n".join(ss_list) if ss_list else "No statefulsets found."
    except Exception as e:
        return f"Error fetching statefulsets: {e}"

@mcp.tool
def get_statefulset(statefulset_name: str = None, namespace: str = None) -> str:
    """Get a specific statefulset, or all statefulsets if not specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        apps_v1 = client.AppsV1Api()
        if statefulset_name and namespace:
            ss = apps_v1.read_namespaced_stateful_set(statefulset_name, namespace)
            return str(ss)
        else:
            ss = apps_v1.list_stateful_set_for_all_namespaces()
            return "\n\n".join([f"{s.metadata.namespace}/{s.metadata.name}: {s.status}" for s in ss.items])
    except Exception as e:
        return f"Error fetching statefulset(s): {e}"

@mcp.tool
def list_events(namespace: str = None) -> str:
    """List all events in a namespace, or all namespaces if none specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        if namespace:
            events = v1.list_namespaced_event(namespace)
        else:
            events = v1.list_event_for_all_namespaces()
        event_list = [f"{e.metadata.namespace}/{e.metadata.name}: {e.message}" for e in events.items]
        return "\n".join(event_list) if event_list else "No events found."
    except Exception as e:
        return f"Error fetching events: {e}"

@mcp.tool
def get_event(event_name: str = None, namespace: str = None) -> str:
    """Get a specific event, or all events if not specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        if event_name and namespace:
            event = v1.read_namespaced_event(event_name, namespace)
            return str(event)
        else:
            events = v1.list_event_for_all_namespaces()
            return "\n\n".join([f"{e.metadata.namespace}/{e.metadata.name}: {e.message}" for e in events.items])
    except Exception as e:
        return f"Error fetching event(s): {e}"

@mcp.tool
def list_replicasets(namespace: str = None) -> str:
    """List all replicasets in a namespace, or all namespaces if none specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        apps_v1 = client.AppsV1Api()
        if namespace:
            rs = apps_v1.list_namespaced_replica_set(namespace)
        else:
            rs = apps_v1.list_replica_set_for_all_namespaces()
        rs_list = [f"{r.metadata.namespace}/{r.metadata.name}" for r in rs.items]
        return "\n".join(rs_list) if rs_list else "No replicasets found."
    except Exception as e:
        return f"Error fetching replicasets: {e}"

@mcp.tool
def get_replicaset(replicaset_name: str = None, namespace: str = None) -> str:
    """Get a specific replicaset, or all replicasets if not specified."""
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        apps_v1 = client.AppsV1Api()
        if replicaset_name and namespace:
            rs = apps_v1.read_namespaced_replica_set(replicaset_name, namespace)
            return str(rs)
        else:
            rs = apps_v1.list_replica_set_for_all_namespaces()
            return "\n\n".join([f"{r.metadata.namespace}/{r.metadata.name}: {r.status}" for r in rs.items])
    except Exception as e:
        return f"Error fetching replicaset(s): {e}"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
