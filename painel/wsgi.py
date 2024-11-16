"""Módulo para execução do servidor em produção."""

from app import app

server = app.server

if __name__ == "__main__":
    server.run()