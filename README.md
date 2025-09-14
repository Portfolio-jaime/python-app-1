# python-app-1

Aplicación web Python Flask lista para Kubernetes, CI/CD, Helm y GitOps.

---

## 📦 Estructura del Proyecto

```
python-app-1/
├── charts/                # Helm chart para despliegue en K8s
├── src/                   # Código fuente Flask
├── templates/             # Plantillas UI (Jinja2)
├── k8s/                   # Manifiestos K8s legacy (referencia)
├── .github/workflows/     # Pipeline CI/CD (GitHub Actions)
├── docs/                  # Documentación extendida
├── Dockerfile             # Imagen Docker
├── requirements.txt       # Dependencias Python
└── README.md              # Este archivo
```

---

## 🚀 Endpoints y UI

- `/` : UI web (HTML, consulta endpoints)
- `/api/v1/info` : Info de despliegue
- `/api/v1/healthz` : Health check (K8s)
- `/api/v1/readyz` : Readiness check
- `/api/v1/version` : Versión app
- `/api/v1/env` : Variables de entorno

---

## 🏗️ Despliegue con Helm

```sh
helm install python-app-1 ./charts/python-app-1 \
  --set image.repository=jaimehenao8126/python-app-1 \
  --set image.tag=<tag>
```

- Ingress por defecto: `python-app-1.test.com`
- Health/readiness: `/api/v1/healthz`

---

## ⚙️ CI/CD y GitOps

- Pipeline: `.github/workflows/cicd.yaml`
- Build/push Docker, update values.yaml, sync ArgoCD
- Despliegue automático en K8s vía ArgoCD

---

## 📝 Documentación Extendida

- [docs/index.md](./docs/index.md): Uso de endpoints, ejemplos curl, detalles de API
- [charts/python-app-1/](./charts/python-app-1/): Helm chart y valores

---

## 🧩 Casos de Uso

- Demo de despliegue cloud native
- Ejemplo de integración CI/CD y GitOps
- Pruebas de health/readiness en K8s

---

## 👤 Autor

Jaime Andrés Henao
