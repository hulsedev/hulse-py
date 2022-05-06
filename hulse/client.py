from hulse import settings, errors, utils


class Hulse:
    def __init__(
        self,
        api_key: str = None,
    ):
        self.api_key = api_key

    def query(self, task: str, data: str, api_key: str = None):
        """Run an inference query on a Hulse cluster.

        :param task: Task to be performed. Corresponds to the model you
            want to use.
        :type task: str
        :param data: Data to be inferred upon by the target model.
        :type data: Any
        :param api_key: Your Hulse API key, defaults to None
        :type api_key: str, optional
        """

        if task not in settings.SUPPORTED_TASKS:
            raise errors.UnsupportedTaskError(task)

        return utils.post_query(task, data, api_key)
