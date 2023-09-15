resource "digitalocean_droplet" "dummy-django-with-docker" {
    # you can set 'ubuntu-22-04-x64' image too without changing anything.
    image = "debian-12-x64"
    name = "dummy-ops"
    region = "fra1"
    size = "s-1vcpu-1gb"
    ssh_keys = [
      data.digitalocean_ssh_key.terraform.id
    ]

    connection {
      host = self.ipv4_address
      user = "root"
      type = "ssh"
      private_key = file(var.pvt_key)
      timeout = "2m"
    }

    provisioner "remote-exec" {
      inline = [
        "export PATH=$PATH:/usr/bin",
        # Add Docker's official GPG key:
        "sudo apt update -y",
        "sudo apt install ca-certificates curl gnupg -y",
        "sudo install -m 0755 -d /etc/apt/keyrings",
        "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg",
        "sudo chmod a+r /etc/apt/keyrings/docker.gpg",

        # We install docker and docker-compose (avoid any prompt with DEBIAN_FRONTEND)
        "sudo DEBIAN_FRONTEND=noninteractive apt install -y docker.io docker-compose"
      ]
    }
}
