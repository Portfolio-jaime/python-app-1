# Python Flask Application (Version 1)

Aplicación web Flask con despliegue automatizado usando Helm Charts y ArgoCD.

## 🎯 Descripción

Esta es una versión alternativa de la aplicación Python Flask, configurada con:

- **Helm Charts**: Para gestión de configuraciones
- **ArgoCD**: Para despliegue GitOps
- **Múltiples entornos**: Dev, Staging, Production
- **Monitoreo**: Integración con Prometheus y Grafana

## 📋 API Endpoints

### GET `/api/v1/info`

Endpoint que devuelve información del sistema y timestamp actual.

**Funcionalidad:**
- Muestra fecha y hora actual
- Hostname del contenedor/pod
- Mensaje de confirmación
- Información de deployment

**Respuesta esperada:**
```json
{
    "time": "02:30:45PM on August 25, 2025",
    "hostname": "python-app-1-pod-abc123",
    "message": "You are doing great, little human! <3",
    "deployed_on": "kubernetes"
}
```

### GET `/api/v1/healthz`

Health check endpoint para Kubernetes liveness y readiness probes.

**Funcionalidad:**
- Verifica que la aplicación esté funcionando
- Usado por Kubernetes para health checks
- Endpoint crítico para disponibilidad

**Respuesta esperada:**
```json
{
    "status": "up"
}
```

## 🚀 Acceso a la Aplicación

### URLs de Entornos

- **Development**: `python-app-1-dev.test.com`
- **Staging**: `python-app-1-staging.test.com`  
- **Production**: `python-app-1.test.com`

### Ejemplos de Uso

```bash
# Test del health check
curl https://python-app-1.test.com/api/v1/healthz

# Obtener información del sistema
curl https://python-app-1.test.com/api/v1/info

# Con headers JSON
curl -H "Accept: application/json" https://python-app-1.test.com/api/v1/info | jq
```

## ⚙️ Configuración con Helm

### Estructura de Charts

```
charts/
├── python-app/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       └── _helpers.tpl
└── argocd/
    └── values-argo.yaml
```

### Values por Entorno

#### Development
```yaml
replicaCount: 1
image:
  tag: "dev"
resources:
  requests:
    cpu: 100m
    memory: 128Mi
ingress:
  host: python-app-1-dev.test.com
```

#### Production
```yaml
replicaCount: 3
image:
  tag: "latest"
resources:
  requests:
    cpu: 200m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi
ingress:
  host: python-app-1.test.com
```

### Despliegue con Helm

```bash
# Instalar en desarrollo
helm install python-app-1-dev ./charts/python-app \
  -f charts/python-app/values-dev.yaml \
  -n python-app-1-dev \
  --create-namespace

# Upgrade en producción
helm upgrade python-app-1 ./charts/python-app \
  -f charts/python-app/values-prod.yaml \
  -n python-app-1-prod
```

## 🔄 GitOps con ArgoCD

### Configuración de Aplicación ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: python-app-1
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/Portfolio-jaime/python-app-1.git
    targetRevision: HEAD
    path: charts/python-app
    helm:
      valueFiles:
      - values-prod.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: python-app-1
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Multi-Environment Setup

```bash
# Crear aplicaciones para todos los entornos
environments=("dev" "staging" "prod")

for env in "${environments[@]}"; do
  argocd app create python-app-1-$env \
    --repo https://github.com/Portfolio-jaime/python-app-1.git \
    --path charts/python-app \
    --helm-set-file values-$env.yaml \
    --dest-server https://kubernetes.default.svc \
    --dest-namespace python-app-1-$env \
    --sync-policy automated
done
```

## 📊 Monitoreo y Observabilidad

### ServiceMonitor para Prometheus

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: python-app-1
  namespace: python-app-1
spec:
  selector:
    matchLabels:
      app: python-app-1
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
```

### Dashboards de Grafana

- **Application Metrics**: Response time, error rate, throughput
- **Infrastructure**: CPU, Memory, Network usage
- **Business**: Request patterns, user activity

### Alertas Críticas

```yaml
groups:
- name: python-app-1.rules
  rules:
  - alert: PythonApp1Down
    expr: up{job="python-app-1"} == 0
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Python App 1 is down"

  - alert: PythonApp1HighErrorRate
    expr: rate(flask_http_request_exceptions_total[5m]) > 0.1
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "High error rate in Python App 1"
```

## 🔧 Desarrollo Local

### Requisitos
- Python 3.9+
- Docker
- Helm 3.x
- kubectl

### Setup Rápido

```bash
# Clonar y setup
git clone https://github.com/Portfolio-jaime/python-app-1.git
cd python-app-1

# Ejecutar con Docker Compose
docker-compose up -d

# Verificar funcionamiento
curl http://localhost:5000/api/v1/healthz
```

### Testing Local con Helm

```bash
# Validar templates
helm template python-app-1 ./charts/python-app \
  -f charts/python-app/values-dev.yaml

# Dry run
helm install python-app-1-test ./charts/python-app \
  -f charts/python-app/values-dev.yaml \
  --dry-run --debug

# Deploy local
helm install python-app-1-local ./charts/python-app \
  -f charts/python-app/values-dev.yaml
```

## 🐛 Troubleshooting

### Problemas Comunes

#### Helm Release Fails
```bash
# Verificar status del release
helm status python-app-1

# Ver historia
helm history python-app-1

# Rollback si es necesario
helm rollback python-app-1 1
```

#### ArgoCD Sync Issues
```bash
# Verificar estado
argocd app get python-app-1

# Forzar sync
argocd app sync python-app-1 --force

# Ver diff
argocd app diff python-app-1
```

#### Application Not Responding
```bash
# Port forward para debug
kubectl port-forward svc/python-app-1 5000:80 -n python-app-1

# Verificar logs
kubectl logs -l app=python-app-1 -n python-app-1 --tail=100

# Verificar health checks
kubectl describe pod -l app=python-app-1 -n python-app-1
```

## 🚀 CI/CD Pipeline

### GitHub Actions Integration

```yaml
name: Python App 1 Pipeline
on:
  push:
    branches: [main, develop]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Build Docker Image
      run: docker build -t python-app-1:${{ github.sha }} .
      
    - name: Update Helm Values
      run: |
        yq eval '.image.tag = "${{ github.sha }}"' -i charts/python-app/values.yaml
        
    - name: Commit Changes
      run: |
        git add charts/python-app/values.yaml
        git commit -m "Update image tag to ${{ github.sha }}"
        git push
```

### Automated Testing

```bash
# Unit tests
python -m pytest src/tests/

# Integration tests
helm test python-app-1

# Security scanning
trivy image python-app-1:latest
```

## 📈 Métricas de Rendimiento

### SLIs (Service Level Indicators)
- **Availability**: > 99.9%
- **Response Time**: < 200ms (P95)
- **Error Rate**: < 0.1%
- **Throughput**: > 1000 RPS

### Capacity Planning
- **CPU**: 200m requests, 500m limits
- **Memory**: 256Mi requests, 512Mi limits
- **Replicas**: Min 2, Max 10 (HPA)

---

**Aplicación Python Flask v1 - Portfolio DevOps** 