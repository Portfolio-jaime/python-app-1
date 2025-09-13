# Python Flask Application

Aplicación web sencilla desarrollada en Python Flask para demostración de despliegues con Kubernetes y GitOps.

## 🎯 Descripción

Esta aplicación Flask proporciona una API REST básica con endpoints para información del sistema y health checks, ideal para demostraciones de:

- Despliegues en Kubernetes
- Pipelines CI/CD
- Monitoreo y observabilidad
- Patrones de microservicios

## 📋 Características

- **Framework**: Flask (Python)
- **Endpoints REST**: JSON API
- **Health Checks**: Endpoint de salud para Kubernetes
- **Containerizada**: Docker ready
- **Cloud Native**: 12-factor app compliant

## 🚀 API Endpoints

### GET `/api/v1/info`

Devuelve información del sistema y la aplicación.

**Response:**
```json
{
    "time": "02:30:45PM on August 25, 2025",
    "hostname": "python-app-1-pod-xyz",
    "message": "You are doing great, little human! <3",
    "deployed_on": "kubernetes"
}
```

**Ejemplo:**
```bash
curl -X GET http://python-app-1.test.com/api/v1/info
```

### GET `/api/v1/healthz`

Health check endpoint para Kubernetes probes.

**Response:**
```json
{
    "status": "up"
}
```

**HTTP Status Codes:**
- `200 OK`: Aplicación saludable
- `503 Service Unavailable`: Aplicación no disponible

**Ejemplo:**
```bash
curl -X GET http://python-app-1.test.com/api/v1/healthz
```

## 🐳 Containerización

### Dockerfile
La aplicación está containerizada usando una imagen base de Python:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Build y Run Local
```bash
# Build de la imagen
docker build -t python-app-1 .

# Ejecutar localmente
docker run -p 5000:5000 python-app-1

# Verificar que funciona
curl http://localhost:5000/api/v1/healthz
```

## ☸️ Despliegue en Kubernetes

### Manifiestos Base

La aplicación se despliega usando los siguientes recursos de Kubernetes:

- **Deployment**: Gestiona los pods de la aplicación
- **Service**: Expone la aplicación dentro del cluster
- **Ingress**: (Opcional) Routing externo

### Despliegue Rápido
```bash
# Aplicar manifiestos
kubectl apply -f k8s/

# Verificar estado
kubectl get pods,svc -n default

# Port forward para testing
kubectl port-forward svc/python-app-1 5000:80

# Test de conectividad
curl http://localhost:5000/api/v1/healthz
```

### Health Checks en Kubernetes

La aplicación está configurada con probes de Kubernetes:

```yaml
livenessProbe:
  httpGet:
    path: /api/v1/healthz
    port: 5000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /api/v1/healthz
    port: 5000
  initialDelaySeconds: 5
  periodSeconds: 5
```

## 🔧 Desarrollo Local

### Requisitos
- Python 3.9+
- pip
- Flask

### Setup del Entorno
```bash
# Clonar repositorio
git clone https://github.com/Portfolio-jaime/python-app-1.git
cd python-app-1

# Crear virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
cd src
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

### Testing
```bash
# Test del endpoint info
curl http://localhost:5000/api/v1/info

# Test del health check
curl http://localhost:5000/api/v1/healthz

# Verificar JSON response
curl -H "Accept: application/json" http://localhost:5000/api/v1/info | jq
```

## 📊 Monitoreo

### Métricas Disponibles

La aplicación expone información útil para monitoreo:

- **Hostname**: Identificación del pod/contenedor
- **Timestamp**: Para verificar que la aplicación responde
- **Health Status**: Estado de la aplicación

### Integración con Prometheus

Para monitoreo avanzado, la aplicación puede extenderse con métricas de Prometheus:

```python
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('request_duration_seconds', 'Request latency')

@app.route('/metrics')
def metrics():
    return generate_latest()
```

## 🔐 Seguridad

### Mejores Prácticas Implementadas

1. **Non-root User**: Container ejecuta como usuario no-root
2. **Minimal Base Image**: Usa imagen slim para reducir superficie de ataque
3. **Health Checks**: Endpoints para verificar estado de la aplicación
4. **Environment Variables**: Configuración via variables de entorno

### Variables de Entorno

```bash
# Puerto de la aplicación (default: 5000)
FLASK_PORT=5000

# Modo debug (solo development)
FLASK_DEBUG=false

# Environment
FLASK_ENV=production
```

## 🚀 CI/CD Pipeline

La aplicación está integrada con GitHub Actions para:

1. **Testing**: Ejecución de tests unitarios
2. **Security Scanning**: Análisis de vulnerabilidades
3. **Docker Build**: Construcción automática de imágenes
4. **Deployment**: Actualización automática de manifiestos

### Workflow Ejemplo
```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Run tests
      run: python -m pytest tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Build Docker image
      run: docker build -t python-app-1 .
```

## 📈 Escalabilidad

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: python-app-1-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: python-app-1
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## 🐛 Troubleshooting

### Problemas Comunes

#### Aplicación no responde
```bash
# Verificar logs
kubectl logs -l app=python-app-1

# Verificar estado de pods
kubectl get pods -l app=python-app-1

# Port forward para debug
kubectl port-forward deployment/python-app-1 5000:5000
```

#### Health check falla
```bash
# Test directo al pod
kubectl exec -it deployment/python-app-1 -- curl localhost:5000/api/v1/healthz

# Verificar configuración de probes
kubectl describe deployment python-app-1
```

## 📞 Soporte

**Autor:** Jaime Henao  
**Email:** jaime.andres.henao.arbelaez@ba.com  
**Organización:** British Airways DevOps Team  
**GitHub:** [@Portfolio-jaime](https://github.com/Portfolio-jaime)

---

**Aplicación Python Flask - DevOps Portfolio** 