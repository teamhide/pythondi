from flask import Flask, Blueprint, jsonify

from pythondi import Provider, configure, inject
from .repo import Repo, SQLRepo

bp = Blueprint('home', __name__)


@bp.route('/')
def home():
    usecase = Usecase()
    usecase.repo.get()
    return jsonify({'hello': 'world'})


class Usecase:
    @inject()
    def __init__(self, repo: Repo):
        self.repo = repo


def create_app():
    provider = Provider()
    provider.bind(Repo, SQLRepo)
    configure(provider=provider)
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
