#!/usr/bin/env python

import os
import typer
from rich import print
from rich.prompt import Prompt
import openai
import readline

app = typer.Typer()

readline.parse_and_bind('"\e[A": history-search-backward')
readline.parse_and_bind('"\e[B": history-search-forward')
readline.parse_and_bind('"\e[C": forward-char')
readline.parse_and_bind('"\e[D": backward-char')

openai_organization_id = os.getenv("OPENAI_ORGANIZATION_ID")
openai_api_key = os.getenv("OPENAI_API_KEY")

openai.organization = openai_organization_id
openai.api_key = openai_api_key


def generate_text(
    prompt,
    temperature=0.6,
    max_tokens=2000,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0,
    turbo=True,
):
    if turbo:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt
            if isinstance(prompt, list)
            else [{"role": "user", "content": f"{prompt}"}],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
        text = response.choices[0]["message"]["content"]
        tokens = response.usage.total_tokens

    else:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt if isinstance(prompt, str) else prompt[-1].get("content"),
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
        text = response.choices[0].text
        tokens = response.usage.total_tokens

    return text, tokens


@app.command()
def main():
    messages = []
    prompt = ""
    while prompt != "q":
        prompt = Prompt.ask("$")
        print("")
        message = {"role": "user", "content": f"{prompt}"}
        messages.append(message)
        text, tokens = generate_text(prompt=messages)
        response = {"role": "assistant", "content": f"{text}"}
        messages.append(response)
        print(f"\n{text}\n")


def cli():
    """For python script installation purposes (flit)"""
    app()


if __name__ == "__main__":
    app()
