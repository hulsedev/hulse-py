import json
import inspect
import os
import logging
import ctypes
import threading

import requests
from transformers import pipeline
from flask import Flask, redirect, request, cli

# disable flask logs to CLI, avoid spamming user
cli.show_server_banner = lambda *args: None


from hulse import settings, errors


def process_stream_data(raw_data: str) -> dict:
    """Process a block of stream data from the Hulse server.

    :param raw_data: Raw stream data block.
    :type raw_data: str
    :return: Processed stream data block (if any).
    :rtype: dict
    """
    decoded_raw_data = raw_data.decode("utf-8")
    if "data:" in decoded_raw_data:
        try:
            stripped_raw_data = decoded_raw_data.replace("data:", "").strip()
            data = json.loads(stripped_raw_data)
            return data
        except json.decoder.JSONDecodeError:
            pass


def handle_consumer_stream(response: requests.Response, timeout: int = 10) -> dict:
    """Handle the response stream from the Hulse server when making a query.

    :param response: Stream request response to be handled.
    :type response: requests.Response
    :param timeout: Timeout after which should raise an error if no results received, defaults to 10
    :type timeout: int, optional
    :return: Result returned from the Hulse server.
    :rtype: dict
    """
    # TODO: implement timeout logic
    for line in response.iter_lines():
        data = process_stream_data(line)
        if data:
            return data


def handle_producer_stream(response: requests.Response, api_key: str):
    """Produce a stream to be sent to the Hulse server.

    :param response: Stream request response to be handled.
    :type response: requests.Response
    :param api_key: Hulse API key.
    :type api_key: str
    """
    for line in response.iter_lines():
        data = process_stream_data(line)
        if data:
            # analyse data using hugging face model
            classifier = pipeline(data.get("task"))
            result = classifier(data.get("data"))

            # post data back to the server
            resp = requests.post(
                settings.HULSE_STREAM_URL + "result/",
                data={
                    "result": json.dumps(result[0]),
                    "qid": data.get("qid"),
                },
                headers=settings.get_auth_headers(api_key),
            )


def post_query(task: str, data: str, api_key: str) -> dict:
    """Send query to server to be processed by online producers.

    :param task: Transformer task to be performed.
    :type task: str
    :param data: Data to be analysed by the target model.
    :type data: str
    :param api_key: Api key for Hulse.
    :type api_key: str
    :raises errors.UnsufficientResources: If there are no online producers.
    :raises errors.HulseError: An error occurred while communicating with the Hulse server.
    :return: The result of the query.
    :rtype: dict
    """
    channel_path = f"consumer/{api_key}/"
    query_resp = requests.get(
        settings.HULSE_STREAM_URL + channel_path,
        {"task": task, "data": data},
        stream=True,
        headers=settings.get_auth_headers(api_key),
    )
    if query_resp.status_code == 418:
        raise errors.UnsufficientResources()
    elif query_resp.status_code != 200:
        raise errors.HulseError(query_resp.status_code)
    else:
        return handle_consumer_stream(query_resp)


def get_clusters(api_key: str) -> list:
    """Get all available clusters for the given account.

    :param api_key: Hulse API key.
    :type api_key: str
    :raises Exception: Unknown error occured while sending request to Hulse server.
    :return: List of clusters for the given account.
    :rtype: list
    """
    r = requests.get(
        settings.HULSE_API_URL + "clusters/",
        headers=settings.get_auth_headers(api_key),
    )
    if r.status_code != 200:
        raise errors.HulseError(r.status_code, "Failed to get clusters")

    clusters = r.json().get("clusters")
    return clusters


def join_cluster(cluster_id: str, api_key: str) -> bool:
    """Join a Hulse cluster

    :param cluster_id: Cluster ID to join.
    :type cluster_id: str
    :param api_key: Hulse API key
    :type api_key: str
    :raises errors.HulseError: Error raised if the cluster could not be joined.
    :return: Whether the cluster was joined or not.
    :rtype: bool
    """
    r = requests.post(
        settings.HULSE_API_URL + "cluster/join/",
        headers=settings.get_auth_headers(api_key),
        data={"cluster_id": cluster_id},
    )
    if r.status_code != 200:
        raise errors.HulseError(r.status_code, "Failed to join cluster")

    return True


def delete_cluster(cluster_id: str, api_key: str) -> bool:
    """Delete a Hulse cluster

    :param cluster_id: Cluster ID to delete.
    :type cluster_id: str
    :param api_key: Hulse API key
    :type api_key: str
    :raises errors.HulseError: Error raised if the cluster could not be deleted.
    :return: Whether the cluster was deleted or not.
    :rtype: bool
    """
    r = requests.post(
        settings.HULSE_API_URL + "cluster/delete/",
        headers=settings.get_auth_headers(api_key),
        data={"cluster_id": cluster_id},
    )
    if r.status_code != 200:
        raise errors.HulseError(r.status_code, "Failed to delete cluster")

    return True


def edit_cluster(cluster_id: str, name: str, description: str, api_key: str) -> bool:
    """Edit a Hulse cluster

    :param cluster_id: Cluster ID to edit.
    :type cluster_id: str
    :param name: New name for the cluster.
    :type name: str
    :param description: New description for the cluster.
    :type description: str
    :param api_key: Hulse API key
    :type api_key: str
    :raises errors.HulseError: Error raised if the cluster could not be edited.
    :return: Whether the cluster was edited or not.
    :rtype: bool
    """
    r = requests.post(
        settings.HULSE_API_URL + "cluster/edit/",
        headers=settings.get_auth_headers(api_key),
        data={"cluster_id": cluster_id, "name": name, "description": description},
    )
    if r.status_code != 200:
        raise errors.HulseError(r.status_code, "Failed to edit cluster")

    return True


def leave_cluster(cluster_id: str, api_key: str) -> bool:
    """Leave a Hulse cluster

    :param cluster_id: Cluster ID to leave.
    :type cluster_id: str
    :param api_key: Hulse API key
    :type api_key: str
    :raises errors.HulseError: Error raised if the cluster could not be left.
    :return: Whether the cluster was left or not.
    :rtype: bool
    """
    r = requests.post(
        settings.HULSE_API_URL + "cluster/leave/",
        headers=settings.get_auth_headers(api_key),
        data={"cluster_id": cluster_id},
    )
    if r.status_code != 200:
        raise errors.HulseError(r.status_code, "Failed to leave cluster")

    return True


def run_host(api_key: str):
    """Run the Hulse host until termination.

    :param api_key: Hulse API key for the account.
    :type api_key: str
    """
    # build channel path to host computation
    channel_path = f"producer/{api_key}/"

    # make streaming request to hulse server to enable push
    r = requests.get(
        settings.HULSE_STREAM_URL + channel_path,
        headers=settings.get_auth_headers(api_key),
        stream=True,
    )
    try:
        handle_producer_stream(r, api_key)
    except Exception as e:
        raise errors.HulseError(expression=e)


def create_cluster(api_key: str, name: str, description: str = None) -> bool:
    """Create a new Hulse cluster.

    :param api_key: Hulse API key.
    :type api_key: str
    :param name: Name of the cluster to be created.
    :type name: str
    :param description: Short description of the newly created cluster, defaults to None
    :type description: str, optional
    :return: Whether the cluster was created.
    :rtype: bool
    """
    r = requests.post(
        settings.HULSE_API_URL + "cluster/create/",
        headers=settings.get_auth_headers(api_key),
        data={"name": name, "description": description},
    )
    return r.status_code == 200


def _async_raise(tid, exctype):
    """Raises an exception in the threads with id tid"""
    # https://stackoverflow.com/a/325528
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(exctype)
    )
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class HostThread(threading.Thread):
    """Run a Hulse host in a separate thread."""

    def _get_my_tid(self):
        """Get the current thread's id.

        :raises threading.ThreadError: raise a thread error if not alive.
        :raises AssertionError: if the thread id cannot be determined.
        :return: Current thread id.
        :rtype: str
        """
        if not self.is_alive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        raise AssertionError("could not determine the thread's id")

    def raise_exception(self, exctype):
        """Raise an exception within the currently running thread.

        :param exctype: Type of exception to be raised.
        :type exctype: Exception
        """
        _async_raise(self._get_my_tid(), exctype)


class LoginThread(HostThread):
    def __init__(
        self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None
    ):
        """Run a login thread in the background."""
        super().__init__(
            group=group,
            target=target,
            name=name,
            args=args,
            kwargs=kwargs,
            daemon=daemon,
        )
        self.api_key = None
        self.email = None
        self.username = None

        # local development server, ran on localhost
        self.app = Flask(__name__)
        logging.getLogger("werkzeug").disabled = True
        self.app.secret_key = os.getenv("SECRET_KEY", "mysecretkey")

        @self.app.route("/")
        def home():
            """Home route for the local login server

            :return: redirects to the successful login page on hulse.app
            :rtype: Any
            """
            self.api_key = request.args.get("authToken")
            self.username = request.args.get("username")
            self.email = request.args.get("email")

            return redirect("https://www.hulse.app/success")

    def run(self):
        """Run the login server thread

        :return: Whether the login server was started.
        :rtype: bool
        """
        try:
            self.app.run(host="0.0.0.0", port=4240)
        except Exception as e:
            return True
        return False

    def get_api_key(self):
        """Returns the current value of the thread api key.

        :return: Api key attribute of the thread.
        :rtype: str
        """
        return self.api_key

    def get_username(self):
        """Return current username"""
        return self.username

    def get_email(self):
        """Return current email"""
        return self.email
