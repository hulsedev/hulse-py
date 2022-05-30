from typing import Union

from hulse import settings, errors, utils


class Hulse:
    def __init__(
        self,
        api_key: str,
    ):
        """Create a new Hulse client.

        :param api_key: Your Hulse API key to run queries
        :type api_key: str
        """
        self.api_key = api_key

    def query(
        self,
        data: Union[str, list],
        task: str = None,
        model: str = None,
        **kwargs,
    ) -> dict:
        """Run an inference query on a Hulse cluster.

        Note that we don't support HF pipeline batching as of now, since all
        inferences are performed on CPU. HF does not recommend batching on CPU.

        :param task: Task to be performed. Corresponds to the model you
            want to use.
        :type task: str
        :param data: Data to be inferred upon by the target model.
        :type data: Any
        """
        if task and task not in settings.SUPPORTED_TASKS:
            raise errors.UnsupportedTaskError(task)

        return utils.post_query(task, data, self.api_key)

    def get_clusters(
        self,
    ):
        pass

    def set_api_key(self, api_key: str):
        """Set the Hulse API key.

        :param api_key: Hulse API key to define as default configuration.
        :type api_key: str
        """
        self.api_key = api_key
