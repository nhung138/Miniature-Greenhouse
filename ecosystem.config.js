 module.exports = {
  apps: [
    {
      name: "hardware-main",
      script: ".venv/bin/python",
      args: "main.py 1 0",
      interpreter: "none",
      restart_delay: 5000,
      env: { PYTHONUNBUFFERED: "1" }
    },
    {
      name: "api-backend",
      script: "uvicorn",
      args: "api:app --host 0.0.0.0 --port 8000",
      interpreter: ".venv/bin/python",
      restart_delay: 5000
    },
    {
      name: "web-frontend",
      cwd: "./greenhouse-dashboard",
      script: "npm",
      args: "run dev",
      restart_delay: 5000
    }
  ]
};
