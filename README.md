# GitOps Kubernetes avec FluxCD

Ce dépôt contient une structure GitOps multi-environnements (`dev` et `prod`) prête pour FluxCD.

## Arborescence

- `clusters/dev`: point d'entrée Flux pour l'environnement de développement.
- `clusters/prod`: point d'entrée Flux pour l'environnement de production.
- `infrastructure/dev` et `infrastructure/prod`: namespaces et éléments d'infrastructure par environnement.
- `apps/base`: base commune des applications.
- `apps/dev` et `apps/prod`: overlays applicatifs par environnement.

## Prérequis

- Un cluster Kubernetes accessible avec `kubectl`.
- Le CLI Flux installé localement.
- Un token GitHub avec droits sur le dépôt.

## Bootstrap Flux

Remplace `YOUR_GITHUB_TOKEN` puis choisis l'environnement a brancher.

### Bootstrap `dev`

```bash
export GITHUB_TOKEN=YOUR_GITHUB_TOKEN
flux bootstrap github \
  --owner=Meriem1403 \
  --repository=T-NSA-810---CIA \
  --branch=main \
  --path=clusters/dev \
  --personal
```

### Bootstrap `prod`

```bash
export GITHUB_TOKEN=YOUR_GITHUB_TOKEN
flux bootstrap github \
  --owner=Meriem1403 \
  --repository=T-NSA-810---CIA \
  --branch=main \
  --path=clusters/prod \
  --personal
```

## Vérification

```bash
kubectl get pods -n flux-system
flux get sources git -A
flux get kustomizations -A
```

## Exemple inclus

Une application de démonstration `podinfo` est incluse:

- en `dev` sur le namespace `apps-dev` avec `replicaCount: 1`
- en `prod` sur le namespace `apps-prod` avec `replicaCount: 2`
