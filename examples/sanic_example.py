from sanic import Sanic, Blueprint
from sanic.response import json

from pythondi import Provider, configure, inject
from .repo import Repo, SQLRepo

bp = Blueprint('home', url_prefix='/')


@bp.route('/')
async def home(request):
    usecase = Usecase()
    usecase.repo.get()
    return json({'hello': 'world'})


class Usecase:
    @inject()
    def __init__(self, repo: Repo):
        self.repo = repo


def create_app():
    provider = Provider()
    provider.bind(Repo, SQLRepo)
    configure(provider=provider)
    app = Sanic(__name__)
    app.blueprint(bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
