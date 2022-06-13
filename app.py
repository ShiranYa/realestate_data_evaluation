import os

from flask import Flask, request, Response, send_from_directory
from proparty_list_evaluation import is_evaluation_succeeded

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_real_estate_evaluation():
	params = request.args.to_dict()
	is_completed = is_evaluation_succeeded(params)
	if not is_completed:
		return Response('not found', status=404)
	directory = os.path.dirname('property_evaluation.pdf')
	filename = os.path.basename('property_evaluation.pdf')

	return send_from_directory(directory, filename)


if __name__ == '__main__':
	app.run(debug=True)
