from chalice import Chalice
from chalicelib.services import SpannerService
from chalicelib.config import Settings

app = Chalice(app_name='app')
settings = Settings()
service = SpannerService(**settings.model_dump())


@app.route('/singers/{id}')
def get(
    id: str,
):
    return service.get(id)


@app.route('/singers')
def all():
    return service.all()


@app.route('/singers', methods=['POST', 'PUT'])
def update_or_create():
    request = app.current_request
    body = request.json_body
    return service.update_or_create(body)


@app.route('/singers/{id}', methods=['DELETE'])
def delete(
    id: str,
):
    return service.delete(id)
