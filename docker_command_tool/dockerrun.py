import subprocess


def collect_inputs():
    config = {}

    config["image"] = input("Image name (required): ").strip()
    config["name"] = input("Container name: ").strip()
    detach = input("Run detached? (y/n): ").strip().lower()
    config["detach"] = detach == "y"

    config["network"] = input("Attach to network (Empty if none): ").strip()

    ports = input(
        "Expose ports (host:container, comma separated | Empty if none): "
    ).strip()
    config["ports"] = (
        [p.strip() for p in ports.split(",") if p.strip()] if ports else []
    )

    volumes = input(
        "Mount volumes (source:target, comma separated | Empty if none): "
    ).strip()
    config["volumes"] = (
        [v.strip() for v in volumes.split(",") if v.strip()] if volumes else []
    )

    env_vars = input(
        "Environment variables (KEY=value, comma separated | Empty if none): "
    ).strip()
    config["env"] = (
        [e.strip() for e in env_vars.split(",") if e.strip()] if env_vars else []
    )

    config["restart"] = input("Restart policy (no/unless-stopped/always): ").strip()

    return config


def build_command(config):
    command = ["docker", "run"]

    if config["detach"]:
        command.append("-d")

    if config["name"]:
        command.extend(["--name", config["name"]])

    if config["network"]:
        command.extend(["--network", config["network"]])

    for port in config["ports"]:
        command.extend(["-p", port])

    for volume in config["volumes"]:
        command.extend(["-v", volume])

    for env in config["env"]:
        command.extend(["-e", env])

    if config["restart"]:
        command.extend(["--restart", config["restart"]])

    command.append(config["image"])

    return command


def confirm_and_execute(command):
    print("\nGenerated command:")
    print(" ".join(command))

    confirm = input("\nExecute this command? (y/n): ").strip().lower()

    if confirm == "y":
        subprocess.run(command)
    else:
        print("Aborted.")


def main():
    config = collect_inputs()

    if not config["image"]:
        print("Image is required.")
        return

    command = build_command(config)
    confirm_and_execute(command)


if __name__ == "__main__":
    main()
