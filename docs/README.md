# Using the Mirascope CLI

One of the main frustrations of dealing with prompts and calls is keeping track of all the various revisions. Taking inspiration from alembic and git, the Mirascope CLI provides a couple of key commands to make managing prompts and calls easier.

## Installation

To install just the CLI, you can run `pip install mirascope-cli`.

If you're using `mirascope`, you can run `pip install mirascope[mirascope-cli]` or `pip install mirascope[all]` to install the Mirascope CLI.

## The prompt management environment

The first step to using the Mirascope CLI is to use the `init` command in your project's root directory.

```shell
mirascope init
```

This will create the directories and files to help manage prompts and calls.
Here is a sample structure created by the `init` function:

```plaintext
|
|-- mirascope.ini
|-- mirascope
|   |-- prompt_template.j2
|   |-- versions/
|   |   |-- <directory_name>/
|   |   |   |-- version.txt
|   |   |   |-- <revision_id>_<directory_name>.py
|-- prompts/
```

Here is a rundown of each directory and file:

- `mirascope.ini` - The INI file that can be customized for your project
- `mirascope` - The default name of the directory that is home to the prompt management environment
- `prompt_template.j2` - The Jinja2 template file that is used to generate prompt versions
- `versions` - The directory that holds the various prompt versions
- `versions/<directory_name` - The sub-directory that is created for each prompt file in the `prompts` directory
- `version.txt` - A file system method of keeping track of current and latest revisions. Coming soon is revision tracking using a database instead
- `<revision_id>_<directory_name>.py` - A prompt version that is created by the `mirascope add` command, more on this later.
- `prompts` - The user's directory that stores all prompt and call files

The directory names can be changed anytime by modifying the `mirascope.ini` file or when running the `init` command.

```shell
mirascope init --mirascope_location my_mirascope --prompts_location calls
```

## Saving your first prompt

After creating the prompt management directory, you are now ready to build and iterate on some prompts. Begin by adding a Mirascope Prompt to the prompts directory.

```python
# prompts/book_recommender.py
from mirascope.openai import OpenAICall, OpenAICallParams


class BookRecommender(OpenAICall):
    prompt_template = "Can you recommend some books on {topic} in a list format?"

    topic: str
    
    call_params = OpenAICallParams(model="gpt-3.5-turbo")
```

Once you are happy with the first iteration of this prompt, you can run:

```shell
mirascope add book_recommender
```

This will commit `book_recommender.py` to your `versions/` directory, creating a `book_recommender` sub-directory and a `0001_book_recommender.py`.

Here is what `0001_book_recommender.py` will look like:

```python
# versions/book_recommender/0001_book_recommender.py
from mirascope.openai import OpenAICall, OpenAICallParams

prev_revision_id = "None"
revision_id = "0001"


class BookRecommender(OpenAICall):
    prompt_template = "Can you recommend some books on {topic} in a list format?"

    topic: str
    
    call_params = OpenAICallParams(model="gpt-3.5-turbo")
```

The prompt inside the versions directory is almost identical to the prompt inside the prompts directory with a few differences.

The variables `prev_revision_id` and `revision_id` will be used for features coming soon, so stay tuned for updates.

## Colocate

**Everything that affects the quality of a prompt lives in the prompt.** This is why `call_params` exists in `BaseCall` and why `OpenAICall` and other provider wrappers extend the `BasePrompt` class.

## Iterating on the prompt

Now that this version of `book_recommender` has been saved, you are now free to modify the original `book_recommender.py` and iterate. Maybe, you want to switch to a different provider and compare results.

Here is what the next iteration of `book_recommender.py` will look like:

```python
# prompts/book_recommender.py
from google.generativeai import configure
from mirasope.gemini import GeminiCall, GeminiCallParams

configure(api_key="YOUR_GEMINI_API_KEY")


class BookRecommender(GeminiCall):
	prompt_template = "Can you recommend some books on {topic} in a list format?"

	ingredient: str

	call_params = GeminiCallParams(model="gemini-1.0-pro")
```

Before adding the next revision of `my_prompt`, you may want to check the status of your prompt.

```shell
# You can specify a specific prompt
mirascope status my_prompt

# or, you can check the status of all prompts
mirascope status
```

Note that status will also be checked before the `add` or `use` command is run.
Now we can run the same `add` command in the previous section to commit another version `0002_book_recommender.py`

## Switching between versions

You can now freely switch different providers or use the same provider with a different model to iterate to the best results.

You can use the `use` command to quickly switch between the prompts:

```shell
mirascope use book_recommender 0001
```

Here you specify which prompt and also which version you want to use. This will update your `prompts/book_recommender.py` with the contents of `versions/0001_book_recommender.py` (minus the variables used internally).

This will let you quickly swap prompts or providers with **no code change**, the exception being when prompts have different attributes. In that case, your **linter will detect missing or additional attributes** that need to be addressed.

## Removing prompts

Often times when experimenting with prompts, a lot of experimental prompts will need to be cleaned up in your project.

You can use the `remove` command to delete any version:

```shell
mirascope remove book_recommender 0001
```

Here you specify which prompt and version you want to remove. Removal will delete the file but also update any versions that have the deleted version in their `prev_revision_id` to `None`.

!!! note

    `mirascope remove` will not remove the prompt if `current_revision` is the same as the prompt you are trying to remove. You can use `mirascope add` if you have incoming changes or `mirascope use` to swap `current_revision`.

## Mirascope INI

The Mirascope INI provides some customization for you. Feel free to update any field.

```python
[mirascope]

# path to mirascope directory
mirascope_location = .mirascope

# path to versions directory
versions_location = %(mirascope_location)s/versions

# path to prompts directory
prompts_location = prompts

# name of versions text file
version_file_name = version.txt

# formats the version file
# leave blank to not format 
format_command = ruff check --select I --fix; ruff format

# auto tag prompts with version
auto_tag = True
```

- `auto_tag` - Adds `@tags(["version:0001"])` to Mirascope Prompts. This will auto increment the version number if a new version is added.

## Future updates

There is a lot more to be added to the Mirascope CLI. Here is a list in no order of things we are thinking about adding next:

- prompt comparison - A way to compare two different versions with a golden test
- history - View the revision history of a version
- testing - Adding input and outputs to the revision for CI testing

If you want some of these features implemented or if you think something is useful but not on this list, let us know!
