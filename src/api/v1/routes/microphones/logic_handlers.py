from src.bases.api.routes import RouteLogicHandler
from src.clients.dcerno import DcernoClient
from config import DCERNO_CONFIG


class MicrophoneLogicHandler(RouteLogicHandler):
    def run(self):
        client = DcernoClient(
            host=DCERNO_CONFIG['host'],
            port=DCERNO_CONFIG['port']
        )
        data = client.get_all_units()
        return dict(micros=data['s'])