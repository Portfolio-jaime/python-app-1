# 🚀 Casos de Uso y Pruebas

## Casos de Uso

- Despliegue cloud native de microservicio Python
- Demo de health/readiness probes en Kubernetes
- Ejemplo de integración CI/CD y GitOps
- Pruebas de UI y API REST

## Pruebas Manuales

### Probar endpoint de salud
```bash
curl http://python-app-1.test.com/api/v1/healthz
```

### Probar UI web
Abre en navegador: http://python-app-1.test.com/

### Probar info de despliegue
```bash
curl http://python-app-1.test.com/api/v1/info
```

### Probar readiness
```bash
curl http://python-app-1.test.com/api/v1/readyz
```

### Probar versión
```bash
curl http://python-app-1.test.com/api/v1/version
```
