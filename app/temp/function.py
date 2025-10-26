import os
import shutil
from typing import List
import json
import pyfiglet
import click
from classes import Repository, File, Commit


def load_repo():
    """Load the repo data from the file that contain the repo data."""
    try:
        if os.path.exists('repo.json') and os.path.getsize('repo.json') > 0:
            with open('repo.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                repo = Repository(data['name_repo'])
                repo.list_commits = data['list_commits']
                repo.staging = data['staging']
                # repo.list_files = data['list_files']
                return repo
    except Exception as e:
        click.echo(click.style(f"1. Error loading repository: {e}", fg="red"))
    return None


def save_repo(repo: Repository):
    """Saving the repo to a file that contains the repo data."""
    try:
        if repo is not None and isinstance(repo, Repository):
            existing_data = {}
            if os.path.exists('repo.json') and os.path.getsize('repo.json') > 0:
                with open('repo.json', 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            existing_data['name_repo'] = getattr(repo, 'name_repo', None)
            existing_data['list_commits'] = existing_data.get('list_commits', [])
            if not repo.staging:
                existing_data['staging'] = []
            existing_data['staging'] = existing_data.get('staging', [])
            if 'list_commits' not in existing_data:
                existing_data['list_commits'] = []
            existing_data['list_commits'].extend(
                [commit_to_dict(commit) for commit in repo.list_commits if isinstance(commit, Commit)])
            # existing_data['staging'].extend([file_to_dict(stage) for stage in repo.staging])
            for stage in repo.staging:
                if repo.staging and not hasattr(stage, 'name'):
                    continue
                if not any(existing_file['file_name'] == stage.name for existing_file in existing_data['staging']):
                    existing_data['staging'].append(file_to_dict(stage))
                    print(click.style('success', fg="green"))
                else:
                    print(click.style("failed", fg="red"))

            with open('repo.json', 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=20)
        else:
            raise ValueError("Invalid repo object provided.")
    except Exception as e:
        click.echo(click.style(f"2. Error saving repository: {e}", fg="red"))


def file_to_dict(file: File):
    """Parse the object 'File' to dictionary."""
    return {
        'file_name': file.name,
        'path': file.path,
        'last_modified': file.last_modified
    }


def commit_to_dict(commit: Commit):
    """Parse the object 'Commit' to dictionary."""
    return {
        'id_commit': commit.commit_id,
        'message': commit.message.split("wit commit -m", 1)[0].strip(),
        'date': commit.date,
        'list_files': commit.list_files
    }


def create_repo():
    """create the repository and initialize it."""
    try:
        name_repo = click.prompt("Enter the repository name", type=str)
        repo = Repository(str(name_repo))
        banner = pyfiglet.figlet_format(f"WIT PROJECT: {name_repo}", font="3-d")
        click.echo(click.style(banner, fg="yellow", bg="blue", bold=True))

        save_repo(repo)
        repo_path = os.path.join(".wit", name_repo)
        create_directory(repo_path, f"Repository '{name_repo}' created successfully!")

        stage = os.path.join(repo_path, "Staging")
        create_directory(stage, "Directory Staging created successfully.")

        commit = os.path.join(repo_path, "Commited")
        create_directory(commit, "Directory Commited created successfully.")
    except Exception as e:
        click.echo(click.style(f"6. Error creating repository: {e}", fg="red"))


def create_directory(path, success_message):
    """A function that creates a directory in an accepted path."""
    if not os.path.exists(path):
        os.mkdir(path)
        click.echo(click.style(success_message, fg="green"))


def move_files(source_dir, dest_dir):
    """Specific function to remove the files from staging to the commited."""
    check_path(source_dir, dest_dir)
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        shutil.move(item_path, dest_dir)


def get_last_commit(file_path: str, new_value=None):
    """Copy the files who haven't added to staging from the last commit."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if new_value is not None:
            data['prev'] = new_value
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return str(new_value)
        else:
            if data['prev'] == 0:
                raise OSError("No commit in the repository.")
            return str(data.get('prev', None))

    except FileNotFoundError as exc:  # check commit
        raise f"The file {file_path} does not exist: {exc}."
    except json.JSONDecodeError as jsn:
        raise f"The file {file_path} is not a valid JSON file: {jsn}."


def checkout_files(source_dir, dest_dir):
    """Copy the files from the selected commit to the working copy."""
    check_path(source_dir, dest_dir)
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        shutil.copy(item_path, dest_dir)


def check_path(source, dest=None):
    """Checking the accepted path if it valid."""
    if not os.path.exists(source):
        raise FileExistsError("Source directory does not exist.")
    if dest:
        if not os.path.exists(dest):
            raise FileExistsError("Error: Repository is not initialized. Please run 'wit init' first.")


def copy_files(source_dir, dest_dir, files: List[str], ignore_list: List[str] = None):
    """A specific function to copy files from working copy to staging copy."""
    try:
        ignore_list = ignore_list or []

        check_path(source_dir, dest_dir)

        if files[0] == '.':
            files = os.listdir(source_dir)

        for filename in files:
            full_file_name = os.path.join(source_dir, filename)
            if any(ignore in full_file_name for ignore in ignore_list):
                continue

            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, dest_dir)
            elif os.path.isdir(full_file_name):
                shutil.copytree(full_file_name, os.path.join(dest_dir, filename),
                                dirs_exist_ok=True, ignore=shutil.ignore_patterns(*ignore_list))
            else:
                click.echo(f"Item '{filename}' does not exist in the source directory.")

    except MemoryError as e:
        click.echo(f"Error copying files: {e}")


def copy_all_files(source, dest):
    """Specific function to copy files from the last commit if they not in the commit directory."""
    if not os.path.exists(source):
        raise FileExistsError("Source directory does not exist.")

    if not os.path.exists(dest):
        raise FileExistsError("Error: Repository is not initialized. Please run 'wit init' first.")

    for filename in os.listdir(source):
        source_file = os.path.join(source, filename)
        target_file = os.path.join(dest, filename)

        if not os.path.exists(target_file):
            shutil.copy2(source_file, target_file)
