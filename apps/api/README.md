# ☁️ TOTP Authenticator - Cloud Sync Server

This is the Backend Server (FastAPI) source code that powers the Cloud Sync feature for the TOTP Authenticator Desktop app.

This server is strictly designed around **End-to-End Encryption (E2EE)** principles. It acts purely as a "blind storage" box. The backend never receives the encryption keys and has absolutely zero ability to decrypt your TOTP secrets. Because of this zero-knowledge architecture, you can safely use our default hosted server or host this backend yourself with complete peace of mind.

## 🚀 1-Click Deploy (For Free Tier Services)

You can launch this backend into the cloud instantly without writing any code or dealing with server configurations. The platform will automatically clone the repository and build the environment:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

*(Note: If deploying to Render with SQLite, it is highly recommended to configure a Persistent Disk mounted at `/data` so your database is not wiped when Render restarts the free instance).*

## 🐳 Self-Hosting with Docker (Recommended)

If you own a personal VPS (Ubuntu, CentOS) or a home NAS (like Synology/Raspberry Pi), deploying this server with Docker is incredibly fast and reliable:

1. Clone this repository and navigate to the API directory:
   ```bash
   git clone <repo-url>
   cd topt-authenticator/apps/api
   ```

2. Start the server in the background:
   ```bash
   docker compose up -d
   ```

3. That's it! The server is now running at `http://localhost:8000`. 
   In your Desktop App's Sync Settings, simply enter `http://<your-vps-ip>:8000` as the Server URL to start syncing.

## ⚙️ Environment Variables

- `SECRET_KEY`: A secure random string used to sign JWT authentication tokens. **You must change this to a strong random value before deploying to the internet!**
- `DATABASE_URL`: The SQLAlchemy connection string for the database. Defaults to `sqlite:////data/totp_sync.db` (which perfectly aligns with the Docker Volume mount).
