from flask import Flask, render_template, request, redirect, url_for, flash
import re
import requests
import os
app = Flask(__name__)
app.secret_key = "a3k7$#1r9!2jdlNcmwQ^z"  # Add this line!
app.config['DOWNLOAD_FOLDER'] = 'static/downloads'
app.config['ALLOWED_EXTENSIONS'] = {'mp4'}
# Ensure download directory exists
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)
def download_video(video_url):
    try:
        headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}
        # Send a GET request to the video URL
        os.system('cls')
        print("Downloading video from: ", video_url)
        response = requests.get(video_url, headers=headers).text.replace('\\','')
        try:
            browser_native_hd_url= re.search(r'"browser_native_hd_url":"(.*?)"', response).group(1)
            output_file = "facebook_video.mp4"
        except :
            browser_native_hd_url= re.search(r'"image":{"uri":"(.*?)"', response).group(1)
            output_file = "facebook_photo.jpg"
        print(browser_native_hd_url)
        # open('tempss.txt', 'w' ,encoding= 'utf-8').write(response)
        # Download the video
        response = requests.get(browser_native_hd_url, stream=True)
        filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], output_file)
        if response.status_code == 200:
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                    if chunk:
                        f.write(chunk)
            print("✅ Download complete:", output_file)
            return filepath
        else:
            print("❌ Failed to download, status code:", response.status_code)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("video_url", "").strip()

        if not video_url:
            flash("Please enter a valid Facebook video URL.", "error")
            return redirect(url_for("index"))
            
        # Validate Facebook URL
        if not any(domain in video_url for domain in ['facebook.com', 'fb.watch']):
            flash("Please enter a valid Facebook video URL.", "error")
            return redirect(url_for("index"))
        # Try to download the video
        filename = download_video(video_url)
        
        if not filename:
            flash("Could not download video. Please check the URL and try again.", "error")
            return redirect(url_for("index"))
            
        # In a real app, you would serve the actual downloaded file
        # For demo, we'll just show a success message
        # download_link = url_for('static', filename=filename)
        flash("Video downloaded successfully!", "success")
        return render_template("index.html", download_link=filename)

    return render_template("index.html", download_link=None)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
