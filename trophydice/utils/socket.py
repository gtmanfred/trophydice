import contextlib
import json
from typing import Union
from typing import Optional
from uuid import uuid4
from urllib.parse import urlparse

import socketio
from fastapi import FastAPI
from socketio.asyncio_pubsub_manager import AsyncPubSubManager

try:
    import aiobotocore.session
except ImportError:
    aiobotocore = None

from ..config import Config


class SocketManager:
    """
    Integrates SocketIO with FastAPI app. 
    Adds `sio` property to FastAPI object (app).

    Default mount location for SocketIO app is at `/ws`
    and defautl SocketIO path is `socket.io`.
    (e.g. full path: `ws://www.example.com/ws/socket.io/)

    SocketManager exposes basic underlying SocketIO functionality

    e.g. emit, on, send, call, etc.
    """

    def __init__(
        self,
        app: Optional[FastAPI] = None,
        mount_location: str = "/ws",
        socketio_path: str = "socket.io",
        cors_allowed_origins: Union[str, list] = '*',
        async_mode: str = "asgi"
    ) -> None:
        if Config.REDIS_URL is not None:
            url = Config.REDIS_URL
            urlobj = urlparse(url)
            if not urlobj.path:
                url = f'{url}/0'
            self._mgr = socketio.AsyncRedisManager(url)
        elif Config.SNS_TOPIC_ARN is not None:
            self._mgr = AsyncSQSManager(
                Config.SNS_TOPIC_ARN,
                client_options={
                    "endpoint_url": Config.AWS_ENDPOINT_URL
                },
            )
        else:
            self._mgr = None

        self._sio = socketio.AsyncServer(
            async_mode=async_mode,
            cors_allowed_origins=cors_allowed_origins,
            client_manager=self._mgr,
        )
        self._app = socketio.ASGIApp(
            socketio_server=self._sio,
            socketio_path=socketio_path,
        )

        self.mount_location = mount_location

        if app is not None:
            self.init_app(app)

    def init_app(self, app: FastAPI) -> None:
        app.mount(self.mount_location, self._app)
        app.sio = self._sio

    def is_asyncio_based(self) -> bool:
        return True

    @property
    def on(self):
        return self._sio.on

    @property
    def attach(self):
        return self._sio.attach

    @property
    def emit(self):
        return self._sio.emit

    @property
    def send(self):
        return self._sio.send

    @property
    def call(self):
        return self._sio.call

    @property
    def close_room(self):
        return self._sio.close_room

    @property
    def get_participants(self):
        if self._mgr is not None:
            return self._mgr.get_participants
        return lambda namespace, room: []

    @property
    def get_session(self):
        return self._sio.get_session

    @property
    def save_session(self):
        return self._sio.save_session

    @property
    def session(self):
        return self._sio.session

    @property
    def disconnect(self):
        return self._sio.disconnect

    @property
    def handle_request(self):
        return self._sio.handle_request

    @property
    def start_background_task(self):
        return self._sio.start_background_task

    @property
    def sleep(self):
        return self._sio.sleep

    @property
    def enter_room(self):
        return self._sio.enter_room

    @property
    def leave_room(self):
        return self._sio.leave_room


class AsyncSQSManager(AsyncPubSubManager):
    _queue_name = None
    _session = None

    def __init__(self, topic_arn=None, channel='socketio', write_only=False, logger=None, client_options=None):
        if aiobotocore is None:
            raise RuntimeError('aiobotocore package is not installed '
                               '(Run "pip install aiobotocore" in your virtualenv).')
        self.topic_arn = topic_arn
        self.client_options = client_options or {}
        super().__init__(channel=channel, write_only=write_only, logger=logger)

    @contextlib.asynccontextmanager
    async def awsconnect(self, client):
        async with self.session.create_client(client, **self.client_options) as client:
            yield client

    @property
    def session(self):
        if self._session is None:
            self._session = aiobotocore.session.get_session()
        return self._session

    @property
    def _queue(self):
        if self._queue_name is None:
            self._queue_name = f'{self.channel}-{self.host_id}'
        return self._queue_name

    async def _publish(self, data):
        async with self.awsconnect('sns') as client:
            await client.publish(
                TopicArn=self.topic_arn,
                Message=json.dumps(data),
                Subject="message",
            )

    async def _listen(self):
        async with self.awsconnect('sqs') as client:
            response = await client.create_queue(
                QueueName=self._queue,
            )
            queue_url = response['QueueUrl']

            try:
                response = await client.get_queue_attributes(
                    QueueUrl=queue_url,
                    AttributeNames=['QueueArn'],
                )
                queue_arn = response['Attributes']['QueueArn']

                async with self.awsconnect('sns') as sns_client:
                    await sns_client.subscribe(
                        TopicArn=self.topic_arn,
                        Protocol='sqs',
                        Endpoint=queue_arn,
                    )

                while True:
                    response = await client.receive_message(
                        QueueUrl=queue_url,
                        WaitTimeSeconds=2,
                    )
                    if 'Messages' not in response:
                        continue
                    for message in response['Messages']:
                        await client.delete_message(
                            QueueUrl=queue_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
                        body = json.loads(message['Body'])
                        yield json.loads(body['Message'])
            except BaseException:
                await client.delete_queue(QueueUrl=queue_url)
                raise
