variable "proxmox_api_url" {
  description = "URL API Proxmox (ex: https://192.168.102.11:8006/api2/json)"
  type        = string
}

variable "proxmox_api_token_id" {
  description = "Token ID Proxmox (ex: root@pam!terraform)"
  type        = string
  sensitive   = true
}

variable "proxmox_api_token_secret" {
  description = "Secret du token Proxmox"
  type        = string
  sensitive   = true
}

variable "proxmox_node" {
  description = "Nom du nœud Proxmox cible"
  type        = string
  default     = "pve"
}

variable "proxmox_template" {
  description = "Nom du template Cloud-Init Ubuntu"
  type        = string
  default     = "ubuntu-template"
}

variable "vm_name" {
  description = "Nom de la VM à créer"
  type        = string
  default     = "cia-test-vm"
}

variable "vm_cores" {
  description = "Nombre de vCPU"
  type        = number
  default     = 2
}

variable "vm_memory" {
  description = "RAM en Mo"
  type        = number
  default     = 2048
}

variable "vm_disk_size" {
  description = "Taille disque en Go"
  type        = string
  default     = "20G"
}

variable "vm_ip" {
  description = "IP statique Cloud-Init (CIDR)"
  type        = string
  default     = "192.168.10.20/24"
}

variable "vm_gateway" {
  description = "Passerelle par défaut"
  type        = string
  default     = "192.168.10.1"
}

variable "vm_nameserver" {
  description = "Serveur DNS"
  type        = string
  default     = "192.168.10.1"
}

variable "vm_ssh_user" {
  description = "Utilisateur SSH Cloud-Init"
  type        = string
  default     = "ubuntu"
}

variable "vm_ssh_public_key" {
  description = "Clé SSH publique pour Cloud-Init"
  type        = string
  sensitive   = true
}
