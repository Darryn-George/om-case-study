

locals {
 file_indices = toset(["0", "2", "3", "4"]) # Skipping index 1
}

resource "local_file" "foo" {
  for_each = local.file_indices

  filename = "file${each.key}.txt"
  content  = "# Some content for file ${each.key}"
}
