output "vm_id" {
  description = "ID Proxmox de la VM créée"
  value       = proxmox_vm_qemu.cia_test.vmid
}

output "vm_name" {
  description = "Nom de la VM"
  value       = proxmox_vm_qemu.cia_test.name
}

output "vm_ip" {
  description = "Adresse IP configurée (Cloud-Init)"
  value       = var.vm_ip
}
