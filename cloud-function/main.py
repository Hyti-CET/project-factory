from flask import Flask, request, jsonify
import jinja2
import json
from google.cloud import pubsub_v1

app = Flask(__name__)

@app.route('/create-project', methods=['POST'])
def create_project():
    data = request.get_json()

    # Validate input fields
    required_fields = ['project_name', 'project_id', 'billing_account_id', 'owner_email']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    # Load and render the Terraform template
    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("terraform_template.tf.j2")
    rendered_template = template.render(data)

    # Save rendered template to file
    with open('/tmp/main.tf', 'w') as f:
        f.write(rendered_template)

    # (Optional) Trigger Cloud Build or other deployment method here

    # Publish status to Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('your-project-id', 'project-creation-status')
    publisher.publish(topic_path, json.dumps({'status': 'Project creation started', 'project_id': data['project_id']}).encode('utf-8'))

    return jsonify({'message': 'Project creation initiated successfully'}), 200

if __name__ == "__main__":
    app.run(debug=True)
