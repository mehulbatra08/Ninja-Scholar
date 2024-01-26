from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://mehulbtr:ramlal@cluster1.lnn8pvu.mongodb.net/?retryWrites=true&w=majority"
mongo = PyMongo(app).cx["subjects"]
# db = g.coin_markets = PyMongo(current_app).cx["your_database_name"]


subjects_collection = mongo.db.subjects

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/select_subjects', methods=['POST'])
def select_subjects():
    if request.method == 'POST':
        branch = request.form['branch']
        semester = request.form['semester']

        subjects = subjects_collection.find({'Semester_name': semester,'branch_name':branch})
        return render_template('subject_listing.html', subjects=subjects,semester=semester)
    

@app.route('/subject/<string:subject_id>')
def subject_details(subject_id):
    subject = subjects_collection.find_one({'_id': ObjectId(subject_id)})
    return render_template('subject_details.html', subject=subject)
# @app.route('/subject/<string:subject_id>')
# def subject_details(subject_id):
#     subject = subjects_collection.find_one({'_id': ObjectId(subject_id)})
#     return render_template('subject_details.html', subject=subject)

@app.route('/add_document', methods=['POST'])
def add_document():
    if request.method == 'POST':
        subject_name = request.form['subject_name']
        branch_name = request.form['branch_name']
        semester_name = request.form['semester']
        unit_1 = request.form['unit_1']
        unit_2 = request.form['unit_2']
        unit_3 = request.form['unit_3']
        unit_4 = request.form['unit_4']
        pyq = request.form['pyq']

        # Create a list to store drive link details
        drive_links = []

        # Get lists of drive link names and drive links from the form
        drive_link_names = request.form.getlist('drive_link_names')
        drive_links_list = request.form.getlist('drive_links')

        # Iterate through the lists and create dictionaries
        for name, link in zip(drive_link_names, drive_links_list):
            drive_link = {'name': name, 'link': link}
            drive_links.append(drive_link)

        new_subject = {
            'subject_name': subject_name,
            'branch_name': branch_name,
            'Semester_name': semester_name,
            'unit_1': unit_1,
            'unit_2': unit_2,
            'unit_3': unit_3,
            'unit_4': unit_4,
            'pyq': pyq,
            'drive_links': drive_links
        }

        subjects_collection.insert_one(new_subject)

    return redirect(url_for('home'))


@app.route('/add_subject', methods = ['GET'])
def add_subject():
    return render_template('add_subject.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)






