# Archive : squelette FluxCD + Kubernetes

Ce dossier contenait une structure GitOps (**Flux**, **Helm**, app de démo `podinfo`) pour un cluster Kubernetes avec environnements `dev` et `prod`.

Elle **n’est pas le cœur** du projet CIA (Proxmox hybride, OpenVPN, pfSense, NetBox, Elasticsearch). Elle est conservée pour :

- réutilisation future (bonus CI/CD, « golden paths »),
- ou démonstration d’IaC applicatif sur K8s si autorisée en bonus.

Réactivation Flux : depuis la racine du dépôt, passer `--path=legacy/flux-bootstrap/clusters/dev` (ou `clusters/prod`) lors du `flux bootstrap github`. Il faut un cluster Kubernetes et un jeton GitHub ayant les droits sur ce dépôt.
