provider "proxmox" {
  pm_api_url          = var.proxmox_api_url
  pm_api_token_id     = var.proxmox_api_token_id
  pm_api_token_secret = var.proxmox_api_token_secret
  pm_tls_insecure     = true
}

resource "proxmox_vm_qemu" "cia_test" {
  name        = var.vm_name
  target_node = var.proxmox_node
  clone       = var.proxmox_template

  agent    = 1
  os_type  = "cloud-init"
  cores    = var.vm_cores
  sockets  = 1
  memory   = var.vm_memory
  scsihw   = "virtio-scsi-pci"
  bootdisk = "scsi0"

  disk {
    slot    = 0
    size    = var.vm_disk_size
    type    = "disk"
    storage = "local-lvm"
    iothread = 1
  }

  network {
    model  = "virtio"
    bridge = "vmbr0"
  }

  ipconfig0 = "ip=${var.vm_ip},gw=${var.vm_gateway}"

  nameserver = var.vm_nameserver

  sshkeys = var.vm_ssh_public_key

  lifecycle {
    ignore_changes = [
      network,
    ]
  }
}
