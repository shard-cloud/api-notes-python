#!/usr/bin/env python3
"""
FastAPI Notes API
Entry point da aplicação
"""

from src.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=80,
        reload=True
    )
