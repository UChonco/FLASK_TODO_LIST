from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simple in-memory database
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        tasks.append(task)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('index'))
@app.route('/edit/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    global tasks
    if request.method == 'POST':
        new_description = request.form.get('task')
        for task in tasks:
            if task['id'] == task_id:
                task['description'] = new_description
                break
        return redirect(url_for('index'))
    
    task_to_edit = next((task for task in tasks if task['id'] == task_id), None)
    if task_to_edit:
        return render_template('edit.html', task=task_to_edit)
    return redirect(url_for('index'))

    
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
