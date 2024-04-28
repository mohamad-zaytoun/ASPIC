from flask import render_template, request, redirect, url_for
from .models import Literal, Rule , contraposition
from . import app  # This import is correct if you defined `app` in __init__.py

# This list will store our rules in memory
rules_list = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # When the form is submitted, we retrieve data from the form fields
        premises_input = request.form.get('premises')
        conclusion_input = request.form.get('conclusion')
        is_defeasible_input = request.form.get('is_defeasible') == 'true'
        reference_input = request.form.get('reference')

        # Process the premises into Literal objects, split by comma
        premises = []
        if premises_input:
            for item in premises_input.split(','):
                item = item.strip()
                is_negative = item.startswith('!')
                if is_negative:
                    item = item.lstrip('!')  # Remove the negation sign to get the literal name
                premises.append(Literal(item, is_negative))

        # Create the conclusion Literal object
        conclusion_is_negative = conclusion_input.startswith('!')
        if conclusion_is_negative:
            conclusion_input = conclusion_input.lstrip('!')
        conclusion = Literal(conclusion_input, conclusion_is_negative)

        reference = Literal(reference_input) if reference_input else None

        # Create a new Rule object
        new_rule = Rule(premises, conclusion, is_defeasible_input, reference)
        rules_list.append(new_rule)

        # Redirect back to the home page, which will show the form again
        return redirect(url_for('index'))

    # Render the index.html template
    # If it's a GET request, it just shows the form.
    # If it's a POST request, it shows the form and updates the list of rules.
    return render_template('index.html', rules=rules_list)

@app.route('/view-rules', methods=['GET'])
def view_rules():
    # Simply render a new template that will list all rules
    return render_template('view-rules.html', rules=rules_list)


@app.route('/generate-contrapositions', methods=['POST'])
def generate_contrapositions():
    new_rules = []
    for rule in rules_list:
        if not rule.is_defeasible:  # Only generate for strict rules
            try:
                contrapositives = contraposition(rule)
                new_rules.extend(contrapositives)
            except ValueError as e:
                # You can handle errors more gracefully here if needed
                print(e)
    rules_list.extend(new_rules)
    return redirect(url_for('view_rules'))
# Run the app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)
