import json

import requests
from transformers import pipeline

from hulse import settings, errors


def process_stream_data(raw_data: str) -> dict:
    """Process a block of stream data from the Hulse server.

    :param raw_data: Raw stream data block.
    :type raw_data: str
    :return: Processed stream data block (if any).
    :rtype: dict
    """
    data = raw_data.decode("utf-8")
    if "data:" in data:
        try:
            data = json.loads(data.replace("data:", "").strip())
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
    try:
        for line in response.iter_lines():
            data = process_stream_data(line)
            if data:
                return data
    except Exception as e:
        # if no results received, raise error
        return None


def handle_producer_stream(response: requests.Response, api_key: str):
    """Iterate over the response stream and process the data.

    :param response: Stream request response to be handled.
    :type response: requests.Response
    :param api_key: Hulse API key.
    :type api_key: str
    """
    for line in response.iter_lines():
        data = process_stream_data(line)
        if data:
            # analyse data using hugging face model
            try:
                # feed pipeline with task & model queried by user
                classifier = pipeline(task=data.get("task"), model=data.get("model"))
                result = classifier(data.get("data"))
            except Exception as e:
                print("Error:", e)

            # post data back to the server
            resp = requests.post(
                settings.HULSE_STREAM_URL + "result/",
                data={
                    "result": json.dumps(result[0]),
                    "qid": data.get("qid"),
                },
                headers=settings.get_auth_headers(api_key),
            )


def post_query(task: str, model: str, data: str, api_key: str) -> dict:
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
        {"task": task, "data": data, "model": model},
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
        raise Exception(r.status_code)

    clusters = r.json().get("clusters")
    return clusters


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
