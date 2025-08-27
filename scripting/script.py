import json
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <tfplan.json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        plan = json.load(f)

    # Terraform plan JSON structure: look for "resource_changes"
    changes = plan.get("resource_changes", [])
    allowed = True
    for change in changes:
        actions = change.get("change", {}).get("actions", [])
        address = change.get("address", "unknown resource")

        # Only allow create or modify
        if any(a not in ("create", "modify") for a in actions):
            print(f"Resource '{address}' has forbidden action(s): {actions}. Plan must not proceed.")
            allowed = False
            continue

        # If modify, check only tags.GitCommitHash is changed
        if actions == ["modify"]:
            before = change["change"].get("before", {})
            after = change["change"].get("after", {})
            # Only allow 'tags' attribute to change
            before_tags = before.get("tags", {})
            after_tags = after.get("tags", {})
            # Check if only 'tags' changed
            changed_keys = [k for k in after if before.get(k) != after.get(k)]
            if changed_keys != ["tags"]:
                print(f"Resource '{address}' modifies attributes other than 'tags': {changed_keys}. Plan must not proceed.")
                allowed = False
                continue
            # Within tags, only allow 'GitCommitHash' to change
            tag_keys = set(before_tags.keys()) | set(after_tags.keys())
            for tag in tag_keys:
                if before_tags.get(tag) != after_tags.get(tag):
                    if tag != "GitCommitHash":
                        print(f"Resource '{address}' modifies tag '{tag}' (not allowed). Plan must not proceed.")
                        allowed = False

    if allowed:
        print("Plan is safe to apply.")
    else:
        print("Plan must NOT proceed.")

if __name__ == "__main__":
    main()

# change script to whatever language you are comfortable with
