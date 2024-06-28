from autogen import UserProxyAgent

class UserProxyAgentWeb(UserProxyAgent):
    def __init__(self, *args, **lwargs):
        super(UserProxyAgent, self).__init__(*args, **lwargs)
        

    def set_websocket(self, websocket):
        self.websocket = websocket

    async def send(self, message):
        await self.websocket.send_json(message)