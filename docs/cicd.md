# ⚙️ CI/CD y GitOps

## Pipeline GitHub Actions

- Build y push de imagen Docker
- Actualización automática de `values.yaml` (Helm)
- Commit y push con PAT
- Sincronización de ArgoCD vía CLI

### Ejemplo de workflow (`.github/workflows/cicd.yaml`):

```yaml
name: CI/CD
on:
  push:
    branches: [main]
jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build & Push Docker
        run: |
          docker build -t $IMAGE .
          docker push $IMAGE
      - name: Update values.yaml
        run: |
          yq e '.image.tag = "$TAG"' -i charts/python-app-1/values.yaml
      - name: Commit & Push
        run: |
          git config user.name "github-actions"
          git add .
          git commit -m "Update image tag"
          git push
      - name: Sync ArgoCD
        run: |
          argocd app sync python-app-1
```

## GitOps con ArgoCD

- Monitorea el repo y sincroniza cambios automáticamente
- Rollback y auditoría de despliegues
- Integración con Helm para valores dinámicos
