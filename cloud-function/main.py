from flask import Flask, request, jsonify
import jinja2
import os
import json
from google.cloud import pubsub_v1

app = Flask(__name__)

@app.route('/create-project', methods=['POST'])
def create_project():
    data = request.get_json()

    # Validate required fields
    required_fields = ['project_name', 'project_id', 'billing_account_id', 'owner_email', 'vpc_name']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'Missing field: {field}'}), 400

    # Load and render the Jinja2 template
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("main.tf.j2")
    rendered_template = template.render(data=data)

    # Save the rendered Terraform file
    with open('/tmp/main.tf', 'w') as f:
        f.write(rendered_template)

    # Publish a status to Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('your-project-id', 'project-creation-status')
    message_data = json.dumps({'status': 'Project creation started', 'project_id': data['project_id']}).encode('utf-8')
    publisher.publish(topic_path, message_data)

    return jsonify({'message': 'Project creation initiated'}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
