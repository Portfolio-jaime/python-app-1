# 🏗️ Arquitectura y Despliegue

## Diagrama General

```mermaid
graph TD
    Dev[Desarrollador] --> CI[GitHub Actions]
    CI --> Docker[Docker Registry]
    Docker --> ArgoCD[ArgoCD]
    ArgoCD --> K8s[Kubernetes Cluster]
    K8s --> App[python-app-1]
```

## Componentes Clave

- **Flask App**: API REST y UI
- **Helm Chart**: Despliegue flexible en K8s
- **Ingress**: Exposición HTTP (python-app-1.test.com)
- **ArgoCD**: GitOps y sincronización automática
- **GitHub Actions**: CI/CD, build/push Docker, sync ArgoCD

---

# 📦 Estructura de Carpetas

```
python-app-1/
├── charts/                # Helm chart
├── src/                   # Código fuente Flask
├── templates/             # UI Jinja2
├── k8s/                   # Manifiestos legacy
├── .github/workflows/     # CI/CD
├── docs/                  # Documentación
├── Dockerfile             # Imagen Docker
├── requirements.txt       # Dependencias
└── README.md
```
