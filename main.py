from flask import Flask, request
from flask import jsonify
from flask.views import MethodView
from models import Session, Post

app = Flask('site')


class HttpError(Exception):
    def __init__(self, status_code: int, error_mes: str | dict | list):
        self.status_code = status_code
        self.error_mes = error_mes


def get_post_by_id(session: Session, announcement_id: int):
    post = session.get(Post, announcement_id)
    if post is None:
        raise HttpError(404, 'post not found')
    return post


@app.errorhandler(HttpError)
def error_handler(err):
    http_response = jsonify({"error": err.error_mes})
    http_response.status_code = err.status_code
    return http_response


class AnnouncementView(MethodView):
    def post(self):
        json_data = request.json
        with Session as session:
            post = Post(**json_data)
            session.add(post)
            session.commit()
            return jsonify(post.post_id)

    def get(self, announcement_id: int):
        with Session as session:
            post = get_post_by_id(session, announcement_id)
            return jsonify(post.dict)

    def delete(self, announcement_id: int):
        with Session as session:
            post = get_post_by_id(session, announcement_id)
            session.delete(post)
            session.commit()
        return jsonify({'status': 'delete'})

    def patch(self, announcement_id: int):
        json_data = request.json
        with Session as session:
            post = get_post_by_id(session, announcement_id)
            for key, value in json_data.items():
                setattr(post, key, value)
            session.add(post)
            session.commit()
            return jsonify(post.post_id)


announcement_view = AnnouncementView.as_view('announcement')

app.add_url_rule(
    '/announcement/<int:announcement_id>',
    view_func=announcement_view,
    methods=["GET", "PATCH", "DELETE"],
)
app.add_url_rule(
    '/announcement',
    view_func=announcement_view,
    methods=["POST"],
)

app.run()
