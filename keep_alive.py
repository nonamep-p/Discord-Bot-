
try:
    from flask import Flask
    import threading
    import time

    app = Flask(__name__)

    @app.route('/')
    def home():
        return "🤖 Kaala Billota Bot is online!"

    @app.route('/health')
    def health():
        return {"status": "healthy", "timestamp": time.time()}

    @app.route('/ping')
    def ping():
        return "pong"

    def run():
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

    def keep_alive():
        """Start the keep-alive web server"""
        try:
            thread = threading.Thread(target=run)
            thread.daemon = True
            thread.start()
            print("✅ Keep-alive server started on port 5000")
        except Exception as e:
            print(f"⚠️ Keep-alive server failed to start: {e}")
            print("Bot will continue without keep-alive server")

except ImportError:
    print("⚠️ Flask not available, keep-alive server disabled")
    def keep_alive():
        """Dummy keep-alive function when Flask is not available"""
        print("⚠️ Keep-alive server disabled (Flask not installed)")
        pass
