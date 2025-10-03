from flask import Flask, request, jsonify
import pyautogui
import time
import os
import subprocess

app = Flask(__name__)

# File path for saving
file_path = os.path.join(os.path.expanduser("~"), "Desktop", "VijayUIAutomationDemo.txt")

def open_notepad():
    """Open a new Notepad window"""
    subprocess.Popen(["notepad.exe"])
    time.sleep(2)

def open_notepad_with_file(file):
    """Open Notepad with an existing file"""
    subprocess.Popen(["notepad.exe", file])
    time.sleep(2)

@app.route('/write-text', methods=['POST'])
def write_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' in payload"}), 400

        user_input = data['text']

        # Check if file exists
        if not os.path.exists(file_path):
            open_notepad()
            pyautogui.typewrite(user_input)
            time.sleep(1)

            # Save file
            pyautogui.hotkey('ctrl', 's')
            time.sleep(2)
            pyautogui.typewrite(file_path)
            time.sleep(1)
            pyautogui.press('enter')

            return jsonify({
                "status": "created",
                "message": f"File created and saved at {file_path}"
            })

        else:
            open_notepad_with_file(file_path)

            # Move cursor to end and add a new line
            pyautogui.hotkey('ctrl', 'end')
            pyautogui.press('enter')
            pyautogui.typewrite(user_input)
            time.sleep(1)

            # Save
            pyautogui.hotkey('ctrl', 's')

            return jsonify({
                "status": "appended",
                "message": f"Text appended and file saved at {file_path}"
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


