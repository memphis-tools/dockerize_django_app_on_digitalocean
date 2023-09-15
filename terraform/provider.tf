// Tell Terraform that you want to use the DigitalOcean provider
terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

// Configure the DigitalOcean provider and specify the credentials for your DigitalOcean account
// Nothing to set here, no hardcode, variables will be set on execution
variable "do_token" {}
variable "pvt_key" {}

provider "digitalocean" {
  token = var.do_token
}

// We want to have Terraform automatically add your SSH key to any new Droplets we create
// Replace terraform with the name of the key you provided in your DigitalOcean account
data "digitalocean_ssh_key" "terraform" {
  name = "terraform"
}
