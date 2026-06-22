from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import csv
import urllib.request
import io
import re
import os
import json
import hashlib
from datetime import time, timezone, timedelta

TOKEN = "8792351236:AAE4VTllcYaaSMVNo4qMfCg_pj49919INsY"


PAYMENT_MSGS = [
    """To set up the pa-yment method, please follow the steps below:

If you would like me to set up the Shopify pa-yment method for you, I would need the following information:

01. Full Name
02. Full Address
03. Date of Birth
04. Social Security Number(SSN)
05. TAX ID
06. Ban-k Account N-umber
07. Residential address document (such as a utility bill, bank statement, or official letter showing your name and address)
08. Identity document (such as a passport, national ID card, or driver’s license)
09. Ph_one Number
10. Shopify store main login.

Or, if you can set up pa-yment gateway from your end. You can see the pa-yment gateway setup instructions, please follow these steps-

>> Go to the Shopify Admin panel
>> Click Settings
>> Click Pa-yment Options

From here, you will see all available pa-yment methods, including Shopify Pa-yments, Pa-yPal, and Manual Pa-yment Methods.

For further assistance, I’ve also provided a helpful video on how to set up the pa-yment method:

Here is this URL: https://docs.google.com/document/d/1shb2g9yXsYfxwzl2-i8McwZfDZ9TcazvkKLsblHHxZk/edit?usp=sharing

Please follow the instructions and set up the pa-yment method on your end. If you encounter any issues or need further assistance, feel free to let me know. I’m here to help and will take care of the rest.

Thank you.""",

    """Here are the p_ayment instructions: 

If you can provide me with the following information, I can set the Shopify pa-yment method for you:

01. Full Name
02. Full Address
03. Date of Birth
04. Social Security Number(SSN)
05. TAX ID
06. Ban-k Account N-umber

If you feel any hesitation in providing the above information, you can set up pa-yment gateway from your end following these steps-

>> Go to the Admin panel
>> Click Settings
>> Click Pa-yment Options

Then you can see all the pa-yment options like Shopify Pa-yment, Pa-ypal, and Manual pa-yment methods.

Also, you can see the video on how you can add the pa-yment method to your store.

Here is this URL:  https://docs.google.com/document/d/1shb2g9yXsYfxwzl2-i8McwZfDZ9TcazvkKLsblHHxZk/edit?usp=sharing

Please follow the instructions and set up the pa_yment method from your end. If you face any issues with that, please let me know.

Thank you.""",

    """P-ayment instructions

Note:  I checked and noticed that you didn't set up your pa-yment getaway to your store. So I've sent you instructions on how can you set up the pa-yment getaway to your store. Please follow the instructions.

For pa-yment method instruction:

To check the pa-yment method, you need to follow some steps: 

 >> Go to the Admin panel
>> Click Settings
>> Click Pa-yment Options

Then you can see all the pa-yment options, like Shopify Pa-yment, Pa-ypal, and Manual pa-yment methods.

Also, you can see the video on how you can add the pa-yment method to your store. Here is the URL: https://docs.google.com/document/d/1MXPahESNwNxFQh-UcLupywqVmZiRqIMVx1DVWgBN_qw/edit?usp=sharing

Please follow the instructions and set up the pa_yment method from your end. If you face any issues with that, please let me know.

Thank you.""",

    """Hi Gilansah,

I trust this message finds you in good health and spirits.

I completely understand your concern, and you are right that you have already paid for the pa-yment method integration. I want to clarify the process from my side, so everything is smooth:

As you know, to connect the pa_yment method on your Shopify store, I need your Shopify main login credentials and your Pa_yPal login credentials. Once I have these, I can immediately set up the pa_yment method for you.

Secondly, if you prefer not to share the login credentials, we can arrange a quick meeting where I can guide you and complete the pa_yment setup directly.

I hope this explains my thinking and the current situation clearly. Please let me know which option works best for you so we can proceed without delay.

Thank you for your understanding and cooperation."""
]


FOLLOWUP_MSGS = [
    """Hi there,

I hope you are doing well.

Do you need any modifications, adjustments, or support from my side? If you need any help, please feel free to let me know.

Or, if everything looks good on your end, please confirm so I can proceed with the project delivery.

Please don’t worry, after delivery, I will provide 30 days of ongoing support. During this time, if you need any modifications or adjustments, feel free to contact me via my Fiverr inbox, and I will take care of everything.

Thank you.""",

    """Hi there,

I hope you're doing well.

I just wanted to check if you had a chance to review the last update I sent. Please review everything and let me know if you'd like any changes or modifications. I’ll be happy to make any adjustments as needed.

You can view the draft here: https://fitestore-2.myshopify.com

Also, If everything looks good, may I deliver the project to you?

No worries about the delivery; you will receive 30 days of ongoing support from me. If you need any modifications, feel free to let me know.

Thank you for your support and cooperation.

Best regards.""",

    """As per your instructions, I—------

1. Note: Also, I've completed all of the tasks on my end. If everything looks good, can I deliver this project to you?

No worries about the project delivery. After delivery, if you need any changes or modifications, you can let me know in my "Fiverr Inbox". I will take care of the rest.

Please let me know your thoughts.

Thank you.""",

    """2. 

Since I have completed all of the tasks and modifications from my end. So, can I deliver the project to you?

No worries about this project. After delivery, I will give 30 days of ongoing support to you. In the support period, if you need any changes or modifications, you can let me know in my "Fiverr inbox". I'll take care of the rest.

Please find the result at your end and let me know your thoughts.

Thank you.""",

    """Hi There,

Hope you are doing well. 

Take your time to review, and whenever you're available, feel free to let me know if you’d like any changes or adjustments. I’m here to refine everything based on your feedback.

If everything looks good, can I deliver this project to you?

No worries about this project. After delivery, I will give you 30 days of ongoing support. In the support period, if you need any changes or modifications, you can let me know in my "Fiverr inbox.". I'll take care of the rest.

Please let me know if you need any changes or modifications.

Thank you."""
]


DELIVERY_MSGS = [
    """Since I have completed all of the tasks, so I am delivering this project to you.

No worries about the delivery. if you need any changes or modifications, please let me know in my "Fiverr inbox" and then I'll work on it and get back to you with an update asap.

Also, you will get 30 days of ongoing support from me. So the delivery will not be a problem.

Feel free to share if you need any changes or modifications I'm happy to modify them. Hope you understand my concern.

Thank you so much.""",

    """--------------------------------------------------------------------------------------------------------------------------------------------------


Since I have completed all tasks from my end, I am delivering this project to you.

No worries about this project. Based on my work, you will get 30 days of ongoing support for this project. In this support period, if you need any changes or modifications, you can let me know in my "Fiverr Inbox". I will take care of the rest.

If everything looks great, please accept the job.

It's a pleasure to work with you, and I hope we'll work together in the future.

Thank you!


--------------------------------------------------------------------------------------------------------------------------------------------------""",

    """Milestore Deliver msg 

Since I have completed the first milestone tasks from my end, I am delivering this project to you.

No worries about this project. in the second milestone, If you need any changes or modifications, you can let me know on my "Fiverr Inbox" or "Order page.". I will take care of the rest.

If everything looks great, please accept the first milestone. I will start working on the second milestone.

Thank you!"""
]


EXTEND_MSGS = [
    """Hi there,

Since the project delivery date is nearing and need your times, I am sending you a delivery date extension.

Please accept the delivery date extension from your end so that we can have a safe project.

Thank you.""",

    """Hi there,

Since you need time to review my work update, I am sending you an extension on the delivery date.

Please accept the delivery date extension from your end so that we can have a safe project.

Thank you.""",

    """Hi there,

I hope you are doing well.

Since you need time to review my work update . The delivery timeline is about to end. So, I'm sending you an extension request.

Please accept the extension request to proceed with the work smoothly.

Thank you."""
]

def parse_timeline_to_hours(timeline_str):
    timeline_str = timeline_str.strip().lower()
    if not timeline_str:
        return 9999
    
    match_days = re.match(r'^(\d+)\s*days?', timeline_str)
    if match_days:
        return int(match_days.group(1)) * 24
    
    days = 0
    hours = 0
    
    d_match = re.search(r'(\d+)\s*d', timeline_str)
    if d_match:
        days = int(d_match.group(1))
        
    h_match = re.search(r'(\d+)\s*h', timeline_str)
    if h_match:
        hours = int(h_match.group(1))
        
    if d_match or h_match or re.search(r'(\d+)\s*m', timeline_str):
        return (days * 24) + hours
        
    return 9999

def get_warning_projects():
    url = 'https://docs.google.com/spreadsheets/d/1IRIDbowvg0qM9wqNMxegwqz4jNGl6bj9UThL0NjYScQ/export?format=csv'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        content = response.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(content))
        results = []
        for row in reader:
            timeline_str = row.get('Timeline', '')
            hours = parse_timeline_to_hours(timeline_str)
            if hours <= 48:
                results.append(row)
        return results
    except Exception as e:
        print(f"Error fetching sheet: {e}")
        return []

CHAT_ID_FILE = 'group_chat_id.txt'

def save_chat_id(chat_id):
    with open(CHAT_ID_FILE, 'w') as f:
        f.write(str(chat_id))

def get_chat_id():
    if os.path.exists(CHAT_ID_FILE):
        with open(CHAT_ID_FILE, 'r') as f:
            return int(f.read().strip())
    return None

async def set_group(update, context):
    chat_id = update.message.chat_id
    save_chat_id(chat_id)
    await update.message.reply_text("This group has been registered to receive daily 8:00 AM warnings!")

async def test_warning(update, context):
    chat_id = update.message.chat_id
    await update.message.reply_text("Checking for projects with <= 48h timeline...")
    projects = get_warning_projects()
    if not projects:
        await update.message.reply_text("No projects found with <= 48 hours timeline!")
        return
    await send_warnings_to_chat(context, chat_id, projects)

async def daily_warning_job(context: ContextTypes.DEFAULT_TYPE):
    chat_id = get_chat_id()
    if chat_id:
        projects = get_warning_projects()
        if projects:
            await send_warnings_to_chat(context, chat_id, projects)

async def send_warnings_to_chat(context, chat_id, projects):
    msg_chunks = []
    current_chunk = "⚠️ <b>WARNING: Projects with <= 48 Hours Timeline</b> ⚠️\n\n"
    for r in projects:
        part = f"👤 Client: {r.get('Client Name', '') or 'N/A'}\n"
        part += f"👥 Team: {r.get('Assign Team', '') or 'N/A'}\n"
        part += f"📊 Status: {r.get('Status', '') or 'N/A'}\n"
        part += f"⏳ Timeline: {r.get('Timeline', '') or 'N/A'}\n"
        part += "---------------------------------------\n"
        
        if len(current_chunk) + len(part) > 4000:
            msg_chunks.append(current_chunk)
            current_chunk = part
        else:
            current_chunk += part
            
    if current_chunk:
        msg_chunks.append(current_chunk)
        
    for chunk in msg_chunks:
        try:
            await context.bot.send_message(chat_id=chat_id, text=chunk, parse_mode='HTML')
        except Exception as e:
            print(f"Failed to send warning: {e}")


def search_projects(name):
    url = 'https://docs.google.com/spreadsheets/d/1IRIDbowvg0qM9wqNMxegwqz4jNGl6bj9UThL0NjYScQ/export?format=csv'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        content = response.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(content))
        results = []
        name_lower = name.lower()
        for row in reader:
            assign_team = row.get('Assign Team', '')
            if name_lower in assign_team.lower():
                results.append(row)
        return results
    except Exception as e:
        print(f"Error fetching sheet: {e}")
        return None

def format_project_results(name, results):
    if not results:
        return None
    
    msg_chunks = []
    current_chunk = f"Projects for {name}:\n\n"
    for r in results:
        client_name = r.get('Client Name', '') or 'N/A'
        assign_team = r.get('Assign Team', '')
        names = [n.strip() for n in assign_team.split('/') if n.strip()]
        other_names = [n for n in names if n.lower() != name.lower()]
        if other_names:
            client_name += f" (Shared with {', '.join(other_names)})"
            
        part = f"👤 Client: {client_name}\n"
        part += f"📁 Profile: {r.get('Profile Name', '') or 'N/A'}\n"
        part += f"🏷️ Order ID: {r.get('Order ID', '') or 'N/A'}\n"
        part += f"📊 Status: {r.get('Status', '') or 'N/A'}\n"
        part += f"💰 Value: {r.get('Value', '') or 'N/A'}\n"
        part += f"⏳ Timeline: {r.get('Timeline', '') or 'N/A'}\n"
        part += f"🔗 Link: {r.get('Spreadsheet Link', '') or 'N/A'}\n"
        part += "---------------------------------------\n"
        
        if len(current_chunk) + len(part) > 4000:
            msg_chunks.append(current_chunk)
            current_chunk = part
        else:
            current_chunk += part
            
    if current_chunk:
        msg_chunks.append(current_chunk)
        
    return msg_chunks


def get_cc_issues():
    url = 'https://docs.google.com/spreadsheets/d/1ic9UMVX0FFsAyz0TZ-_lGKj_D9NornoGhq38KTRtM54/export?format=csv&gid=1412843338'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        content = response.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(content))
        results = []
        for row in reader:
            assign_name = row.get('Assign Name', '')
            if '/CC' in assign_name:
                results.append(row)
        return results
    except Exception as e:
        print(f"Error fetching issues sheet: {e}")
        return None

def format_issue_results(results):
    if not results:
        return ["No issues found with /CC in Assign Name."]
    
    from collections import defaultdict
    
    grouped = defaultdict(list)
    for r in results:
        assign_raw = r.get('Assign Name', '')
        emp_names_str = assign_raw.replace('/CC', '').replace('/cc', '').strip()
        names = [n.strip() for n in emp_names_str.split('/') if n.strip()]
        for emp_name in names:
            grouped[emp_name].append(r)
            
    employees = sorted(list(grouped.keys()))
    if not employees:
        return ["No issues found."]
        
    msg_chunks = []
    current_chunk = "📋 <b>Pending /CC Issues</b> 📋\n\n"
    
    THEMES = ["🔴", "🔵", "🟢", "🟠", "🟣", "🟤", "⚫", "⚪"]
    
    for i, emp_name in enumerate(employees):
        theme_emoji = THEMES[i % len(THEMES)]
        issues = grouped[emp_name]
        
        part = f"{theme_emoji} <b>Employee: {emp_name}</b> <i>(Total: {len(issues)})</i>\n"
        part += "<blockquote>"
        
        for idx, iss in enumerate(issues):
            client_key = "Client's Name"
            client_name = iss.get(client_key, '') or 'N/A'
            
            assign_raw = iss.get('Assign Name', '')
            orig_names = [n.strip() for n in assign_raw.replace('/CC', '').replace('/cc', '').strip().split('/') if n.strip()]
            other_names = [n for n in orig_names if n.lower() != emp_name.lower()]
            if other_names:
                client_name += f" (+{','.join(other_names)})"
                
            note = iss.get('Special Notes', '') or 'N/A'
            note_lower = note.lower().strip()
            
            part += f"👤 <b>Client: {client_name}</b>\n"
            
            if note_lower and note_lower != 'need to check' and note_lower != 'n/a':
                part += f"🚨 <b>Note: {note}</b> 🚨\n"
            else:
                part += f"📝 <b>Note:</b> {note}\n"
            
            if idx < len(issues) - 1:
                part += "〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"
                
        part += "</blockquote>\n"
        
        if len(current_chunk) + len(part) > 4000:
            msg_chunks.append(current_chunk)
            current_chunk = part
        else:
            current_chunk += part
            
    if current_chunk:
        msg_chunks.append(current_chunk)
        
    return msg_chunks

async def handle_issue(update, context):
    await update.message.reply_text("Fetching /CC issues...")
    results = get_cc_issues()
    if results is None:
        await update.message.reply_text("Failed to fetch issues.")
        return
        
    formatted_chunks = format_issue_results(results)
    for chunk in formatted_chunks:
        await update.message.reply_text(chunk, parse_mode='HTML', disable_web_page_preview=True)



async def start(update, context):
    await update.message.reply_text(
        "Commands:\n\npayment\nfollowup\ndelivery\nextend"
    )

ALERTS_FILE = "alerts.json"
NOTIFIED_FILE = "notified_issues.json"

def load_alerts():
    if os.path.exists(ALERTS_FILE):
        try:
            with open(ALERTS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_alerts(data):
    with open(ALERTS_FILE, 'w') as f:
        json.dump(data, f)

def load_notified():
    if os.path.exists(NOTIFIED_FILE):
        try:
            with open(NOTIFIED_FILE, 'r') as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_notified(data):
    with open(NOTIFIED_FILE, 'w') as f:
        json.dump(list(data), f)

async def alerton(update, context):
    if not context.args:
        await update.message.reply_text("Please provide your name exactly as it appears in the sheet. Example: /alerton Refayet")
        return
        
    name = context.args[0]
    chat_id = update.effective_chat.id
    
    alerts = load_alerts()
    alerts[name.lower()] = chat_id
    save_alerts(alerts)
    
    await update.message.reply_text(f"✅ Success! You will now receive automatic notifications for issues assigned to '{name}/CC'.")

async def check_new_issues(context: ContextTypes.DEFAULT_TYPE):
    results = get_cc_issues()
    if not results:
        return
        
    alerts = load_alerts()
    if not alerts:
        return
        
    notified = load_notified()
    new_notified = False
    
    for r in results:
        client_name = r.get("Client's Name", '') or 'N/A'
        profile_name = r.get("Profile Name", '') or 'N/A'
        note = r.get('Special Notes', '') or 'N/A'
        link = r.get('Conversation Page URL', '') or '#'
        
        # Create a unique hash for the issue
        issue_str = f"{client_name}|{profile_name}".encode('utf-8')
        issue_hash = hashlib.md5(issue_str).hexdigest()
        
        if issue_hash in notified:
            continue
            
        assign_raw = r.get('Assign Name', '')
        emp_names_str = assign_raw.replace('/CC', '').replace('/cc', '').strip()
        names = [n.strip() for n in emp_names_str.split('/') if n.strip()]
        
        for emp_name in names:
            emp_lower = emp_name.lower()
            if emp_lower in alerts:
                chat_id = alerts[emp_lower]
                
                other_names = [n for n in names if n.lower() != emp_lower]
                client_display = client_name
                if other_names:
                    client_display += f" (+{','.join(other_names)})"
                    
                note_lower = note.lower().strip()
                if note_lower and note_lower != 'need to check' and note_lower != 'n/a':
                    note_display = f"🚨 <b>Note: {note}</b> 🚨"
                else:
                    note_display = f"📝 <b>Note:</b> {note}"
                
                msg = f"🚨 <b>New Issue Assigned to You!</b> 🚨\n\n"
                msg += f"👤 <b>Client: {client_display}</b>\n"
                msg += f"{note_display}\n"
                msg += f"🔗 <b>Link:</b> <a href='{link}'>Click Here</a>"
                
                try:
                    await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode='HTML', disable_web_page_preview=True)
                except Exception as e:
                    print(f"Failed to send alert to {emp_name}: {e}")
        
        notified.add(issue_hash)
        new_notified = True
        
    if new_notified:
        save_notified(notified)


async def reply(update, context):
    text = update.message.text.lower()

    if text.startswith('/'):
        # Ignore actual registered commands so they don't trigger name searches
        if text.startswith(('/start', '/setgroup', '/testwarning', '/issue', '/alerton')):
            return
        # Strip the slash so it can be searched as a name
        text = text[1:]

    if text == "payment":
        for msg in PAYMENT_MSGS:
            await update.message.reply_text(msg)

    elif text == "followup":
        for msg in FOLLOWUP_MSGS:
            await update.message.reply_text(msg)

    elif text == "delivery":
        for msg in DELIVERY_MSGS:
            await update.message.reply_text(msg)

    elif text == "extend":
        for msg in EXTEND_MSGS:
            await update.message.reply_text(msg)

    else:
        if len(text) >= 2:
            results = search_projects(text)
            formatted_chunks = format_project_results(update.message.text, results)
            if formatted_chunks:
                for chunk in formatted_chunks:
                    await update.message.reply_text(chunk, disable_web_page_preview=True)
                return
                
        await update.message.reply_text("Command not found or no projects found for this name.")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setgroup", set_group))
app.add_handler(CommandHandler("testwarning", test_warning))
app.add_handler(CommandHandler("issue", handle_issue))
app.add_handler(CommandHandler("alerton", alerton))
app.add_handler(MessageHandler(filters.TEXT | filters.COMMAND, reply))

bd_timezone = timezone(timedelta(hours=6))
target_time = time(hour=8, minute=0, tzinfo=bd_timezone)

app.job_queue.run_daily(daily_warning_job, time=target_time)

# Run issue checker every 60 seconds
app.job_queue.run_repeating(check_new_issues, interval=60, first=10)

print("Bot Running...")
app.run_polling()