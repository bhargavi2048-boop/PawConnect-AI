from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import csv
import os
import json
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'pawconnect_secret_2024'

COMPLAINTS_CSV = 'data/complaints.csv'
VOLUNTEERS_CSV = 'data/volunteers.csv'

COMPLAINTS_HEADERS = ['id', 'complaint_no', 'name', 'mobile', 'location', 'lat', 'lng',
                       'complaint_type', 'description', 'photo', 'status', 'timestamp']
VOLUNTEERS_HEADERS = ['id', 'name', 'mobile', 'location', 'help_type', 'timestamp']

def init_csv():
    os.makedirs('data', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    if not os.path.exists(COMPLAINTS_CSV):
        with open(COMPLAINTS_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(COMPLAINTS_HEADERS)
    if not os.path.exists(VOLUNTEERS_CSV):
        with open(VOLUNTEERS_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(VOLUNTEERS_HEADERS)

def read_csv(filepath):
    rows = []
    if os.path.exists(filepath):
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
    return rows

def write_csv_row(filepath, headers, row_data):
    file_exists = os.path.exists(filepath)
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_data)

def get_next_complaint_no():
    complaints = read_csv(COMPLAINTS_CSV)
    return f"PC{len(complaints)+1:03d}"

def update_complaint_status(complaint_id, new_status):
    complaints = read_csv(COMPLAINTS_CSV)
    for c in complaints:
        if c['id'] == complaint_id:
            c['status'] = new_status
    with open(COMPLAINTS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COMPLAINTS_HEADERS)
        writer.writeheader()
        writer.writerows(complaints)

# ─── CHATBOT LOGIC ─────────────────────────────────────────────────────────────
CHATBOT_RESPONSES = {
    "food": {
        "keywords": ["food", "feed", "eat", "hungry", "give", "feeding"],
        "response": "🍖 <strong>Safe foods for stray dogs:</strong><br>• Cooked rice with boiled vegetables<br>• Plain boiled chicken (no bones)<br>• Chapati / plain bread<br>• Fresh clean water (most important!)<br><br>⚠️ <strong>Avoid:</strong> chocolate, onions, grapes, spicy food, salty snacks, or anything with artificial sweeteners (xylitol).<br><br>💡 Feeding twice daily at consistent times helps dogs trust humans."
    },
    "injured": {
        "keywords": ["injured", "hurt", "wound", "bleeding", "broken", "accident", "hit"],
        "response": "🚨 <strong>If a dog is injured:</strong><br>1. Stay calm and approach slowly — don't startle them<br>2. Don't try to remove embedded objects<br>3. Cover wounds gently with a clean cloth<br>4. Call a local animal welfare helpline immediately<br>5. Use our <a href='/report' class='chat-link'>Report Page</a> to alert volunteers<br><br>📞 <strong>National Animal Helpline (India):</strong> 1962<br>🏥 Contact your nearest animal hospital or Blue Cross Society."
    },
    "sick": {
        "keywords": ["sick", "ill", "disease", "vomit", "diarrhea", "cough", "limp", "mange", "infection"],
        "response": "🏥 <strong>If a dog appears sick:</strong><br>• Keep a safe distance — some illnesses are contagious<br>• Do NOT attempt home treatment or diagnosis<br>• Report via our <a href='/report' class='chat-link'>Complaint Form</a> for medical volunteers<br>• Watch for signs: lethargy, not eating, discharge, skin lesions<br><br>⚠️ <em>PawConnect AI does not provide medical diagnoses. Always consult a licensed veterinarian.</em>"
    },
    "contact": {
        "keywords": ["contact", "organization", "ngo", "welfare", "helpline", "number", "call", "reach"],
        "response": "📋 <strong>Animal Welfare Contacts (India):</strong><br>• <strong>Animal Welfare Board of India:</strong> awbi.gov.in<br>• <strong>PFA (People for Animals):</strong> 1800-11-4100<br>• <strong>Blue Cross of India:</strong> +91-44-22350170<br>• <strong>SPCA India:</strong> spca.in<br>• <strong>National Helpline:</strong> 1962<br><br>🔍 Search 'animal shelter near me' for local resources."
    },
    "help": {
        "keywords": ["help", "volunteer", "rescue", "contribute", "support", "join", "donate"],
        "response": "💪 <strong>Ways you can help stray dogs:</strong><br>• 🍽️ <strong>Feed regularly</strong> — set up a community feeding station<br>• 💉 <strong>Support sterilization</strong> — ABC programs reduce overpopulation<br>• 🏠 <strong>Foster</strong> — provide temporary shelter<br>• 📢 <strong>Spread awareness</strong> — share our platform<br>• 👤 <strong>Register as Volunteer</strong> — <a href='/volunteer' class='chat-link'>Join here</a><br>• 💰 <strong>Donate</strong> to registered animal NGOs"
    },
    "report": {
        "keywords": ["report", "complaint", "submit", "register", "found", "stray", "missing"],
        "response": "📝 <strong>To report a stray dog concern:</strong><br>1. Go to our <a href='/report' class='chat-link'>Report a Dog</a> page<br>2. Fill in your name, location, and issue type<br>3. Add a photo if possible<br>4. Submit — our team will respond within 2 hours<br><br>✅ Your report is stored securely and assigned to the nearest volunteer or NGO."
    },
    "default": {
        "response": "🐾 Hello! I'm <strong>PawBot</strong>, your animal welfare assistant!<br><br>I can help you with:<br>• 🍖 What to feed stray dogs<br>• 🚨 What to do for injured/sick dogs<br>• 📞 Animal welfare organization contacts<br>• 💪 How to volunteer and help<br>• 📝 How to report an issue<br><br>Just type your question and I'll guide you!"
    }
}

def get_chatbot_response(user_message):
    msg = user_message.lower().strip()
    for key, data in CHATBOT_RESPONSES.items():
        if key == 'default':
            continue
        if any(kw in msg for kw in data['keywords']):
            return data['response']
    return CHATBOT_RESPONSES['default']['response']

# ─── ROUTES ────────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    complaints = read_csv(COMPLAINTS_CSV)
    volunteers = read_csv(VOLUNTEERS_CSV)
    rescued = sum(1 for c in complaints if c.get('status') in ('Rescued', 'Closed'))
    stats = {
        'total_complaints': len(complaints),
        'total_volunteers': len(volunteers),
        'pending': sum(1 for c in complaints if c.get('status') in ('Submitted', 'Pending', 'In Progress')),
        'resolved': rescued,
        'animals_rescued': rescued,
    }
    return render_template('home.html', stats=stats)

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        mobile = request.form.get('mobile', '').strip()
        location = request.form.get('location', '').strip()
        lat = request.form.get('lat', '').strip()
        lng = request.form.get('lng', '').strip()
        complaint_type = request.form.get('complaint_type', '').strip()
        description = request.form.get('description', '').strip()

        if not all([name, mobile, location, complaint_type]):
            flash('Please fill all required fields.', 'danger')
            return redirect(url_for('report'))

        photo_filename = ''
        photo = request.files.get('photo')
        if photo and photo.filename:
            ext = photo.filename.rsplit('.', 1)[-1].lower()
            if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                photo_filename = f"{uuid.uuid4().hex}.{ext}"
                photo.save(os.path.join('static/uploads', photo_filename))

        complaint_no = get_next_complaint_no()
        row = {
            'id': uuid.uuid4().hex[:8].upper(),
            'complaint_no': complaint_no,
            'name': name,
            'mobile': mobile,
            'location': location,
            'lat': lat,
            'lng': lng,
            'complaint_type': complaint_type,
            'description': description,
            'photo': photo_filename,
            'status': 'Submitted',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        write_csv_row(COMPLAINTS_CSV, COMPLAINTS_HEADERS, row)
        flash(f'✅ Report submitted! Your Complaint ID: <strong>{complaint_no}</strong>. We will respond within 2 hours.', 'success')
        return redirect(url_for('report'))

    return render_template('report.html')

@app.route('/volunteer', methods=['GET', 'POST'])
def volunteer():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        mobile = request.form.get('mobile', '').strip()
        location = request.form.get('location', '').strip()
        help_type = request.form.get('help_type', '').strip()

        if not all([name, mobile, location, help_type]):
            flash('Please fill all required fields.', 'danger')
            return redirect(url_for('volunteer'))

        row = {
            'id': uuid.uuid4().hex[:8].upper(),
            'name': name,
            'mobile': mobile,
            'location': location,
            'help_type': help_type,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        write_csv_row(VOLUNTEERS_CSV, VOLUNTEERS_HEADERS, row)
        flash(f'🎉 Welcome aboard! You are registered as a <strong>{help_type}</strong>. Thank you for your kindness!', 'success')
        return redirect(url_for('volunteer'))

    volunteers = read_csv(VOLUNTEERS_CSV)
    return render_template('volunteer.html', volunteers=volunteers)

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message.strip():
        return jsonify({'response': 'Please type a message!'})
    response = get_chatbot_response(user_message)
    return jsonify({'response': response})

@app.route('/admin')
def admin():
    complaints = read_csv(COMPLAINTS_CSV)
    volunteers = read_csv(VOLUNTEERS_CSV)

    # Analytics data
    type_counts = {}
    monthly_counts = {}
    for c in complaints:
        ct = c.get('complaint_type', 'Other')
        type_counts[ct] = type_counts.get(ct, 0) + 1
        ts = c.get('timestamp', '')
        if ts:
            try:
                month = datetime.strptime(ts[:7], '%Y-%m').strftime('%b %Y')
                monthly_counts[month] = monthly_counts.get(month, 0) + 1
            except:
                pass

    rescued = sum(1 for c in complaints if c.get('status') in ('Rescued', 'Closed'))
    stats = {
        'total_complaints': len(complaints),
        'total_volunteers': len(volunteers),
        'pending': sum(1 for c in complaints if c.get('status') in ('Submitted', 'Pending')),
        'in_progress': sum(1 for c in complaints if c.get('status') == 'In Progress'),
        'rescued': rescued,
        'closed': sum(1 for c in complaints if c.get('status') == 'Closed'),
        'animals_rescued': rescued,
    }

    # Map data — complaints with coords
    map_complaints = [c for c in complaints if c.get('lat') and c.get('lng')]

    return render_template('admin.html',
        complaints=complaints,
        volunteers=volunteers,
        stats=stats,
        type_counts=json.dumps(type_counts),
        monthly_counts=json.dumps(monthly_counts),
        map_complaints=json.dumps(map_complaints))

@app.route('/admin/update_status', methods=['POST'])
def update_status():
    complaint_id = request.form.get('complaint_id')
    new_status = request.form.get('status')
    valid = ['Submitted', 'In Progress', 'Rescued', 'Closed']
    if complaint_id and new_status in valid:
        update_complaint_status(complaint_id, new_status)
        flash(f'Status updated to <strong>{new_status}</strong>.', 'success')
    return redirect(url_for('admin'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('✅ Thank you for your message! We will get back to you within 24 hours.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/track')
def track():
    complaint_no = request.args.get('id', '').strip().upper()
    found = None
    if complaint_no:
        complaints = read_csv(COMPLAINTS_CSV)
        for c in complaints:
            if c.get('complaint_no', '').upper() == complaint_no or c.get('id', '').upper() == complaint_no:
                found = c
                break
    return render_template('track.html', complaint=found, searched=bool(complaint_no), query=complaint_no)

if __name__ == '__main__':
    init_csv()
    import os
port = int(os.environ.get("PORT", 5000))
app.run(debug=False, host="0.0.0.0", port=port)
