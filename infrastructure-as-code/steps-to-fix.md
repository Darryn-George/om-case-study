# Add steps/actions here:

1. step 1

# Lists all resources in the state and filters for those named local_file.foo
terraform state list | grep 'local_file.foo'

# Removes the resource with index [1] from the Terraform state (but does not delete the actual file).
terraform state rm 'local_file.foo[1]'

# Moves the state entries from numeric indices (e.g., [0]) to string indices (e.g., ["0"]).
# This is needed when you change your resource definition from a count-based resource to a for_each-based resource using string keys.
terraform state mv 'local_file.foo[0]' 'local_file.foo["0"]'
terraform state mv 'local_file.foo[2]' 'local_file.foo["2"]'
terraform state mv 'local_file.foo[3]' 'local_file.foo["3"]'
terraform state mv 'local_file.foo[4]' 'local_file.foo["4"]'

# Verifies the state after the changes.
terraform state list | grep 'local_file.foo'

3. step 2

locals {
 file_indices = toset(["0", "2", "3", "4"]) # Skipping index 1
}

resource "local_file" "foo" {
  for_each = local.file_indices

  filename = "file${each.key}.txt"
  content  = "# Some content for file ${each.key}"
}

4. etc

terraform plan
terraform apply
