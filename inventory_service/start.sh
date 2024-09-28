#!/bin/bash

# Uygulamayı arka planda çalıştır
uvicorn app.main:app --host 0.0.0.0 --port 8004 &

# Consumer'ı çalıştır
python -m app.consumer
