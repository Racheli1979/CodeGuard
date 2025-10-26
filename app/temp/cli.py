"""This module handles user commands and interfaces with the repository system."""
from typing import List
import os
import click
import requests
from classes import Commit
import function


@click.group()
def cli():
    """Wit CLI tool"""
    pass


@cli.command()
def init():
    """Initialize a new repository."""
    try:
        if not os.path.exists(".wit"):
            function.create_directory(f"{os.getcwd()}\\.wit",
                                      "Hello, the directory created successfully!")
            function.create_repo()
        else:
            raise Exception("7. Repository already initialize.")
    except Exception as e:
        click.echo(click.style(f"Error initializing wit: {e}", fg="red"))


@cli.command()
@click.argument('files', nargs=-1)
def add(files: List[str]):
    """Add files to staging copy."""
    try:
        repo = function.load_repo()
        if repo is None:
            raise Exception("Error: Repository is not initialized. Please run 'wit init' first.")
        if not files or files[0] == "":
            raise Exception(click.style("Command not valid.", fg="red"))
        else:
            function.copy_files(os.getcwd(), f'.wit/{str(repo.name_repo)}/Staging',
                                files, repo.wit_ignore)
            repo.add(files)
            function.save_repo(repo)
    except Exception as e:
        click.echo(click.style(f"5. Error adding files: {e}", fg="red"))


@cli.command()
@click.option('-m', '--message', required=True, help="The commit message.")
def commit(message):
    """Create a new commit."""
    try:
        repo = function.load_repo()
        staged = f'.wit/{str(repo.name_repo)}/Staging/'
        if not os.listdir(staged):
            raise Exception('No changes in the project')
        # יצירת commit חדש
        new_commit = Commit(message, os.listdir(staged))
        repo.list_commits.append(new_commit)

        # יצירת תיקיית commit חדשה
        repo_path = f'.wit\\{str(repo.name_repo)}\\Commited'

        function.create_directory(repo_path, "Directory date created successfully.")
        id_commit_path = os.path.join(repo_path, str(new_commit.commit_id))
        function.create_directory(id_commit_path,
                                  f"Directory id {id_commit_path} created successfully.")

        # העברת הקבצים מ-Staging
        function.move_files(staged, id_commit_path)
        click.echo(click.style("Directory staging moved successfully.", fg="green"))

        # קריאה של ה-commit הקודם מ-JSON
        prev_json_path = f'{os.getcwd()}/prev.json'
        prev_commit_id = function.get_last_commit(prev_json_path)
        if prev_commit_id:
            prev_commit_path = os.path.join(repo_path, f"{prev_commit_id}")
            if os.path.exists(prev_commit_path):
                # העתקת קבצים מה-commit הקודם
                function.copy_all_files(prev_commit_path, id_commit_path)
                click.echo(click.style(
                    f"Copied files from previous commit: {prev_commit_id}", fg="green"))
            else:
                click.echo(click.style("cant find dest !!!!!!!!!!!!!!!!!!!!!!!!!!!!!", fg="yellow"))

        # עדכון קובץ ה-JSON עם ה-commit הנוכחי
        function.get_last_commit(prev_json_path, new_commit.commit_id)

        # ניקוי Staging
        repo.staging = []
        function.save_repo(repo)
        click.echo(click.style(f"Commit {new_commit.commit_id} created successfully.", fg="green"))

    except Exception as e:
        click.echo(click.style(f"Error during commit: {e}", fg="red"))


@cli.command()
def log():
    """Display commit logs."""
    try:
        data = function.load_repo()
        for commit1 in data.list_commits:
            click.echo(click.style(
                "----------------------------------------------", fg="blue"))
            click.echo(click.style(f"{Commit(commit1['message'], commit1['list_files'])} ", fg="yellow"))
        click.echo(click.style(
            "----------------------------------------------", fg="blue"))

    except Exception as e:
        click.echo(click.style(f"4. Error: {e}", fg="red"))


@cli.command()
def status():
    """Show the staging area for files who hasn't commited yet."""
    repo = function.load_repo()
    if not repo.staging:
        click.echo(click.style("No changes in the project.", fg="cyan"))
    else:
        for file in repo.staging:
            click.echo(click.style(f'{file}', fg="cyan"))


@cli.command()
@click.argument('id_commit')
def checkout(id_commit):
    """Return the project to the selected commit."""
    try:
        repo = function.load_repo()
        for commit1 in repo.list_commits:
            if str(commit1['id_commit']) == str(id_commit):
                source = f'.wit/{repo.name_repo}/Commited/{id_commit}'
                dest = '.'
                function.checkout_files(source, dest)
                click.echo(click.style("Checkout success.", fg="green"))
    except Exception as e:
        click.echo(click.style(f'13. Error while checkout: {e}', fg="red"))


@cli.command()
@click.argument('route')
def push(route):
    """push the last commits to a remote repo,
    and analysis the code from lint errors."""
    item = {}
    try:
        response = requests.post(f"https://localhost:8000/{route}/",json=item)
        print(response.json())
    except Exception as e:
        pass
    pass


if __name__ == "__main__":
    cli()
