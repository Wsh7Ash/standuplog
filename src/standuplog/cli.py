#!/usr/bin/env python3
import subprocess, click
from datetime import datetime
from rich.console import Console
from .digest import parse_log, digest
console = Console()
@click.group()
@click.version_option()
def main(): pass
@main.command()
@click.option('--path', default='.', help='Git repo path')
def show(path):
    fmt = '%aI' + '\x1f' + '%an' + '\x1f' + '%s' + '\x1e'
    out = subprocess.run(['git', '-C', path, 'log', '--since=2 days ago', f'--pretty=format:{fmt}'],
                         capture_output=True, text=True)
    if out.returncode != 0:
        console.print(f'[red]{out.stderr.strip()}[/red]')
        raise SystemExit(1)
    buckets = digest(parse_log(out.stdout), datetime.now())
    if not buckets:
        console.print('[yellow]no commits in the last 2 days[/yellow]')
    for author, days in buckets.items():
        console.print(f'[bold]{author}[/bold]')
        for day in ('yesterday', 'today'):
            for s in days[day]:
                console.print(f'  {day}: {s}')
if __name__ == '__main__': main()
